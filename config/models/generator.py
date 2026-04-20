from pydantic import BaseModel, Field, SecretStr


class OpenAIGeneratorConfig(BaseModel):
    model: str = "gpt-4o-mini"
    temperature: float = 0.0
    max_tokens: int = 1024
    prompt_template: str = "rag.j2"
    api_key: SecretStr


class OllamaGeneratorConfig(BaseModel):
    model: str = "llama3"
    base_url: str = "http://localhost:11434"
    temperature: float = 0.0
    max_tokens: int = 1024
    prompt_template: str = "rag.j2"
    timeout: float = 120.0


class GeneratorConfig(BaseModel):
    provider: str = "ollama"
    prompts_dir: str = "src/prompts"
    openai: OpenAIGeneratorConfig | None = None
    ollama: OllamaGeneratorConfig | None= None