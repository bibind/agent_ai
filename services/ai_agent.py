from logging_config import logger
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
from langchain_core.language_models.chat_models import BaseChatModel
import os

try:
    from langchain_community.chat_models import ChatOllama
except Exception:  # pragma: no cover - optional dependency
    ChatOllama = None

CONVERSATION_HISTORY: list[tuple[str, str]] = []


def get_chat_model(model: str | None = None, temperature: float = 0.2) -> BaseChatModel:
    """Return a chat model instance based on the configuration."""
    model = model or os.environ.get("AI_MODEL", "openai")
    if model == "openai":
        llm: BaseChatModel = ChatOpenAI(temperature=temperature)
    else:
        if ChatOllama is None:
            raise RuntimeError("ChatOllama not available")
        llm = ChatOllama(model=model, temperature=temperature)
    return llm


def generate_patch(prompt: str, model: str | None = None, temperature: float = 0.2) -> str:
    """Generate a git patch using the configured chat model."""
    llm = get_chat_model(model=model, temperature=temperature)
    logger.info("Querying LLM for patch generation")
    message = llm.invoke(HumanMessage(content=prompt))
    CONVERSATION_HISTORY.append((prompt, message.content))
    return message.content
