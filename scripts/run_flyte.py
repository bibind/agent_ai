import argparse
import os
from loguru import logger

from services.workflow.flyte_launcher import launch_agent_workflow


def main():
    parser = argparse.ArgumentParser(description="Run Flyte agent workflow")
    parser.add_argument("--repo_url", required=True, help="Git repository URL")
    parser.add_argument("--goal", required=True, help="Goal for the agent")
    default_level = os.environ.get("LOG_LEVEL", "INFO")
    parser.add_argument(
        "--log_level",
        default=default_level,
        help="Logging level",
    )
    args = parser.parse_args()

    logger.remove()
    logger.add(lambda msg: print(msg, end=""), level=args.log_level)
    log_file = os.environ.get("LOG_FILE", "agent.log")
    logger.add(log_file, level=args.log_level, rotation="1 MB")
    result = launch_agent_workflow(repo_url=args.repo_url, goal=args.goal)
    logger.info(f"Workflow finished. Branch: {result}")


if __name__ == "__main__":
    main()

