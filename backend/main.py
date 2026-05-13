import docker
import os
import uuid
import json
import requests
import time
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = docker.from_env()
active_agents: Dict[str, dict] = {}
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3"
REGISTRY_PATH = "workspaces/agents_registry.json"

# --- PERSISTENCE LOGIC ---
def save_registry():
    os.makedirs("workspaces", exist_ok=True)
    with open(REGISTRY_PATH, "w") as f:
        data = {k: v["config"] for k, v in active_agents.items()}
        json.dump(data, f, indent=4)

def load_registry():
    if os.path.exists(REGISTRY_PATH):
        try:
            with open(REGISTRY_PATH, "r") as f:
                data = json.load(f)
                for k, v in data.items():
                    if k in active_agents:
                        active_agents[k]["config"] = v
        except Exception as e:
            print(f"Registry load error: {e}")

@app.on_event("startup")
async def startup_event():
    print("--- Hard-Syncing Units from Docker ---")
    containers = client.containers.list(all=True)
    for c in containers:
        if c.name.startswith("nexus_agent_"):
            agent_id = c.name.replace("nexus_agent_", "")
            active_agents[agent_id] = {
                "id": agent_id,
                "container": c.name,
                "config": {"name": f"Unit-{agent_id}", "role": "Nexus Agent"}
            }
    load_registry()
    print(f"--- System Online: {len(active_agents)} units recovered ---")

# --- DATA MODELS ---
class AgentRequest(BaseModel):
    name: str
    role: str

class MultiTaskRequest(BaseModel):
    agent_ids: List[str]
    prompt: str

# --- ENDPOINTS ---
@app.get("/forge/agents")
async def list_agents():
    return active_agents

@app.post("/forge/spawn")
async def spawn_agent(req: AgentRequest):
    agent_id = str(uuid.uuid4())[:6]
    c_name = f"nexus_agent_{agent_id}"
    
    base = os.getcwd()
    agent_ws = os.path.abspath(os.path.join(base, "workspaces", c_name))
    shared_ws = os.path.abspath(os.path.join(base, "workspaces", "_shared"))
    os.makedirs(agent_ws, exist_ok=True)
    os.makedirs(shared_ws, exist_ok=True)

    try:
        client.containers.run(
            "alpine", name=c_name, detach=True, tty=True,
            volumes={agent_ws: {'bind': '/home/agent/workspace', 'mode': 'rw'},
                     shared_ws: {'bind': '/home/agent/shared', 'mode': 'rw'}},
            command="sh"
        )
        active_agents[agent_id] = {"id": agent_id, "container": c_name, "config": req.dict()}
        save_registry()
        return {"id": agent_id}
    except Exception as e:
        return {"error": str(e)}

@app.post("/forge/execute_sequential")
async def execute_sequential(req: MultiTaskRequest):
    full_mission_log = []
    current_team_context = ""

    for idx, agent_id in enumerate(req.agent_ids):
        agent = active_agents.get(agent_id)
        if not agent: continue

        # Oprava: Použití system a prompt parametrů pro stabilitu
        payload = {
            "model": OLLAMA_MODEL,
            "system": f"You are {agent['config']['name']}, a professional {agent['config']['role']}. Provide technical and direct answers.",
            "prompt": f"MISSION OBJECTIVE: {req.prompt}\nPROGRESS SO FAR: {current_team_context}\nYOUR TASK: Contribute to the objective from your role's perspective.",
            "stream": False,
            "options": {
                "num_predict": 300,
                "temperature": 0.3
            }
        }

        output = ""
        try:
            # Retry logika (3 pokusy)
            for attempt in range(3):
                res = requests.post(OLLAMA_URL, json=payload, timeout=180)
                if res.status_code == 200:
                    output = res.json().get("response", "").strip()
                    if output: break
                time.sleep(2)

            if not output:
                output = "SYSTEM ERROR: Unit failed to respond after 3 attempts."
            
            current_team_context += f"\n[{agent['config']['name']}]: {output}\n"
            full_mission_log.append({"agent": agent['config']['name'], "output": output})
            
        except Exception as e:
            full_mission_log.append({"agent": agent['config']['name'], "output": f"CRITICAL FAILURE: {str(e)}"})

    return {"mission_results": full_mission_log}

@app.post("/forge/terminal")
async def terminal_cmd(agent_id: str, command: str):
    agent = active_agents.get(agent_id)
    if not agent: return {"output": "Agent not found."}
    try:
        c = client.containers.get(agent["container"])
        r = c.exec_run(f"sh -c \"{command}\"")
        return {"output": r.output.decode('utf-8') or "Command executed."}
    except Exception as e:
        return {"output": f"Shell Error: {str(e)}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)