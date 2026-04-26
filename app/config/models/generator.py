from pydantic import BaseModel


class GeneratorConfig(BaseModel):
    llm_profile: str
    prompts_dir: str = "app/config/prompts/templates"
    prompt_template: str = "rag.j2"
