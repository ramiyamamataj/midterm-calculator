import pytest
from app.calculation import Calculation
from app.calculator_config import CalculatorConfig

def test_calculation_initialization():
    calc = Calculation("add", 5.0, 10.0, 15.0, "2026-01-01T00:00:00")
    assert calc.operation == "add"
    assert calc.a == 5.0
    assert calc.b == 10.0
    assert calc.result == 15.0
    assert calc.timestamp == "2026-01-01T00:00:00"

def test_calculation_formatting():
    calc1 = Calculation("add", 1.0, 2.0, 3.0)
    assert calc1.format_result() == "3"
    calc2 = Calculation("divide", 1.0, 3.0, 1.0 / 3.0)
    assert calc2.format_result() == "0.3333"
    calc3 = Calculation("add", 0.0, 0.0, 0.0)
    assert calc3.format_result() == "0"

def test_calculation_serialization():
    calc = Calculation("multiply", 2.0, 4.0, 8.0, "2026-01-01T12:00:00")
    data = calc.to_dict()
    assert data["operation"] == "multiply"
    assert data["operand1"] == 2.0
    assert data["operand2"] == 4.0
    assert data["result"] == 8.0
    assert data["timestamp"] == "2026-01-01T12:00:00"

    reconstructed = Calculation.from_dict(data)
    assert reconstructed.operation == "multiply"
    assert reconstructed.a == 2.0
    assert reconstructed.b == 4.0
    assert reconstructed.result == 8.0
    assert "multiply(2.0, 4.0) = 8" in str(reconstructed)
