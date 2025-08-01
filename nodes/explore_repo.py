import re
from datetime import datetime
from pathlib import Path
from git import Repo
from loguru import logger


def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


class ExploreRepo:
    """Clone the repository and create a feature branch."""

    def __init__(self, repo_url: str):
        self.repo_url = repo_url

    def run(self, context: dict) -> dict:
        goal = context.get("goal", "goal")
        workspace = Path("/tmp/agent_workspace")
        workspace.mkdir(parents=True, exist_ok=True)
        repo_name = self.repo_url.rstrip("/").split("/")[-1].replace(".git", "")
        repo_path = workspace / repo_name
        if repo_path.exists():
            logger.info(
                f"Repository already exists at {repo_path}, fetching updates"
            )
            repo = Repo(repo_path)
            repo.remote().fetch()
        else:
            logger.info(f"Cloning {self.repo_url} to {repo_path}")
            repo = Repo.clone_from(self.repo_url, repo_path)
        slug = slugify(goal)[:20]
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        branch_name = f"feat/{slug}-{timestamp}"
        repo.git.checkout('-b', branch_name)
        file_list = [
            str(p.relative_to(repo_path))
            for p in repo_path.rglob("*")
            if p.is_file()
        ]
        context.update(
            {
                "repo": repo,
                "repo_path": str(repo_path),
                "branch_name": branch_name,
                "repo_files": file_list,
            }
        )
        logger.info(f"Created branch {branch_name}")
        logger.info(f"Repository contains {len(file_list)} files")
        return context
