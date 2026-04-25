from pydantic import BaseModel


class MultiQueryConfig(BaseModel):
    n_variants: int = 3
    prompt_template: str = "multi_query.j2"


class QueryTransformerConfig(BaseModel):
    enabled: bool = False
    provider: str = "multi-query"
    llm_profile: str = "fast"
    prompts_dir: str = "src/prompts"
    multi_query: MultiQueryConfig = MultiQueryConfig()