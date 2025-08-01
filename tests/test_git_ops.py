import os
from pathlib import Path
from git import Repo
import pytest

from services.git_ops import create_branch, commit_all, repo_diff


def init_repo(path: Path) -> Repo:
    repo = Repo.init(path)
    (path / "README.md").write_text("init")
    repo.git.add(all=True)
    repo.index.commit("init")
    return repo


def test_create_branch(tmp_path):
    repo = init_repo(tmp_path)
    branch = create_branch(repo, "Add feature")
    assert repo.active_branch.name == branch
    assert branch.startswith("feat/")


def test_commit_all_and_diff(tmp_path):
    repo = init_repo(tmp_path)
    (tmp_path / "file.txt").write_text("change")
    commit_all(repo, "update")
    assert repo.head.commit.message.strip() == "update"
    assert repo_diff(repo) == ""
    (tmp_path / "file.txt").write_text("new change")
    assert repo_diff(repo) != ""
