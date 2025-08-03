from pathlib import Path

from git import Repo


def init_repo(path: Path, default_branch: str = "main") -> Repo:
    repo = Repo.init(path, initial_branch=default_branch)
    (path / "README.md").write_text("init")
    repo.git.add(all=True)
    repo.index.commit("init")
    return repo

