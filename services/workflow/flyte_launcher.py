from datetime import datetime
from pathlib import Path
from typing import Tuple

from flytekit import task, workflow
from git import Repo
from logging_config import logger

from services.ai_agent import generate_patch
from services.git_ops import slugify


@task
def clone_repository(repo_url: str, goal: str) -> Tuple[str, str]:
    """Clone the repository and create a new feature branch."""
    workspace = Path("/tmp/flyte_agent")
    workspace.mkdir(parents=True, exist_ok=True)
    repo_name = repo_url.rstrip("/").split("/")[-1].replace(".git", "")
    repo_path = workspace / repo_name
    try:
        if repo_path.exists():
            logger.info(f"Repository already exists at {repo_path}, fetching updates")
            repo = Repo(repo_path)
            repo.remote().fetch()
        else:
            logger.info(f"Cloning {repo_url} to {repo_path}")
            repo = Repo.clone_from(repo_url, repo_path)
        slug = slugify(goal)[:20]
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        branch_name = f"feat/{slug}-{timestamp}"
        repo.git.checkout('-b', branch_name)
        logger.info(f"Created branch {branch_name}")
    except Exception as exc:
        logger.error(f"Failed to clone repository: {exc}")
        raise
    return str(repo_path), branch_name


@task
def generate_patch_from_goal(repo_path: str, goal: str) -> str:
    """Call the LLM to generate a raw git patch."""
    prompt = (
        "Vous êtes un assistant IA qui modifie le dépôt pour l'objectif suivant : "
        f"{goal}. Fournis uniquement le diff git à appliquer."
    )
    try:
        patch = generate_patch(prompt)
        logger.info("Generated patch from goal")
    except Exception as exc:
        logger.error(f"Failed to generate patch: {exc}")
        raise
    return patch


@task
def validate_patch(repo_path: str, patch: str) -> Tuple[bool, str]:
    """Validate the patch using git apply --check."""
    patch_file = Path(repo_path) / "tmp.patch"
    patch_file.write_text(patch)
    repo = Repo(repo_path)
    try:
        repo.git.apply("--check", str(patch_file))
        logger.info("Patch validated successfully")
        valid, message = True, "Patch valid"
    except Exception as exc:
        logger.error(f"Patch validation failed: {exc}")
        valid, message = False, str(exc)
    finally:
        patch_file.unlink(missing_ok=True)
    return valid, message


@task
def apply_patch(repo_path: str, patch: str, valid: bool) -> str:
    """Apply the patch if validation succeeded."""
    if not valid:
        logger.error("Patch invalid, aborting apply")
        raise ValueError("Invalid patch")
    patch_file = Path(repo_path) / "tmp.patch"
    patch_file.write_text(patch)
    repo = Repo(repo_path)
    try:
        repo.git.apply(str(patch_file))
        logger.info("Applied patch to repository")
    finally:
        patch_file.unlink(missing_ok=True)
    return repo_path


@task
def commit_and_push_changes(repo_path: str, branch_name: str, message: str) -> str:
    """Commit the applied patch and push to remote."""
    repo = Repo(repo_path)
    repo.git.add(all=True)
    if repo.is_dirty():
        repo.index.commit(message)
        logger.info("Committed changes")
    else:
        logger.info("No changes to commit")
    try:
        repo.git.push("-u", "origin", branch_name)
        logger.info(f"Pushed branch {branch_name}")
    except Exception as exc:
        logger.error(f"Failed to push branch: {exc}")
        raise
    return branch_name


@workflow
def agent_code_generation_pipeline(repo_url: str, goal: str) -> str:
    repo_path, branch_name = clone_repository(repo_url=repo_url, goal=goal)
    patch = generate_patch_from_goal(repo_path=repo_path, goal=goal)
    valid, _ = validate_patch(repo_path=repo_path, patch=patch)
    apply_patch(repo_path=repo_path, patch=patch, valid=valid)
    commit_and_push_changes(repo_path=repo_path, branch_name=branch_name, message=goal)
    return branch_name


def launch_agent_workflow(repo_url: str, goal: str) -> str:
    """Helper to execute the Flyte workflow locally."""
    return agent_code_generation_pipeline(repo_url=repo_url, goal=goal)

