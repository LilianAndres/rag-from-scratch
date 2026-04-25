from pathlib import Path

from jinja2 import Environment, FileSystemLoader, TemplateNotFound


class PromptLoader:
    """
    Loads and renders Jinja2 prompt templates from the prompts directory.
    """

    def __init__(self, prompts_dir: str | Path = "src/prompts"):
        self._env = Environment(
            loader=FileSystemLoader(str(prompts_dir)),
            trim_blocks=True,
            lstrip_blocks=True,
        )

    def render(self, template_name: str, **kwargs) -> str:
        """
        Render a template by name with the given variables.

        Parameters
        ----------
        template_name:
            Filename relative to prompts_dir, e.g. ``"rag.j2"``.
        **kwargs:
            Variables injected into the template.
        """
        try:
            template = self._env.get_template(template_name)
        except TemplateNotFound:
            raise FileNotFoundError(f"Prompt template not found: {template_name!r}")
        return template.render(**kwargs)