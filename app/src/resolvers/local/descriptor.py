from dataclasses import dataclass

from app.src.core.domain.source import SourceDescriptor


@dataclass
class LocalSourceDescriptor(SourceDescriptor):
    path: str # absolute path to file or directory
    glob_pattern: str = "**/*" # recursive by default
    recursive: bool = True