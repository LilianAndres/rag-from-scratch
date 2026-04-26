from pydantic import BaseModel


class OllamaJudgeConfig(BaseModel):
    model: str = "llama3:8b"
    embedding_model: str = "nomic-embed-text"
    temperature: float = 0.0

class OpenAIJudgeConfig(BaseModel):
    model: str = "gpt-4o-mini"
    embedding_model: str = "text-embedding-3-small"
    temperature: float = 0.0


class JudgeLLMConfig(BaseModel):
    provider: str = "ollama"
    openai: OpenAIJudgeConfig | None = None
    ollama: OllamaJudgeConfig = OllamaJudgeConfig()