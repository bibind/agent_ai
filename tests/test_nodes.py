from pathlib import Path
from git import Repo
from nodes.classify_intent import ClassifyIntent
from nodes.apply_changes import ApplyChanges
from nodes.commit_and_push import CommitAndPush
from nodes.explore_repo import ExploreRepo
from nodes.generate_plan import GeneratePlan
from nodes.generate_code import GenerateCode
from nodes.validate import Validate

class DummyLLM:
    def __init__(self, response: str = ""):
        self.response = response
    def invoke(self, msg):
        class M:
            content = self.response
        return M()

def init_repo(path: Path) -> Repo:
    repo = Repo.init(path)
    (path / "README.md").write_text("init")
    repo.git.add(all=True)
    repo.index.commit("init")
    return repo

def test_classify_intent():
    node = ClassifyIntent()
    ctx = node.run({"goal": "Corriger un bug"})
    assert ctx["intent"] == "bugfix"


def test_apply_changes(tmp_path):
    repo = init_repo(tmp_path)
    file = tmp_path / "file.txt"
    file.write_text("a\n")
    repo.git.add(all=True)
    repo.index.commit("add file")
    diff = repo.git.diff('HEAD')
    patch = f"--- a/file.txt\n+++ b/file.txt\n@@\n-a\n+b\n"
    node = ApplyChanges()
    ctx = {"repo": repo, "repo_path": str(tmp_path), "generated_patch": patch}
    result = node.run(ctx)
    assert "apply_error" not in result
    assert file.read_text() == "b\n"


def test_commit_and_push(tmp_path):
    repo = init_repo(tmp_path / "src")
    bare = Repo.init(tmp_path / "remote", bare=True)
    repo.create_remote('origin', str(bare.working_tree_dir))
    branch = repo.active_branch.name
    node = CommitAndPush("msg")
    ctx = {"repo": repo, "branch_name": branch}
    result = node.run(ctx)
    assert bare.refs[branch].commit.hexsha == repo.head.commit.hexsha


def test_explore_repo(tmp_path):
    src = init_repo(tmp_path / "src")
    node = ExploreRepo(str(src.working_tree_dir))
    ctx = node.run({"goal": "Test"})
    assert Path(ctx["repo_path"]).exists()
    assert ctx["branch_name"].startswith("feat/")
    assert len(ctx["repo_files"]) > 0


def test_generate_plan():
    node = GeneratePlan()
    ctx = node.run({"goal": "Anything"})
    assert len(ctx["plan"]) == 4


def test_generate_code(monkeypatch):
    monkeypatch.setattr('services.ai_agent.get_chat_model', lambda model=None: DummyLLM("patch"))
    node = GenerateCode()
    ctx = node.run({"goal": "change"})
    assert ctx["generated_patch"] == "patch"


def test_validate(tmp_path):
    repo = init_repo(tmp_path)
    node = Validate()
    ctx = node.run({"repo_path": str(tmp_path)})
    assert ctx["validation_result"] == "success"
