# Makefile to ensure Docker is installed and run project setup scripts

.PHONY: check-docker install-docker setup all deploy-flyte run-example help

# Liste des scripts de configuration à exécuter
SETUP_SCRIPTS := setup.sh

check-docker: ## Vérifie si Docker est installé.
	@if command -v docker >/dev/null 2>&1; then \
	echo "Docker est déjà installé."; \
	else \
	echo "Docker n'est pas installé."; \
	exit 1; \
	fi

install-docker: ## Installe Docker si nécessaire.
	@if command -v docker >/dev/null 2>&1; then \
	echo "Docker est déjà installé."; \
	else \
	echo "Installation de Docker..."; \
	curl -fsSL https://get.docker.com -o get-docker.sh; \
	sh get-docker.sh; \
	rm get-docker.sh; \
	echo "Docker a été installé."; \
	fi

setup: check-docker ## Exécute les scripts de configuration.
	@echo "Exécution des scripts de configuration..."; \
	for script in $(SETUP_SCRIPTS); do \
	if [ -f $$script ]; then \
	echo "Lancement de $$script"; \
	chmod +x $$script; \
	./$$script; \
	else \
	echo "Script $$script introuvable"; \
	fi; \
	done

all: install-docker setup ## Cible principale : installe Docker et lance setup.
	@echo "Installation complète.";

deploy-flyte: ## Enregistre les workflows Flyte.
	./scripts/deploy_flyte.sh

run-example: ## Exécute un exemple de workflow avec pyflyte.
	pyflyte run flyte/workflows/auto_commit.py auto_commit_workflow --repo_path /chemin/du/repo


help: ## Affiche cette aide.
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
