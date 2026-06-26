from py_to_exe.errors import HumanError, translate_error


def test_translate_module_not_found():
    stderr = "ModuleNotFoundError: No module named 'cv2'"
    result = translate_error(stderr)
    assert result is not None
    assert isinstance(result, HumanError)
    assert "cv2" in result.title
    assert "pip install" in result.fix


def test_translate_import_error():
    stderr = "ImportError: cannot import name 'foo' from 'bar'"
    result = translate_error(stderr)
    assert result is not None
    assert "foo" in result.title
    assert "bar" in result.title


def test_translate_file_not_found():
    stderr = "FileNotFoundError: [Errno 2] No such file or directory: 'data.json'"
    result = translate_error(stderr)
    assert result is not None
    assert "data.json" in result.title
    assert "--add-data" in result.fix


def test_translate_recursion():
    stderr = "RecursionError: maximum recursion depth exceeded"
    result = translate_error(stderr)
    assert result is not None
    assert "Recursion" in result.title


def test_translate_permission():
    stderr = "PermissionError: [Errno 13] Permission denied: '/tmp/out.exe'"
    result = translate_error(stderr)
    assert result is not None
    assert "Permission" in result.title


def test_translate_disk_full():
    stderr = "OSError: [Errno 28] No space left on device"
    result = translate_error(stderr)
    assert result is not None
    assert "Disk" in result.title


def test_translate_unknown_error():
    stderr = "some random error nobody expected"
    result = translate_error(stderr)
    assert result is None


def test_translate_multiline_stderr():
    stderr = (
        "INFO: Building because out-of-date\n"
        "WARNING: something\n"
        "ModuleNotFoundError: No module named 'pandas'\n"
        "ERROR: Analysis failed\n"
    )
    result = translate_error(stderr)
    assert result is not None
    assert "pandas" in result.title


def test_translate_icon_not_found():
    stderr = "Icon file app.ico not found"
    result = translate_error(stderr)
    assert result is not None
    assert "Icon" in result.title
