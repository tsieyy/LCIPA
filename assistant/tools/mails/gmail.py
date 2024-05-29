from langchain_community.agent_toolkits import GmailToolkit
from langchain_community.tools.gmail.utils import (
    build_resource_service,
    get_gmail_credentials,
)
from assistant.config import cfg


credentials = get_gmail_credentials(
    token_file=f"{cfg.gmail_config_bath_path}/token.json",
    scopes=["https://mail.google.com/"],
    client_secrets_file=f"{cfg.gmail_config_bath_path}/cre.json",
)
api_resource = build_resource_service(credentials=credentials)
gmail_toolkit = GmailToolkit(api_resource=api_resource)
