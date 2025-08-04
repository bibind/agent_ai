# Makefile to ensure Docker is installed and run project setup scripts
# Targets:
#   check-docker   Vérifie si Docker est installé.
#   install-docker Installe Docker si nécessaire.
#   setup          Exécute les scripts de configuration.
#   all            Cible principale : installe Docker et lance setup.

.PHONY: check-docker install-docker setup all

# Liste des scripts de configuration à exécuter
SETUP_SCRIPTS := setup.sh

check-docker:
	@if command -v docker >/dev/null 2>&1; then \
		echo "Docker est déjà installé."; \
	else \
		echo "Docker n'est pas installé."; \
		exit 1; \
	fi

install-docker:
	@if command -v docker >/dev/null 2>&1; then \
		echo "Docker est déjà installé."; \
	else \
		echo "Installation de Docker..."; \
		curl -fsSL https://get.docker.com -o get-docker.sh; \
		sh get-docker.sh; \
		rm get-docker.sh; \
		echo "Docker a été installé."; \
	fi

setup: check-docker
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

all: install-docker setup
	@echo "Installation complète.";
