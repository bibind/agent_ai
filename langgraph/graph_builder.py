"""Utility to build agent workflows using a simple state graph."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field, fields, replace
from typing import Callable, Dict, List, Optional, cast

from loguru import logger

from nodes.classify_intent import ClassifyIntent
from nodes.explore_repo import ExploreRepo
from nodes.generate_plan import GeneratePlan
from nodes.generate_code import GenerateCode
from nodes.apply_changes import ApplyChanges
from nodes.validate import Validate
from nodes.commit_and_push import CommitAndPush
from nodes import NodeContext

try:  # Try to import the real LangGraph library
    from langgraph.graph import END, StateGraph  # type: ignore
except Exception:  # pragma: no cover - fallback minimal implementation
    END = "__end__"

    class StateGraph:  # minimal fallback used only for tests
        def __init__(self, state_type: type):
            self.state_type = state_type
            self.states: Dict[str, Callable[[object], object]] = {}
            self.edges: Dict[str, List[str]] = {}
            self.entry: Optional[str] = None

        def add_state(self, name: str, fn: Callable[[object], object]) -> None:
            self.states[name] = fn

        def add_edge(self, start: str, end: str) -> None:
            self.edges.setdefault(start, []).append(end)

        def set_entry_point(self, name: str) -> None:
            self.entry = name

        def compile(self):
            states = self.states
            edges = self.edges
            entry = self.entry

            class Flow:
                def invoke(self, state: object) -> object:
                    current = entry
                    while current and current != END:
                        fn = states[current]
                        state = fn(state)
                        next_nodes = edges.get(current)
                        current = next_nodes[0] if next_nodes else END
                    return state

            return Flow()


@dataclass
class AgentState:
    """Shared state passed between workflow nodes."""

    goal: str
    repo: Optional[object] = None
    repo_path: Optional[str] = None
    branch_name: Optional[str] = None
    intent: Optional[str] = None
    plan: List[str] = field(default_factory=list)
    generated_patch: Optional[str] = None
    patch_error: Optional[str] = None
    apply_error: Optional[str] = None
    validation_result: Optional[str] = None


class GraphBuilder:
    """Build and run an agent workflow based on ``StateGraph``."""

    def __init__(self, repo_url: str, goal: str, use_openai: bool = False) -> None:
        self.repo_url = repo_url
        self.goal = goal
        self.use_openai = use_openai
        self.workflow: StateGraph = StateGraph(AgentState)
        self._states: List[str] = []
        self._entry_defined = False

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def add_state(self, name: str, func: Callable[[AgentState], AgentState]) -> None:
        """Register a new state in the workflow."""
        self.workflow.add_state(name, func)
        self._states.append(name)
        if not self._entry_defined:
            self.workflow.set_entry_point(name)
            self._entry_defined = True

    def add_edge(self, start: str, end: str) -> None:
        """Create a transition between two states."""
        self.workflow.add_edge(start, end)

    def set_entry_point(self, name: str) -> None:
        self.workflow.set_entry_point(name)
        self._entry_defined = True

    # ------------------------------------------------------------------
    def _wrap_node(self, node: object) -> Callable[[AgentState], AgentState]:
        def _runner(state: AgentState) -> AgentState:
            context = cast(NodeContext, asdict(state))
            updated = node.run(context)
            field_names = {f.name for f in fields(AgentState)}
            state = replace(
                state, **{k: v for k, v in updated.items() if k in field_names}
            )
            for key, value in updated.items():
                if key not in field_names:
                    setattr(state, key, value)
            return state

        return _runner

    def _build_default(self) -> None:
        """Populate the workflow with a default linear sequence."""

        steps = [
            ("classify_intent", ClassifyIntent()),
            ("explore_repo", ExploreRepo(self.repo_url)),
            ("generate_plan", GeneratePlan()),
            ("generate_code", GenerateCode(use_openai=self.use_openai)),
            ("apply_changes", ApplyChanges()),
            ("validate", Validate()),
            ("commit_and_push", CommitAndPush(commit_message=self.goal)),
        ]

        for name, node in steps:
            self.add_state(name, self._wrap_node(node))

        for start, end in zip(self._states, self._states[1:]):
            self.add_edge(start, end)
        self.add_edge(self._states[-1], END)

    def compile(self):
        if not self._states:
            self._build_default()
        return self.workflow.compile()

    def run(self) -> AgentState:
        """Execute the workflow and return the final ``AgentState``."""

        state = AgentState(goal=self.goal)
        flow = self.compile()
        if hasattr(flow, "invoke"):
            result = flow.invoke(state)
        else:
            result = flow(state)
        logger.info("Workflow finished")
        return result
