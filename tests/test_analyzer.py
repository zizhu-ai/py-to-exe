from py_to_exe.analyzer import AnalysisResult, analyze, extract_imports


def test_extract_imports_simple(tmp_path):
    script = tmp_path / "app.py"
    script.write_text('import os\nimport json\nprint("hi")\n')
    imports = extract_imports(script)
    assert "os" in imports
    assert "json" in imports


def test_extract_imports_from(tmp_path):
    script = tmp_path / "app.py"
    script.write_text("from pathlib import Path\nfrom os.path import join\n")
    imports = extract_imports(script)
    assert "pathlib" in imports
    assert "os" in imports


def test_extract_imports_nested(tmp_path):
    script = tmp_path / "app.py"
    script.write_text(
        "def foo():\n"
        "    import requests\n"
        "    return requests.get('http://example.com')\n"
    )
    imports = extract_imports(script)
    assert "requests" in imports


def test_extract_imports_syntax_error(tmp_path):
    script = tmp_path / "bad.py"
    script.write_text("def broken(\n")
    imports = extract_imports(script)
    assert imports == set()


def test_analyze_simple(tmp_path):
    script = tmp_path / "app.py"
    script.write_text('import os\nimport json\nprint("hello")\n')
    result = analyze(script)
    assert isinstance(result, AnalysisResult)
    assert "os" in result.detected_imports
    assert result.has_gui_framework is False
    assert isinstance(result.hidden_imports, list)


def test_analyze_requests_hidden_imports(tmp_path):
    script = tmp_path / "app.py"
    script.write_text("import requests\n")
    result = analyze(script)
    assert "requests" in result.detected_imports
    assert "urllib3" in result.hidden_imports
    assert "certifi" in result.hidden_imports


def test_analyze_gui_detection(tmp_path):
    script = tmp_path / "app.py"
    script.write_text("import tkinter\n")
    result = analyze(script)
    assert result.has_gui_framework is True


def test_analyze_no_gui(tmp_path):
    script = tmp_path / "app.py"
    script.write_text("import sys\n")
    result = analyze(script)
    assert result.has_gui_framework is False


def test_analyze_pandas_excludes(tmp_path):
    script = tmp_path / "app.py"
    script.write_text("import pandas\n")
    result = analyze(script)
    assert "pandas.tests" in result.suggested_excludes


def test_analyze_empty_script(tmp_path):
    script = tmp_path / "empty.py"
    script.write_text("")
    result = analyze(script)
    real_imports = result.detected_imports - {"__main__", "builtins"}
    assert real_imports == set()
    assert result.has_gui_framework is False
