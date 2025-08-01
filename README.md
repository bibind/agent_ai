# Agent IA pour le développement

Ce dépôt contient un exemple minimal d'agent autonome capable d'orchestrer
plusieurs tâches pour modifier automatiquement un dépôt Git. Il a été pensé
comme démonstrateur pour l'automatisation des workflows de développement.

Une interface Web simple basée sur **FastAPI** est fournie dans `web_ui/` pour
explorer un dépôt, éditer des fichiers et déclencher une génération de code par
IA. Les actions Git (création de branche, commit, push) sont réalisées via les
services présents dans `services/` et orchestrées par un exemple de workflow
`langgraph/workflows/agent_coder_flow.py`.

## Fonctionnalités principales

- **Classification d'intention** : détermine le type de tâche (bugfix,
  documentation, feature ou chore) à partir de l'objectif fourni.
- **Exploration de dépôt** : clone le dépôt indiqué et crée une branche dédiée.
- **Génération de plan** : produit un plan simple des étapes à exécuter.
- **Génération de code** : utilise un LLM (OpenAI ou modèle local via Ollama)
  pour générer un patch à appliquer au dépôt.
- **Application des changements** : applique le diff généré.
- **Validation Flyte** : exécute un workflow Flyte minimal pour simuler les
  tests.
- **Commit et push** : valide les modifications et pousse la branche distante.

L'orchestration de ces étapes est réalisée par `GraphBuilder` dans
`langgraph/graph_builder.py`.

## Installation

Ce projet nécessite Python 3.10 ou plus ainsi que quelques dépendances :
`loguru`, `GitPython`, `langchain` et `flytekit`. Installez-les par exemple avec :

```bash
pip install loguru GitPython langchain flytekit
```

Si vous souhaitez utiliser OpenAI pour la génération de code, assurez-vous que
la variable d'environnement `OPENAI_API_KEY` est définie.

## Utilisation

L'agent principal se lance via le script `agent_ia.py` :

```bash
python agent_ia.py --repo_url <URL_DU_DEPOT> --goal "Votre objectif" [--use_openai]
```

- `--repo_url` : URL du dépôt Git à modifier.
- `--goal` : objectif exprimé en langage naturel.
- `--use_openai` : optionnel, utilise l'API OpenAI au lieu d'un modèle local.

Le script crée une branche `feat/<slug>-<timestamp>` dans un workspace temporaire
(`/tmp/agent_workspace`), applique les changements générés puis pousse la
branche sur le dépôt distant.

## Organisation du code

- `agent_ia.py` : point d'entrée de l'agent.
- `langgraph/graph_builder.py` : enchaîne les différentes étapes (nodes).
- `nodes/` : contient chaque action de l'agent (classification, exploration,
  génération de code, validation, etc.).
- `flyte/` : exemple de tâche Flyte utilisée pour simuler la phase de test.

## Exemple de workflow

1. L'agent classe l'intention à partir de l'objectif.
2. Il clone le dépôt et crée une branche.
3. Un plan simplifié est généré.
4. Un diff est produit par LLM et appliqué au dépôt.
5. Le workflow Flyte valide les modifications.
6. Les changements sont commités puis poussés.

Ce dépôt fournit un squelette léger pour expérimenter la mise en place d'agents
IA capables d'automatiser des tâches de développement.

## Interface Web

Exécutez l'application FastAPI pour parcourir et modifier localement le dépôt :

```bash
uvicorn web_ui.main:app --reload
```

Par défaut, le chemin du dépôt est celui du projet courant. Définissez la
variable `REPO_PATH` pour cibler un autre répertoire.
