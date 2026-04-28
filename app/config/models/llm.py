from pydantic import BaseModel


class OpenAIProfileConfig(BaseModel):
    model: str = "gpt-4o-mini"
    temperature: float = 0.0
    max_tokens: int = 1024


class OllamaProfileConfig(BaseModel):
    model: str = "llama3"
    temperature: float = 0.0
    max_tokens: int = 1024
    timeout: float = 120.0


class LLMProfileConfig(BaseModel):
    provider: str = "ollama"
    openai: OpenAIProfileConfig = OpenAIProfileConfig()
    ollama: OllamaProfileConfig = OllamaProfileConfig()


class LLMsConfig(BaseModel):
    profiles: dict[str, LLMProfileConfig] = {}