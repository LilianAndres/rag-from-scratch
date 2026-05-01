from typing import Annotated, Literal, Union
from pydantic import BaseModel, Field


class LocalSourceRequest(BaseModel):
    type: Literal["local"]
    path: str
    glob_pattern: str = "**/*"
    recursive: bool = True


class S3SourceRequest(BaseModel):
    type: Literal["s3"]
    bucket: str
    prefix: str = ""
    region: str = "us-east-1"
    aws_access_key_id: str | None = None
    aws_secret_access_key: str | None = None


SourceRequest = Annotated[
    Union[LocalSourceRequest, S3SourceRequest],
    Field(discriminator="type")
]