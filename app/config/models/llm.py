from pydantic import BaseModel, SecretStr


class OpenAIProfileConfig(BaseModel):
    model: str = "gpt-4o-mini"
    temperature: float = 0.0
    max_tokens: int = 1024
    api_key: SecretStr


class OllamaProfileConfig(BaseModel):
    model: str = "llama3"
    base_url: str = "http://localhost:11434"
    temperature: float = 0.0
    max_tokens: int = 1024
    timeout: float = 120.0


class LLMProfileConfig(BaseModel):
    provider: str
    openai: OpenAIProfileConfig | None = None
    ollama: OllamaProfileConfig | None = None


class LLMsConfig(BaseModel):
    profiles: dict[str, LLMProfileConfig] = {}