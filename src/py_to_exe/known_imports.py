KNOWN_HIDDEN_IMPORTS: dict[str, list[str]] = {
    "requests": [
        "urllib3",
        "certifi",
        "charset_normalizer",
        "idna",
    ],
    "pandas": [
        "pandas._libs.tslibs.timedeltas",
        "pandas._libs.tslibs.nattype",
        "pandas._libs.tslibs.np_datetime",
        "pandas._libs.skiplist",
    ],
    "numpy": [
        "numpy.core._methods",
        "numpy.lib.format",
    ],
    "PIL": [
        "PIL._tkinter_finder",
    ],
    "tkinter": [],
}

KNOWN_EXCLUDES: dict[str, list[str]] = {
    "pandas": ["pandas.tests"],
    "numpy": ["numpy.tests", "numpy.distutils"],
}

GUI_FRAMEWORKS: set[str] = {
    "tkinter",
    "PyQt5",
    "PyQt6",
    "PySide2",
    "PySide6",
    "wx",
    "kivy",
}
