import os

from langchain.adapters.openai import convert_openai_messages
from langchain_openai import ChatOpenAI


def call_model(prompt: list, model: str = "gpt-3.5-turbo", max_retries: int = 2, response_format: str = None) -> str:

    optional_params = {}
    if response_format == 'json':
        optional_params = {
            "response_format": {"type": "json_object"}
        }

    lc_messages = convert_openai_messages(prompt)
    api_key = os.environ["OPENAI_API_KEY_CN"]
    base_url = os.environ.get("OPENAI_API_BASE_CN", None)
    response = ChatOpenAI(
        model=model,
        api_key=api_key,
        base_url=base_url,
        max_retries=max_retries,
        model_kwargs=optional_params,
    ).invoke(lc_messages).content
    return response