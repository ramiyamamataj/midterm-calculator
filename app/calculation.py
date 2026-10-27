from datetime import datetime
from app.calculator_config import CalculatorConfig

class Calculation:
    def __init__(self, operation: str, a: float, b: float, result: float, timestamp: str = None):
        self.operation = operation
        self.a = a
        self.b = b
        self.result = result
        self.timestamp = timestamp or datetime.now().isoformat()

    def format_result(self) -> str:
        precision = CalculatorConfig.PRECISION
        formatted = f"{self.result:.{precision}f}".rstrip('0').rstrip('.')
        return formatted if formatted != "" else "0"

    def to_dict(self) -> dict:
        return {
            "operation": self.operation,
            "operand1": self.a,
            "operand2": self.b,
            "result": self.result,
            "timestamp": self.timestamp
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Calculation":
        return cls(
            operation=str(data["operation"]),
            a=float(data["operand1"]),
            b=float(data["operand2"]),
            result=float(data["result"]),
            timestamp=str(data["timestamp"])
        )

    def __str__(self) -> str:
        return f"[{self.timestamp}] {self.operation}({self.a}, {self.b}) = {self.format_result()}"
