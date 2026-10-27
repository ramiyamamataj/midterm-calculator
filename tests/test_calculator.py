import pytest
from app.calculator import Calculator
from app.input_validators import InputValidator
from app.exceptions import ValidationError, OperationError
from app.calculator_config import CalculatorConfig

def test_input_validator():
    a, b = InputValidator.validate_operands("12.5", "3.5")
    assert a == 12.5 and b == 3.5

    with pytest.raises(ValidationError):
        InputValidator.validate_number("invalid_number")

    with pytest.raises(ValidationError):
        InputValidator.validate_number("100000000000")

def test_calculator_state_operations():
    calc = Calculator()
    calc.calculate("add", 1, 2)
    calc.calculate("multiply", 2, 3)
    assert len(calc.get_history()) == 2

    assert calc.undo() is True
    assert len(calc.get_history()) == 1
    assert calc.get_history()[-1].operation == "add"

    assert calc.redo() is True
    assert len(calc.get_history()) == 2

    calc.clear()
    assert len(calc.get_history()) == 0
    assert calc.undo() is True
    assert len(calc.get_history()) == 2

    calc.redo()
    assert calc.redo() is False

def test_history_csv_storage(tmp_path):
    calc = Calculator()
    test_file = tmp_path / "history.csv"
    calc.calculate("add", 10, 20)
    calc.history_manager.save_to_csv(filepath=test_file)

    restored = Calculator()
    restored.history_manager.load_from_csv(filepath=test_file)
    assert len(restored.get_history()) == 1
    assert restored.get_history()[0].operation == "add"

    with pytest.raises(OperationError):
        restored.history_manager.load_from_csv(filepath=tmp_path / "missing.csv")

    corrupted = tmp_path / "bad.csv"
    corrupted.write_text("invalid,header\n1,2")
    with pytest.raises(OperationError):
        restored.history_manager.load_from_csv(filepath=corrupted)
