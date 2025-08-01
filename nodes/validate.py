from loguru import logger
from flytekit import task, workflow


@task
def run_tests(repo_path: str) -> str:
    # Placeholder for real validation commands
    logger.info(f"Running tests in {repo_path}")
    return "success"


@workflow
def validation_workflow(repo_path: str) -> str:
    return run_tests(repo_path=repo_path)


class Validate:
    """Run Flyte validation workflow."""

    def run(self, context: dict) -> dict:
        repo_path = context["repo_path"]
        logger.info("Starting Flyte validation workflow")
        result = validation_workflow(repo_path=repo_path)
        context["validation_result"] = result
        logger.info(f"Validation result: {result}")
        return context
