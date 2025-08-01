#!/usr/bin/env python
import argparse
from loguru import logger
from langgraph.graph_builder import GraphBuilder


def main():
    parser = argparse.ArgumentParser(description="Agent IA pour l'orchestration de dev")
    parser.add_argument("--repo_url", required=True, help="URL du dépôt Git")
    parser.add_argument("--goal", required=True, help="Objectif de l'agent")
    parser.add_argument("--use_openai", action="store_true", help="Utiliser OpenAI au lieu d'Ollama")
    args = parser.parse_args()

    logger.add(lambda msg: print(msg, end=""))
    builder = GraphBuilder(repo_url=args.repo_url, goal=args.goal, use_openai=args.use_openai)
    result = builder.run()
    logger.info("Résumé final:")
    logger.info(result)


if __name__ == "__main__":
    main()
