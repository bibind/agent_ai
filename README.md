# Agent IA

Ce projet fournit un exemple minimal d'agent autonome capable de modifier un dépôt Git et une petite interface web pour explorer les fichiers. Il nécessite Python 3.10 ou plus.

## 🔧 Pré-requis système
- Python >= 3.10 installé
- Git
- (optionnel) [Ollama](https://ollama.ai) pour utiliser un modèle local

## 🚀 Installation locale pas à pas
1. Clonez ce dépôt et placez-vous dedans.
2. Exécutez `./setup.sh` qui crée l'environnement virtuel `.venv` et installe les dépendances depuis `requirements.txt`.
3. Copiez éventuellement un fichier `.env` à la racine pour renseigner vos variables (voir plus bas).

## 🧪 Lancement du projet
```bash
source .venv/bin/activate
python main.py --repo_url <URL_DU_DEPOT> --goal "Votre objectif" [--use_openai]
```
Cela exécute l'agent en mode CLI. Pour lancer l'interface web :
```bash
uvicorn web_ui.main:app --reload
```

## 📂 Structure du dépôt
- `agent_ia.py` : script principal de l'agent
- `main.py` : point d'entrée simplifié appelant `agent_ia.py`
- `services/` : opérations Git et appels LLM
- `nodes/` : étapes de l'agent
- `langgraph/` : orchestration du workflow
- `flyte/` : exemples de tâches Flyte
- `web_ui/` : mini interface FastAPI

## 🤖 Utilisation du CLI / Agent IA
```bash
python main.py --repo_url <url> --goal "Ajouter une fonctionnalité" [--use_openai]
```
- `--repo_url` : dépôt Git cible
- `--goal` : objectif en langage naturel
- `--use_openai` : forcer l'utilisation de l'API OpenAI (sinon Ollama)

## 💬 Configuration de l’API Key OpenAI
L'agent lit la clé API depuis la variable d'environnement `OPENAI_API_KEY`. Vous pouvez aussi définir :
- `AI_MODEL` pour indiquer un modèle Ollama (ex. `llama2`)
- `OLLAMA_BASE_URL` si Ollama n'utilise pas l'URL par défaut
- `GIT_REPO_PATH` ou `REPO_PATH` pour cibler un dépôt local dans l'interface web

Placez ces variables dans un fichier `.env` et elles seront chargées par `setup.sh` lors de l'installation.

## 🐛 Dépannage courant
- Vérifiez que la version de Python utilisée dans `.venv` est ≥ 3.10
- Assurez-vous que `OPENAI_API_KEY` est valide si vous utilisez OpenAI
- Utilisez `--use_openai` uniquement si le paquet `openai` est installé et la clef configurée


