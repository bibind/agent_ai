from loguru import logger

class GeneratePlan:
    """Generate a simple plan for the agent."""

    def run(self, context: dict) -> dict:
        goal = context.get("goal")
        # Placeholder plan generation
        plan = [
            "Analyse du dépôt",
            "Génération du code nécessaire",
            "Validation avec Flyte",
            "Commit et push"
        ]
        context["plan"] = plan
        logger.info("Generated plan:\n" + "\n".join(f"- {step}" for step in plan))
        return context
