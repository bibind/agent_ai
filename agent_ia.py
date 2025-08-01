#!/usr/bin/env python
import argparse
import os
import sys
from loguru import logger
from langgraph.graph_builder import GraphBuilder


def main():
    parser = argparse.ArgumentParser(description="Agent IA pour l'orchestration de dev")
    parser.add_argument("--repo_url", required=True, help="URL du dépôt Git")
    parser.add_argument("--goal", required=True, help="Objectif de l'agent")
    parser.add_argument("--use_openai", action="store_true", help="Utiliser OpenAI au lieu d'Ollama")
    default_level = os.environ.get("LOG_LEVEL", "INFO")
    parser.add_argument(
        "--log_level",
        default=default_level,
        help="Niveau de log Loguru (DEBUG, INFO, WARNING, ...)",
    )
    args = parser.parse_args()

    logger.remove()
    logger.add(lambda msg: print(msg, end=""), level=args.log_level)
    log_file = os.environ.get("LOG_FILE", "agent.log")
    logger.add(log_file, level=args.log_level, rotation="1 MB")
    builder = GraphBuilder(repo_url=args.repo_url, goal=args.goal, use_openai=args.use_openai)
    try:
        result = builder.run()
        logger.info("Résumé final:")
        logger.info(result)
    except Exception as exc:
        logger.exception(f"Execution failed: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
