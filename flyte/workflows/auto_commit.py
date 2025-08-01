"""Example Flyte workflow executed after a commit."""
from flytekit import task, workflow
from loguru import logger
from pathlib import Path


@task
def build(repo_path: str) -> str:
    logger.info(f"Running build for {repo_path}")
    return "built"


@workflow
def auto_commit_workflow(repo_path: str) -> str:
    return build(repo_path=repo_path)
