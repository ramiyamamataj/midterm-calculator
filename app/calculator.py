from abc import ABC, abstractmethod
from app.calculation import Calculation
from app.history import HistoryManager
from app.operations import OperationFactory
from app.logger import Logger
from app.calculator_config import CalculatorConfig

class CalculatorObserver(ABC):
    @abstractmethod
    def update(self, calculation: Calculation, history_manager: HistoryManager):
        pass  # pragma: no cover

class LoggingObserver(CalculatorObserver):
    def __init__(self):
        self.logger = Logger.get_logger()

    def update(self, calculation: Calculation, history_manager: HistoryManager):
        self.logger.info(
            f"Operation: {calculation.operation} | "
            f"Operands: ({calculation.a}, {calculation.b}) | "
            f"Result: {calculation.result}"
        )

class AutoSaveObserver(CalculatorObserver):
    def update(self, calculation: Calculation, history_manager: HistoryManager):
        if CalculatorConfig.AUTO_SAVE:
            history_manager.save_to_csv()

class Calculator:
    def __init__(self):
        self.history_manager = HistoryManager()
        self._observers: list[CalculatorObserver] = []
        self._register_default_observers()

    def _register_default_observers(self):
        self.add_observer(LoggingObserver())
        self.add_observer(AutoSaveObserver())

    def add_observer(self, observer: CalculatorObserver):
        self._observers.append(observer)

    def notify_observers(self, calculation: Calculation):
        for obs in self._observers:
            obs.update(calculation, self.history_manager)

    def calculate(self, operation_name: str, a: float, b: float) -> Calculation:
        op = OperationFactory.get_operation(operation_name)
        result = op.execute(a, b)
        calc = Calculation(operation_name, a, b, result)
        self.history_manager.add_calculation(calc)
        self.notify_observers(calc)
        return calc

    def undo(self) -> bool:
        return self.history_manager.undo()

    def redo(self) -> bool:
        return self.history_manager.redo()

    def clear(self):
        self.history_manager.clear()

    def save(self):
        self.history_manager.save_to_csv()

    def load(self):
        self.history_manager.load_from_csv()

    def get_history(self) -> list[Calculation]:
        return self.history_manager.history
