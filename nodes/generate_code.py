from pathlib import Path
from loguru import logger
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage


class GenerateCode:
    """Generate or modify code using an LLM."""

    def __init__(self, use_openai: bool = False):
        if use_openai:
            self.llm = ChatOpenAI()
        else:
            # Defaults to local ollama model
            from langchain.llms import Ollama
            self.llm = Ollama(model="llama2")

    def run(self, context: dict) -> dict:
        repo_path = Path(context["repo_path"])
        goal = context.get("goal")
        prompt = (
            "Tu es un agent IA. Ton objectif est : "
            f"{goal}.\n"
            "Retourne uniquement un patch Git compatible avec `git apply`. "
            "Ne mets aucun commentaire ou markdown. Commence directement par "
            "'--- a/' et finis par le diff complet."
        )
        logger.info("Generating code with LLM")
        message = self.llm([HumanMessage(content=prompt)])
        context["generated_patch"] = message.content
        logger.debug(message.content)
        return context
