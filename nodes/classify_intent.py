from loguru import logger

from . import NodeContext


class ClassifyIntent:
    """Node to classify user intent from a goal."""

    def run(self, context: NodeContext) -> NodeContext:
        goal = context.get("goal", "")
        # Very naive classification just for example
        if "bug" in goal.lower():
            intent = "bugfix"
        elif any(k in goal.lower() for k in ["doc", "documentation"]):
            intent = "documentation"
        elif any(k in goal.lower() for k in ["feature", "ajouter", "améliorer"]):
            intent = "feature"
        else:
            intent = "chore"
        context["intent"] = intent
        logger.info(f"Classified intent as {intent}")
        return context
