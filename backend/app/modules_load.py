from pathlib import Path
from importlib import import_module


def asterisk(path: Path, package, globals):
    """
    Imports all symbols from all modules in the `path`
    """
    for module_path in path.glob('*.py'):
        if module_path.is_file() and not module_path.stem.startswith('_'):
            module = import_module(f'.{module_path.stem}', package=package)
            symbols = [symbol for symbol in module.__dict__ if not symbol.startswith("_")]
            globals.update({symbol: getattr(module, symbol) for symbol in symbols})
