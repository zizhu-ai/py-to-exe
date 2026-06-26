# Contributing to py-to-exe

Thanks for your interest in contributing! See the [project README](README.md) for an overview of what py-to-exe does.

## Setup

```bash
git clone https://github.com/zizhu-ai/py-to-exe.git
cd py-to-exe
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev,pyinstaller]"
pytest tests/ -v
```

## Adding hidden imports for a package

Edit `src/py_to_exe/known_imports.py`:

1. Add the package name and its hidden imports to `KNOWN_HIDDEN_IMPORTS`
2. Add test exclusions to `KNOWN_EXCLUDES` if the package has a test suite
3. Test by building a script that uses the package: `py-to-exe test_script.py`
4. Add a test case in `tests/test_analyzer.py`

## Adding error translation patterns

Edit `src/py_to_exe/errors.py`:

1. Add a new regex pattern and handler to `_PATTERNS`
2. Include: title, explanation, and a concrete fix command
3. Add a test case in `tests/test_errors.py`

## Running tests

```bash
pytest tests/ -v          # all tests
ruff check src/ tests/    # lint
```
