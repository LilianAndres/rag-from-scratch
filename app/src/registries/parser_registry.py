from app.src.core.domain.document import RawDocument
from app.src.core.interfaces.parser import BaseParser


class ParserRegistry:

    def __init__(self):
        self._parsers: list[BaseParser] = []

    def register(self, parser: BaseParser) -> None:
        self._parsers.append(parser)

    def resolve(self, raw: RawDocument) -> BaseParser:
        for parser in self._parsers:
            if parser.can_handle(raw):
                return parser
        raise ValueError(f"No parser found for the raw document for URI {raw.source_uri}.")