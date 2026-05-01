from app.config.models.parser import ParserConfig
from app.src.parsers.pdf_parser import PDFParser
from app.src.registries.parser_registry import ParserRegistry


class ParserFactory:
    def __init__(self, config: ParserConfig) -> None:
        self._config = config
    
    def build_registry(self) -> ParserRegistry:
        registry = ParserRegistry()
        registry.register(PDFParser(config=self._config.pdf))
        return registry