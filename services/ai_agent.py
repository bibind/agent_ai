from loguru import logger
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
import os

try:
    from langchain.llms import Ollama
except Exception:
    Ollama = None


def generate_patch(prompt: str, model: str | None = None, temperature: float = 0.2) -> str:
    model = model or os.environ.get("AI_MODEL", "openai")
    if model == "openai":
        llm = ChatOpenAI(temperature=temperature)
    else:
        if Ollama is None:
            raise RuntimeError("Ollama not installed")
        llm = Ollama(model=model)
    logger.info("Querying LLM for patch generation")
    result = llm.invoke(HumanMessage(content=prompt))
    return result.content
