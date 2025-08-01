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
            "Vous êtes un assistant IA qui modifie le dépôt pour l'objectif suivant: "
            f"{goal}. Donnez le diff à appliquer."
        )
        logger.info("Generating code with LLM")
        message = self.llm([HumanMessage(content=prompt)])
        context["generated_patch"] = message.content
        logger.debug(message.content)
        return context
