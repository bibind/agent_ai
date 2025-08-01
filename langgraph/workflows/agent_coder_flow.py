"""Minimal LangGraph flow orchestrating repository modifications."""
from langgraph.graph import END, StateGraph
from loguru import logger
from services.git_ops import create_branch, commit_all, push_branch
from services.ai_agent import generate_patch
from services.code_analyzer import write_file
from pathlib import Path
from sandbox.runner import run_script


def build_flow():
    workflow = StateGraph(dict)

    def start(state: dict) -> dict:
        repo = state["repo"]
        goal = state["goal"]
        branch = create_branch(repo, goal)
        state["branch"] = branch
        return state

    def generate(state: dict) -> dict:
        repo = state["repo"]
        prompt = state.get("prompt", state["goal"])
        patch = generate_patch(prompt)
        file_path = state.get("file_path")
        if file_path:
            write_file(Path(repo.working_tree_dir), file_path, patch)
        state["patch"] = patch
        return state

    def validate(state: dict) -> dict:
        repo = state["repo"]
        run_script("pytest", cwd=repo.working_tree_dir)
        return state

    def finalize(state: dict) -> dict:
        repo = state["repo"]
        branch = state["branch"]
        commit_all(repo, state.get("goal", "update"))
        push_branch(repo, branch)
        return state

    workflow.add_state("start", start)
    workflow.add_state("generate", generate)
    workflow.add_state("validate", validate)
    workflow.add_state("finalize", finalize)

    workflow.set_entry_point("start")
    workflow.add_edge("start", "generate")
    workflow.add_edge("generate", "validate")
    workflow.add_edge("validate", "finalize")
    workflow.add_edge("finalize", END)

    return workflow.compile()
