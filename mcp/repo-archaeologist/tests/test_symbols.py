from pathlib import Path

from analyzers import symbols

FIXTURE = Path(__file__).parent / "fixtures" / "sample.py"


def test_list_symbols_finds_function_class_and_methods():
    result = symbols.list_symbols(FIXTURE)
    pairs = {(s["name"], s["kind"]) for s in result}
    assert ("greet", "function") in pairs
    assert ("Animal", "class") in pairs
    assert ("speak", "method") in pairs
    assert ("legs", "method") in pairs


def test_find_symbol_class():
    result = symbols.find_symbol("Animal", FIXTURE)
    assert len(result) == 1
    assert result[0]["kind"] == "class"
    assert result[0]["lineno"] == 13


def test_find_symbol_method_records_parent():
    result = symbols.find_symbol("speak", FIXTURE)
    assert len(result) == 1
    assert result[0]["kind"] == "method"
    assert result[0]["parent"] == "Animal"


def test_find_symbol_missing_returns_empty():
    assert symbols.find_symbol("does_not_exist", FIXTURE) == []
