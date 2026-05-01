from dataclasses import dataclass

from app.src.core.domain.source import SourceDescriptor


@dataclass
class S3SourceDescriptor(SourceDescriptor):
    bucket: str
    prefix: str = ""
    region: str = "us-east-1"
    aws_access_key_id: str | None = None
    aws_secret_access_key: str | None = None
    chunk_size: int = 8 * 1024 * 1024 # 8 MB