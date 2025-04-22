from langchain_openai import AzureChatOpenAI
from pydantic import SecretStr

from src.constants.config import LlmConfig


def get_llm():
    return AzureChatOpenAI(
        model="gpt-4o",
        api_version="2024-10-21",
        azure_endpoint=LlmConfig.base_url,
        api_key=SecretStr(LlmConfig.api_key),
        temperature=0.0,
    )