from os.path import dirname, join
from pathlib import Path

import pytest

from src.c_tool_string.run import c_tool_string, cli

folder_path = dirname(__file__)


def test_one():
    assert c_tool_string(string="asd", folder_path=folder_path) == {
        join(folder_path, "__init__.py"): 0,
        join(folder_path, "run_test.py"): 1,
    }


def test_two():
    assert c_tool_string(string="path", folder_path=folder_path) == {
        join(folder_path, "__init__.py"): 0,
        join(folder_path, "run_test.py"): 37,
    }


def test_three():
    assert c_tool_string(string=".get", folder_path=folder_path) == {
        join(folder_path, "__init__.py"): 0,
        join(folder_path, "run_test.py"): 1,
    }


def test_four():
    assert c_tool_string(string="ctoolstringargs", folder_path=folder_path) == {
        join(folder_path, "__init__.py"): 0,
        join(folder_path, "run_test.py"): 2,
    }


def test_four_case_sensitive():
    assert c_tool_string(
        string="ctoolstringargs", folder_path=folder_path, case_sensitive=True
    ) == {join(folder_path, "__init__.py"): 0, join(folder_path, "run_test.py"): 2}


def test_folder_inexisting():
    with pytest.raises(ValueError, match="folder_path any doesn't exist!"):
        c_tool_string(string="any", folder_path="any")


def test_cli_basic(monkeypatch, tmp_path, capsys):
    # Create test files
    test_file = tmp_path / "test.py"
    test_file.write_text("hello world\nhello again")

    # Mock sys.argv
    monkeypatch.setattr("sys.argv", ["cli", "hello", "-f", str(tmp_path)])

    cli()

    captured = capsys.readouterr()
    assert "SEARCHING string hello" in captured.out
    assert "Total finds: 2" in captured.out


def test_cli_case_sensitive(monkeypatch, tmp_path, capsys):
    test_file = tmp_path / "test.py"
    test_file.write_text("Hello HELLO hello")

    monkeypatch.setattr("sys.argv", ["cli", "hello", "-f", str(tmp_path), "-cs"])

    cli()

    captured = capsys.readouterr()
    assert "Total finds: 1" in captured.out


def test_cli_dont_remove_punctuation_accents(monkeypatch, tmp_path: Path, capsys):
    test_file = tmp_path / "test.py"
    test_file.write_text("café cafe", encoding="utf-8")

    monkeypatch.setattr("sys.argv", ["cli", "café", "-f", str(tmp_path), "-drpa"])

    cli()

    captured = capsys.readouterr()
    assert "Total finds: 1" in captured.out


def test_cli_default_folder(monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["cli", "test_cli"])

    cli()

    captured = capsys.readouterr()
    assert "SEARCHING string test_cli" in captured.out
