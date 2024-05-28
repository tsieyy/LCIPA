import os

from colorama import Fore, Style
from langchain_openai import ChatOpenAI


class OpenAIProvider:

    def __init__(
        self,
        model,
        temperature,
        max_tokens
    ):
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.api_key = self.get_api_key()
        self.base_url = self.get_base_url()
        self.llm = self.get_llm_model()

    def get_api_key(self):
        """
        Gets the OpenAI API key
        Returns:

        """
        try:
            api_key = os.environ["OPENAI_API_KEY"]
        except KeyError:
            raise Exception(
                "OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")
        return api_key

    def get_base_url(self):
        """
        Gets the OpenAI Base URL from the environment variable if defined otherwise use the default one
        Returns:

        """
        base_url = os.environ.get("OPENAI_API_BASE", None)
        return base_url

    def get_llm_model(self):
        # Initializing the chat model
        llm = ChatOpenAI(
            model=self.model,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            api_key=self.api_key,
            base_url=self.base_url if self.base_url else None
        )

        return llm

    async def get_chat_response(self, messages, stream, websocket=None):
        if not stream:
            # Getting output from the model chain using ainvoke for asynchronous invoking
            output = await self.llm.ainvoke(messages)

            return output.content

        else:
            return await self.stream_response(messages, websocket)

    async def stream_response(self, messages, websocket=None):
        paragraph = ""
        response = ""

        # Streaming the response using the chain astream method from langchain
        async for chunk in self.llm.astream(messages):
            content = chunk.content
            if content is not None:
                response += content
                paragraph += content
                if "\n" in paragraph:
                    if websocket is not None:
                        await websocket.send_json({"type": "report", "output": paragraph})
                    else:
                        print(f"{Fore.GREEN}{paragraph}{Style.RESET_ALL}")
                    paragraph = ""

        return response


class OpenAIProviderCN(OpenAIProvider):

    def __init__(self, model, temperature, max_tokens):
        super().__init__(model, temperature, max_tokens)

    def get_api_key(self):
        """
        Gets the OpenAI API key for China
        Returns:

        """
        try:
            api_key = os.environ["OPENAI_API_KEY_CN"]
        except KeyError:
            raise Exception(
                "OpenAI API key for China not found. Please set the OPENAI_API_KEY_CN environment variable.")
        return api_key

    def get_base_url(self):
        """
        Gets the OpenAI Base URL for China from the environment variable if defined otherwise use the default one
        Returns:

        """
        base_url = os.environ.get("OPENAI_API_BASE_CN", None)
        return base_url

    @classmethod
    def get_chat_model(cls, model):
        api_key = os.environ["OPENAI_API_KEY_CN"]
        base_url = os.environ.get("OPENAI_API_BASE_CN", None)
        return ChatOpenAI(model=model, openai_api_key=api_key, openai_api_base=base_url)

