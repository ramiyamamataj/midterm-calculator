from copy import deepcopy
from app.calculation import Calculation

class CalculatorMemento:
    def __init__(self, history: list[Calculation]):
        self._state = deepcopy(history)

    def get_state(self) -> list[Calculation]:
        return deepcopy(self._state)
