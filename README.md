# 🌌 NexusForge AI: Phase 2

NexusForge je experimentální platforma pro **sekvenční orchestraci AI agentů** v izolovaných Docker kontejnerech. Umožňuje vytvářet "Hive Mind" týmy, kde agenti pracují jeden po druhém a předávají si výsledky skrze sdílený kontext.

## ✨ Klíčové vlastnosti
- **Sequential Execution**: Agenti pracují v řadě, což šetří VRAM a zajišťuje kontinuitu.
- **Docker Isolation**: Každý agent má své vlastní bezpečné prostředí (Alpine Linux).
- **Persistent Memory**: Agenti si pamatují svá jména a role i po restartu backendu.
- **Minimalist UI**: Moderní "Cyberpunk" rozhraní pro kontrolu mise v reálném čase.

## 🚀 Rychlý start
1. **Předpoklady**: Nainstalovaný [Docker](https://www.docker.com/) a [Ollama](https://ollama.ai/).
2. **Backend**: 
   ```bash
   cd backend
   pip install -r requirements.txt
   python main.py

Frontend: Stačí otevřít frontend/index.html v prohlížeči.

## 🛠️ Technologie
Backend: Python (FastAPI)

AI: Ollama (Llama3 / DeepSeek)

Virtualizace: Docker SDK for Python

Frontend: Vanilla JS & CSS
