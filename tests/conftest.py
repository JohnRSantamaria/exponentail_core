# tests/conftest.py
import pytest
from collections import defaultdict

_descriptive_results = defaultdict(list)


def pytest_itemcollected(item):
    """Reemplaza el nodeid por el docstring si existe"""
    doc = item._obj.__doc__
    if doc:
        item._nodeid = doc.strip()
        _descriptive_results[item.fspath].append(doc.strip())


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """Muestra agrupados por archivo los tests que pasaron"""
    terminalreporter.write_sep("=", "Resumen agrupado por archivo y descripción")
    for file, descriptions in _descriptive_results.items():
        terminalreporter.write_line(f"\n📄 {file}")
        for desc in descriptions:
            terminalreporter.write_line(f"  - ✓ {desc}")
