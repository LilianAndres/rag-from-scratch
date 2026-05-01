from pydantic import BaseModel, SecretStr


class OpenAIProviderConfig(BaseModel):
    base_url: str = "https://api.openai.com/v1"
    api_key: SecretStr

class OllamaProviderConfig(BaseModel):
    base_url: str = "http://localhost:11434/v1"
    api_key: SecretStr | None = None

class InfinityProviderConfig(BaseModel):
    base_url: str = "http://localhost:7997/v1"
    api_key: SecretStr | None = None

class ProvidersConfig(BaseModel):
    openai: OpenAIProviderConfig | None = None
    ollama: OllamaProviderConfig = OllamaProviderConfig()
    infinity: InfinityProviderConfig = InfinityProviderConfig()