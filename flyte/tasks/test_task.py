from loguru import logger
from flytekit import task


@task
def test_task(repo_path: str) -> str:
    """Simple Flyte task to simulate running unit tests."""
    logger.info(f"Running tests on repo at {repo_path}")
    # Placeholder for actual test execution
    return "ok"
