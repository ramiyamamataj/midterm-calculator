import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class CalculatorConfig:
    LOG_DIR: Path = Path(os.getenv("CALCULATOR_LOG_DIR", "logs"))
    HISTORY_DIR: Path = Path(os.getenv("CALCULATOR_HISTORY_DIR", "history_data"))
    LOG_FILE: Path = Path(os.getenv("CALCULATOR_LOG_FILE", "logs/calculator.log"))
    HISTORY_FILE: Path = Path(os.getenv("CALCULATOR_HISTORY_FILE", "history_data/calculator_history.csv"))

    MAX_HISTORY_SIZE: int = int(os.getenv("CALCULATOR_MAX_HISTORY_SIZE", "100"))
    AUTO_SAVE: bool = os.getenv("CALCULATOR_AUTO_SAVE", "true").lower() in ("true", "1", "yes")
    PRECISION: int = int(os.getenv("CALCULATOR_PRECISION", "4"))
    MAX_INPUT_VALUE: float = float(os.getenv("CALCULATOR_MAX_INPUT_VALUE", "1000000000"))
    DEFAULT_ENCODING: str = os.getenv("CALCULATOR_DEFAULT_ENCODING", "utf-8")

    @classmethod
    def ensure_directories(cls):
        cls.LOG_DIR.mkdir(parents=True, exist_ok=True)
        cls.HISTORY_DIR.mkdir(parents=True, exist_ok=True)
