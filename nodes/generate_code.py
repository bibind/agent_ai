from loguru import logger
from langchain.schema import HumanMessage
from services.ai_agent import get_chat_model, CONVERSATION_HISTORY

class GenerateCode:
    """Generate or modify code using an LLM."""

    def __init__(self, use_openai: bool = False):
        model = "openai" if use_openai else None
        self.llm = get_chat_model(model=model)

    def run(self, context: dict) -> dict:
        goal = context.get("goal")
        prompt = (
            "Tu es un agent IA. Ton objectif est : "
            f"{goal}.\n"
            "Retourne uniquement un patch Git compatible avec `git apply`. "
            "Ne mets aucun commentaire ou markdown. Commence directement par "
            "'--- a/' et finis par le diff complet."
        )
        logger.info("Generating code with LLM")
        message = self.llm.invoke(HumanMessage(content=prompt))
        context["generated_patch"] = message.content
        CONVERSATION_HISTORY.append((prompt, message.content))
        logger.debug(message.content)
        return context
