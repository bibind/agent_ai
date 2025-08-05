from langgraph.graph_builder import GraphBuilder, END


class DummyLLM:
    def invoke(self, msg):
        class M:
            content = ""

        return M()


def test_default_states_and_transitions(monkeypatch):
    monkeypatch.setattr(
        "nodes.generate_code.get_chat_model", lambda model=None: DummyLLM()
    )
    builder = GraphBuilder(repo_url="repo", goal="goal")
    builder.compile()
    expected = [
        "classify_intent",
        "explore_repo",
        "generate_plan",
        "generate_code",
        "apply_changes",
        "validate",
        "commit_and_push",
    ]
    assert builder._states == expected
    edges = builder.workflow.edges
    for start, end in zip(expected, expected[1:]):
        assert edges[start] == [end]
    assert edges[expected[-1]] == [END]
    assert builder.workflow.entry == expected[0]
