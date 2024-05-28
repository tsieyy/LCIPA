from langchain_community.vectorstores import FAISS
import os


class Memory:
    def __init__(self, embedding_provider, **kwargs):

        _embeddings = None
        match embedding_provider:
            case "ollama":
                from langchain.embeddings import OllamaEmbeddings
                _embeddings = OllamaEmbeddings(model="llama2")
            case "openai":
                from langchain_openai import OpenAIEmbeddings
                if "OPENAI_API_KEY_CN" in os.environ:
                    api_key = os.environ["OPENAI_API_KEY_CN"]
                    base_url = os.environ.get("OPENAI_API_BASE_CN", None)
                    _embeddings = OpenAIEmbeddings(model="text-embedding-3-small", api_key=api_key, base_url=base_url)
                else:
                    _embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
            case "azureopenai":
                from langchain_openai import AzureOpenAIEmbeddings
                _embeddings = AzureOpenAIEmbeddings(deployment=os.environ["AZURE_EMBEDDING_MODEL"], chunk_size=16)
            case "huggingface":
                from langchain.embeddings import HuggingFaceEmbeddings
                _embeddings = HuggingFaceEmbeddings()

            case _:
                raise Exception("Embedding provider not found.")

        self._embeddings = _embeddings

    def get_embeddings(self):
        return self._embeddings
