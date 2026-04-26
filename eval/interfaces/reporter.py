from abc import ABC, abstractmethod

from eval.domain import EvalRun


class Reporter(ABC):
    """Writes or displays an EvalRun. output_dir may be None for console reporters."""

    @abstractmethod
    def write(self, run: EvalRun, output_dir) -> None: ...