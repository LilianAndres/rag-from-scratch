from app.src.core.interfaces.query import BaseQueryTransformer
from app.src.core.search.search_query import SearchQuery


class PassthroughTransformer(BaseQueryTransformer):
    def __init__(self):
        pass

    def transform(self, query: SearchQuery) -> list[SearchQuery]:
        return [query]