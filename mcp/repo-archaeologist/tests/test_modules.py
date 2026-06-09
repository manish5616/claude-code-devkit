from pathlib import Path

from analyzers import modules

FIXTURE = Path(__file__).parent / "fixtures" / "sample.py"


def test_summarize_module_top_level():
    result = modules.summarize_module(FIXTURE)
    assert result["module_docstring"].startswith("Sample module")
    assert "greet" in {f["name"] for f in result["functions"]}
    assert any(c["name"] == "Animal" for c in result["classes"])


def test_summarize_module_captures_methods_and_args():
    result = modules.summarize_module(FIXTURE)
    animal = next(c for c in result["classes"] if c["name"] == "Animal")
    method_names = {m["name"] for m in animal["methods"]}
    assert {"speak", "legs"} <= method_names

    greet = next(f for f in result["functions"] if f["name"] == "greet")
    assert greet["args"] == ["name"]
    assert greet["docstring"] == "Return a greeting."
