from unittest.mock import patch
from main import start_repl, show_help

def test_help_menu_output(capsys):
    show_help()
    captured = capsys.readouterr()
    assert "Enhanced Calculator CLI Help" in captured.out

def test_repl_commands_flow(capsys):
    simulated_inputs = [
        "help",
        "add 10 5",
        "percent 20 100",
        "history",
        "undo",
        "redo",
        "clear",
        "save",
        "load",
        "divide 10 0",
        "add 5",
        "invalid_command",
        "exit"
    ]
    with patch("builtins.input", side_effect=simulated_inputs):
        start_repl()
    captured = capsys.readouterr()
    assert "Result: 15" in captured.out
    assert "Division by zero is undefined" in captured.out
