from app.exceptions import ValidationError
from app.calculator_config import CalculatorConfig

class InputValidator:
    @staticmethod
    def validate_number(value: str) -> float:
        try:
            val = float(value)
        except (ValueError, TypeError):
            raise ValidationError(f"Invalid input: '{value}' is not a valid number.")

        max_val = CalculatorConfig.MAX_INPUT_VALUE
        if abs(val) > max_val:
            raise ValidationError(f"Value '{val}' exceeds maximum allowed value ({max_val}).")
        return val

    @staticmethod
    def validate_operands(a_str: str, b_str: str) -> tuple[float, float]:
        a = InputValidator.validate_number(a_str)
        b = InputValidator.validate_number(b_str)
        return a, b
