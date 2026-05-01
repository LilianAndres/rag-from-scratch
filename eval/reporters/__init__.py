from eval.interfaces.reporter import Reporter
from eval.reporters.console_reporter import ConsoleReporter
from eval.reporters.csv_reporter import CsvReporter
from eval.reporters.json_reporter import JsonReporter

_REGISTRY: dict[str, type[Reporter]] = {
    "console": ConsoleReporter,
    "json": JsonReporter,
    "csv": CsvReporter,
}

def build_reporters(names: list[str]) -> list[Reporter]:
    reporters = []
    for name in names:
        cls = _REGISTRY.get(name)
        if cls is None:
            raise ValueError(f"Unknown reporter: {name!r}. Available: {list(_REGISTRY)}")
        reporters.append(cls())
    return reporters