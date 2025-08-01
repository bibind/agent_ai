import argparse
from loguru import logger

from services.workflow.flyte_launcher import launch_agent_workflow


def main():
    parser = argparse.ArgumentParser(description="Run Flyte agent workflow")
    parser.add_argument("--repo_url", required=True, help="Git repository URL")
    parser.add_argument("--goal", required=True, help="Goal for the agent")
    args = parser.parse_args()

    logger.add(lambda msg: print(msg, end=""))
    result = launch_agent_workflow(repo_url=args.repo_url, goal=args.goal)
    logger.info(f"Workflow finished. Branch: {result}")


if __name__ == "__main__":
    main()

