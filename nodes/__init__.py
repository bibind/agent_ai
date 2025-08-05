"""Shared types and utilities for node implementations."""

from __future__ import annotations

from typing import List, TypedDict

from git import Repo


class NodeContext(TypedDict, total=False):
    """Typed dictionary passed between workflow nodes."""

    goal: str
    repo: Repo
    repo_path: str
    branch_name: str
    repo_files: List[str]
    intent: str
    plan: List[str]
    generated_patch: str
    patch_error: str
    apply_error: str
    validation_result: str
    push_error: str


__all__ = ["NodeContext"]

