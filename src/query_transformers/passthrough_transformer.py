from src.core import SearchQuery
from src.core.interfaces.query_transformer import BaseQueryTransformer


class PassthroughTransformer(BaseQueryTransformer):
    def __init__(self):
        pass

    def transform(self, query: SearchQuery) -> list[SearchQuery]:
        return [query]