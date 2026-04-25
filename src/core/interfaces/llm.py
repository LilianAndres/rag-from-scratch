from abc import ABC, abstractmethod


class BaseLanguageModel(ABC):
    """
    Raw text-in, text-out LLM interface.
    """

    @abstractmethod
    def complete(self, prompt: str) -> str:
        """
        Send a fully rendered prompt and return the model's response.

        Parameters
        ----------
        prompt:
            The fully rendered prompt string.

        Returns
        -------
        str
            The model's raw text response.
        """