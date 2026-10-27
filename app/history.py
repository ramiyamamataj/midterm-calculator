import pandas as pd
from app.calculation import Calculation
from app.calculator_memento import CalculatorMemento
from app.calculator_config import CalculatorConfig
from app.exceptions import OperationError

class HistoryManager:
    def __init__(self):
        self.history: list[Calculation] = []
        self._undo_stack: list[CalculatorMemento] = []
        self._redo_stack: list[CalculatorMemento] = []

    def _save_state_to_undo(self):
        self._undo_stack.append(CalculatorMemento(self.history))
        self._redo_stack.clear()

    def add_calculation(self, calculation: Calculation):
        self._save_state_to_undo()
        self.history.append(calculation)
        if len(self.history) > CalculatorConfig.MAX_HISTORY_SIZE:
            self.history.pop(0)

    def undo(self) -> bool:
        if not self._undo_stack:
            return False
        self._redo_stack.append(CalculatorMemento(self.history))
        memento = self._undo_stack.pop()
        self.history = memento.get_state()
        return True

    def redo(self) -> bool:
        if not self._redo_stack:
            return False
        self._undo_stack.append(CalculatorMemento(self.history))
        memento = self._redo_stack.pop()
        self.history = memento.get_state()
        return True

    def clear(self):
        self._save_state_to_undo()
        self.history.clear()

    def save_to_csv(self, filepath=None):
        target = filepath or CalculatorConfig.HISTORY_FILE
        CalculatorConfig.ensure_directories()
        data = [c.to_dict() for c in self.history]
        df = pd.DataFrame(data, columns=["operation", "operand1", "operand2", "result", "timestamp"])
        df.to_csv(target, index=False, encoding=CalculatorConfig.DEFAULT_ENCODING)

    def load_from_csv(self, filepath=None):
        target = filepath or CalculatorConfig.HISTORY_FILE
        try:
            df = pd.read_csv(target, encoding=CalculatorConfig.DEFAULT_ENCODING)
            required = {"operation", "operand1", "operand2", "result", "timestamp"}
            if not required.issubset(set(df.columns)):
                raise OperationError("Malformed history file: Missing required columns.")

            self._save_state_to_undo()
            self.history = [Calculation.from_dict(row) for _, row in df.iterrows()]
        except FileNotFoundError:
            raise OperationError(f"History file not found at '{target}'.")
        except Exception as e:
            if isinstance(e, OperationError):
                raise
            raise OperationError(f"Failed to load history: {str(e)}")
