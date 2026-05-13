# 🌌 NexusForge AI: Kompletní instalační příručka

NexusForge je orchestrátor pro týmy AI agentů běžících v izolovaných Docker kontejnerech. Tento návod tě provede kompletním nastavením od nuly.

---

## 🛠️ KROK 1: Instalace Dockeru

Docker je nezbytný pro izolaci agentů. Každý tvůj agent "žije" ve vlastním malém Linuxu.

### Windows
1. Stáhni si **[Docker Desktop](https://www.docker.com/products/docker-desktop/)**.
2. Při instalaci se ujisti, že je zaškrtnuto **"Use WSL 2 instead of Hyper-V"** (doporučeno).
3. Po restartu PC spusť Docker Desktop a počkej, až ikona v liště zezelená.

### Linux (Ubuntu)
Spusť v terminálu:
```bash
sudo apt update && sudo apt install docker.io -y
sudo systemctl start docker
sudo usermod -aG docker $USER
(Poté se odhlaste a přihlaste, aby se projevila práva.)

🧠 KROK 2: Nastavení Ollama (Mozek AI)
Ollama běží lokálně a poskytuje modely, které NexusForge používá.

Stáhni si Ollama z ollama.com.

Nainstaluj ji a ujisti se, že běží (uvidíš ikonu lamy v liště).

Stažení modelů: Otevři svůj terminál (CMD nebo PowerShell) a stáhni modely:

Bash
# Hlavní model pro uvažování (povinné)
ollama pull llama3

# Volitelný: Skvělý model pro programování
ollama pull deepseek-coder
⚠️ Důležité nastavení pro NexusForge
Pokud tvůj backend neběží na stejném stroji jako Ollama (nebo máš problémy s připojením), musíš povolit externí přístup nastavením proměnné prostředí:

Windows: Nastavení -> Systém -> O systému -> Upřesnit nastavení systému -> Proměnné prostředí -> Nová: OLLAMA_ORIGINS s hodnotou *.

Poté restartuj aplikaci Ollama.

🏗️ KROK 3: Příprava prostředí NexusForge
Klonování repozitáře:

Bash
git clone [https://github.com/20player11/Nexus-Forge-AI.git](https://github.com/20player11/Nexus-Forge-AI.git)
cd Nexus-Forge-AI


2. **Instalace Python závislostí**:
   Ujisti se, že máš Python 3.10 nebo novější.
   ```bash
   cd backend
   pip install fastapi uvicorn docker requests pydantic
   
🚀 KROK 4: Spuštění systému
1. Spuštění Backend serveru
V terminálu ve složce backend spusť:

Bash
python main.py
Měl bys vidět: INFO: Uvicorn running on http://127.0.0.1:8000. Backend se automaticky pokusí spojit s Dockerem a najít existující agenty.

2. Spuštění Frontendu
Jednoduše najdi soubor frontend/index.html a otevři ho v libovolném moderním prohlížeči (Chrome, Edge, Brave).

🎮 Jak používat NexusForge
Deploy Unit: Klikni na tlačítko "DEPLOY NEW UNIT". Zadej jméno (např. Coder_Alpha) a roli (např. Python Expert).

Výběr agentů: Zaškrtni checkboxy u agentů, které chceš zapojit do mise.

Mission Briefing: Do velkého textového pole napiš úkol, např.: "Vytvořte jednoduchou kalkulačku v Pythonu a otestujte ji."

Execute: Klikni na "INITIATE PROTOCOL". Sleduj, jak si agenti předávají informace.

💡 Doporučené modely
V souboru backend/main.py můžeš změnit proměnnou OLLAMA_MODEL na:

llama3: Nejlepší balanc mezi rychlostí a inteligencí (8B verze).

mistral: Velmi rychlý a efektivní model.

phi3: Extrémně lehký model, pokud máš slabší PC / málo VRAM.

🛠️ Odstraňování problémů (Troubleshooting)
"Agent remained silent": Ollama pravděpodobně ještě načítá model do paměti. Zkus poslat požadavek znovu nebo zkontroluj v terminálu ollama list, zda je model správně stažený.

Docker Error: Ujisti se, že Docker Desktop běží. Pokud jsi na Windows, zkontroluj, zda máš zapnutou virtualizaci v BIOSu.

CORS Error: Pokud se frontend nemůže spojit s backendem, ujisti se, že v main.py je správně nastaven allow_origins=["*"].
