from logging_config import logger
from flytekit import task, workflow
from pathlib import Path
import subprocess

from . import NodeContext


@task
def run_tests(repo_path: str) -> dict:
    """Run pytest in the given repository and save the report."""
    logger.info(f"Running tests in {repo_path}")
    report_path = Path(repo_path) / "pytest_report.txt"
    result = subprocess.run(
        ["pytest", "-q"], cwd=repo_path, capture_output=True, text=True
    )
    report_path.write_text(result.stdout + result.stderr)
    status = "success" if result.returncode == 0 else "failure"
    return {"status": status, "report": str(report_path)}


@workflow
def validation_workflow(repo_path: str) -> dict:
    return run_tests(repo_path=repo_path)


class Validate:
    """Run Flyte validation workflow."""

    def run(self, context: NodeContext) -> NodeContext:
        repo_path = context["repo_path"]
        logger.info("Starting Flyte validation workflow")
        result = validation_workflow(repo_path=repo_path)
        context["validation_result"] = result
        logger.info(f"Validation result: {result}")
        return context
