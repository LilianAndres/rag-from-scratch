from pydantic import BaseModel


class GeneratorConfig(BaseModel):
    llm_profile: str = "strong"
    prompt_template: str = "rag.j2"
    prompts_dir: str = "src/prompts"