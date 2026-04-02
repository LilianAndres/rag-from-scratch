from pydantic import BaseModel, Field


class PDFLoaderConfig(BaseModel):
    page_separator: str = "\n"


class LoaderConfig(BaseModel):
    pdf: PDFLoaderConfig = PDFLoaderConfig()
