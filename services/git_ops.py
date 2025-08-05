from git import Repo
from pathlib import Path
from logging_config import logger
from datetime import datetime
import re


class GitOpsError(Exception):
    """Base exception for git operations."""


class BranchCreationError(GitOpsError):
    """Raised when branch creation fails."""


class PushError(GitOpsError):
    """Raised when pushing to remote fails."""


def open_repo(path: str) -> Repo:
    return Repo(path)


def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def create_branch(repo: Repo, goal: str) -> str:
    slug = slugify(goal)[:20]
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    branch_name = f"feat/{slug}-{timestamp}"
    try:
        repo.git.checkout('-b', branch_name)
        logger.info(f"Created branch {branch_name}")
    except Exception as exc:
        raise BranchCreationError(f"Could not create branch {branch_name}: {exc}") from exc
    return branch_name


def commit_all(repo: Repo, message: str):
    repo.git.add(all=True)
    if repo.is_dirty():
        repo.index.commit(message)
        logger.info("Committed changes")


def push_branch(repo: Repo, branch_name: str):
    try:
        repo.git.push("-u", "origin", branch_name)
        logger.info("Pushed branch")
    except Exception as exc:
        raise PushError(f"Failed to push: {exc}") from exc


def repo_diff(repo: Repo) -> str:
    return repo.git.diff('HEAD')
