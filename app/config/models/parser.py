from pydantic import BaseModel


class PDFParserConfig(BaseModel):
    page_separator: str = "\n"


class ParserConfig(BaseModel):
    pdf: PDFParserConfig = PDFParserConfig()
