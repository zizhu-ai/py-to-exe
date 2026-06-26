# py-to-exe — Convert Python to EXE with One Command

> The simplest way to convert Python scripts (.py) to standalone executables (.exe). Zero config. Auto dependency detection.

[![PyPI version](https://img.shields.io/pypi/v/smart-py-to-exe)](https://pypi.org/project/smart-py-to-exe/)
[![Python 3.10+](https://img.shields.io/pypi/pyversions/smart-py-to-exe)](https://pypi.org/project/smart-py-to-exe/)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![CI](https://github.com/zizhu-ai/py-to-exe/actions/workflows/ci.yml/badge.svg)](https://github.com/zizhu-ai/py-to-exe/actions)

## Table of Contents

- [Why py-to-exe?](#why-py-to-exe)
- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Interactive Mode](#interactive-mode)
- [How It Works](#how-it-works)
- [Comparison: py-to-exe vs PyInstaller vs auto-py-to-exe](#comparison)
- [FAQ](#faq)
- [Troubleshooting](#troubleshooting)
- [Limitations](#limitations)
- [Contributing](#contributing)

## Why py-to-exe?

Existing tools like PyInstaller are powerful but painful:

- **Missing imports** — hours of `--hidden-import` debugging loops
- **Cryptic errors** — stack traces instead of solutions
- **Too many flags** — 20+ options when you just want an exe
- **No guidance** — trial and error is the only workflow

**py-to-exe** wraps PyInstaller with smart defaults and automatic fixes:

```bash
pip install smart-py-to-exe[pyinstaller]
py-to-exe your_script.py
```

That's it. Your executable is in `./dist/`.

![py-to-exe demo: convert Python script to standalone executable with one command](assets/py-to-exe-convert-python-to-exe-demo.gif)

## Features

- **One command** — `py-to-exe script.py` handles everything
- **Auto dependency detection** — scans your imports, adds hidden imports automatically
- **GUI auto-detect** — detects tkinter/PyQt/wx and hides the console window
- **Human error messages** — translates PyInstaller errors into "what happened + how to fix it"
- **Environment checks** — `py-to-exe doctor` validates your setup before you build
- **Interactive mode** — run `py-to-exe` with no arguments for a guided walkthrough

## Installation

```bash
pip install smart-py-to-exe[pyinstaller]
```

Requires Python 3.10 or newer.

## Quick Start

### One-command build

```bash
# Build your script (output in ./dist/)
py-to-exe app.py

# See what would happen without building
py-to-exe app.py --dry-run

# Check your environment first
py-to-exe doctor
```

### Interactive mode

Run without arguments for a step-by-step guide:

```bash
py-to-exe
```

```
py-to-exe v0.1.0

  Python script to convert: app.py

  Analyzing dependencies...
  ✓ Found imports: requests
  ✓ Auto-added hidden imports for: certifi, charset_normalizer, idna, urllib3

  Output name (app):
  Show console window? [y/n] (y):
  Package as single file? [y/n] (n):
  Output directory (./dist):

  ▸ Building...
  ✓ Done! Output: ./dist/app/app (4.2s)
```

## Usage

### Common options

```bash
py-to-exe app.py --name MyApp           # Custom executable name
py-to-exe app.py --icon app.ico         # Custom icon
py-to-exe app.py --onefile              # Single file (default: directory)
py-to-exe app.py --no-console           # Hide console (auto for GUI apps)
py-to-exe app.py -o ./build             # Custom output directory
py-to-exe app.py --add-data "data/:data/"   # Include data files
py-to-exe app.py --hidden-import foo    # Add hidden imports manually
py-to-exe app.py -v                     # Verbose output
```

### Environment doctor

```bash
# Check Python version, virtual env, and PyInstaller
py-to-exe doctor

# Also check a specific script
py-to-exe doctor app.py
```

## How it works

1. **Analyze** — Scans your script's AST for imports, matches against a database of known hidden imports
2. **Detect** — Identifies GUI frameworks (tkinter, PyQt, wx) and auto-configures console settings
3. **Build** — Calls PyInstaller with optimized defaults
4. **Translate** — If the build fails, maps the error to a human-readable fix

## Comparison

| Feature | py-to-exe | PyInstaller | auto-py-to-exe |
|---------|-----------|-------------|----------------|
| Zero-config build | Yes | No (many flags) | GUI required |
| Auto hidden imports | Yes | No | No |
| Human error messages | Yes | No | No |
| GUI auto-detection | Yes | No | Manual |
| Environment doctor | Yes | No | No |
| Interactive mode | Yes (TUI) | No | Yes (GUI) |

## FAQ

### How do I convert a Python script to an exe?

Install py-to-exe and run one command:

```bash
pip install smart-py-to-exe[pyinstaller]
py-to-exe your_script.py
```

### Why does my exe get flagged as a virus?

PyInstaller's packaging method can trigger antivirus false positives. This happens because the self-extracting format resembles patterns used by some malware. Options:

- Use `--onefile` sparingly (directory mode triggers fewer alerts)
- Sign your executable with a code signing certificate
- Submit false positive reports to your antivirus vendor

### How do I reduce the exe file size?

- Use a virtual environment to avoid bundling unnecessary packages
- The minimum size is ~15-25 MB (Python runtime itself)
- Run `py-to-exe doctor` to verify you're in a clean virtual environment

### Can I build a Windows exe on macOS or Linux?

No. You must build on the target platform. For cross-platform builds, use GitHub Actions:

```yaml
# .github/workflows/build.yml
jobs:
  build:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install smart-py-to-exe[pyinstaller]
      - run: py-to-exe your_script.py
```

### py-to-exe vs PyInstaller

py-to-exe **uses** PyInstaller under the hood. It adds automatic dependency detection, human-readable errors, and zero-config defaults. If you need full control over every PyInstaller option, use PyInstaller directly.

### py-to-exe vs auto-py-to-exe

auto-py-to-exe is a GUI wrapper for PyInstaller. py-to-exe is a CLI wrapper with smart defaults. Choose auto-py-to-exe if you prefer a graphical interface. Choose py-to-exe if you want a one-command workflow or CI/CD integration.

### How to convert .py to .exe on Windows?

Same as any platform — install and run:

```bash
pip install smart-py-to-exe[pyinstaller]
py-to-exe your_script.py
```

The output exe will be in `./dist/your_script/`. You can distribute the entire folder to other Windows users.

### What is the best Python to EXE converter?

It depends on your needs. For most users, py-to-exe offers the fastest path with automatic dependency handling. For full control, use PyInstaller directly. For a GUI, use auto-py-to-exe. For maximum performance and code protection, consider Nuitka (py-to-exe will support Nuitka in v0.2).

## Troubleshooting

### ModuleNotFoundError after building

Your exe can't find a module at runtime. py-to-exe auto-detects most imports, but dynamic imports need manual help:

```bash
py-to-exe app.py --hidden-import missing_module
```

### exe crashes on another computer

Usually caused by missing system libraries (Visual C++ Redistributable on Windows). Use directory mode (default) instead of `--onefile`, and distribute the entire output folder.

### exe file is too large

Python's runtime alone is 15-25 MB. To minimize size:

1. Use a virtual environment (avoid bundling system packages)
2. Run `py-to-exe doctor` to check your environment
3. Only install packages your script actually needs

### "Failed to execute script" error

Run with `--console` to see the actual error:

```bash
py-to-exe app.py --console
```

Then check the console output when running the exe.

### Build takes too long

Large packages (numpy, pandas, torch) increase build time. First builds are slower due to cache warming. Subsequent builds reuse the cache and are faster.

## Limitations

- **Platform-specific builds** — Must build on the target OS (no cross-compilation)
- **Antivirus false positives** — Cannot be fully eliminated with PyInstaller
- **Dynamic imports** — `__import__(var)` / `importlib.import_module()` need manual `--hidden-import`
- **Minimum size ~15-25 MB** — Python runtime itself sets the floor
- **PyInstaller only (v0.1)** — Nuitka support planned for v0.2

## Contributing

Contributions welcome! See the [contributing guide](CONTRIBUTING.md) for setup instructions.

Areas that need help:

- Adding more packages to the [hidden imports database](src/py_to_exe/known_imports.py)
- Testing on Windows and Linux
- Expanding [error pattern coverage](src/py_to_exe/errors.py)

## License

[MIT](LICENSE)
