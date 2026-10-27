from abc import ABC, abstractmethod
import math
from app.exceptions import OperationError

class BaseOperation(ABC):
    @abstractmethod
    def execute(self, a: float, b: float) -> float:
        pass  # pragma: no cover

class AddOperation(BaseOperation):
    def execute(self, a: float, b: float) -> float:
        return a + b

class SubtractOperation(BaseOperation):
    def execute(self, a: float, b: float) -> float:
        return a - b

class MultiplyOperation(BaseOperation):
    def execute(self, a: float, b: float) -> float:
        return a * b

class DivideOperation(BaseOperation):
    def execute(self, a: float, b: float) -> float:
        if b == 0:
            raise OperationError("Division by zero is undefined.")
        return a / b

class PowerOperation(BaseOperation):
    def execute(self, a: float, b: float) -> float:
        try:
            return math.pow(a, b)
        except OverflowError:
            raise OperationError("Exponentiation resulted in overflow.")
        except ValueError:
            raise OperationError("Negative base with non-integer exponent produces a complex number.")

class RootOperation(BaseOperation):
    def execute(self, a: float, b: float) -> float:
        if b == 0:
            raise OperationError("Zeroth root is undefined.")
        if a < 0 and b % 2 == 0:
            raise OperationError("Even root of a negative number produces a complex number.")
        if a < 0:
            return -math.pow(-a, 1.0 / b)
        return math.pow(a, 1.0 / b)

class ModulusOperation(BaseOperation):
    def execute(self, a: float, b: float) -> float:
        if b == 0:
            raise OperationError("Modulus by zero is undefined.")
        return a % b

class IntDivideOperation(BaseOperation):
    def execute(self, a: float, b: float) -> float:
        if b == 0:
            raise OperationError("Integer division by zero is undefined.")
        return float(a // b)

class PercentOperation(BaseOperation):
    def execute(self, a: float, b: float) -> float:
        if b == 0:
            raise OperationError("Percentage calculation with base zero is undefined.")
        return (a / b) * 100.0

class AbsDiffOperation(BaseOperation):
    def execute(self, a: float, b: float) -> float:
        return abs(a - b)

class OperationFactory:
    _operations: dict[str, type[BaseOperation]] = {
        "add": AddOperation,
        "subtract": SubtractOperation,
        "multiply": MultiplyOperation,
        "divide": DivideOperation,
        "power": PowerOperation,
        "root": RootOperation,
        "modulus": ModulusOperation,
        "int_divide": IntDivideOperation,
        "percent": PercentOperation,
        "abs_diff": AbsDiffOperation,
    }

    @classmethod
    def get_operation(cls, operation_name: str) -> BaseOperation:
        op_cls = cls._operations.get(operation_name.lower())
        if not op_cls:
            raise OperationError(f"Unsupported operation '{operation_name}'.")
        return op_cls()

    @classmethod
    def list_supported_operations(cls) -> list[str]:
        return sorted(list(cls._operations.keys()))
