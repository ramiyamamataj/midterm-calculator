import logging
from app.calculator_config import CalculatorConfig

class Logger:
    _configured = False

    @classmethod
    def get_logger(cls) -> logging.Logger:
        logger = logging.getLogger("calculator_app")
        if not cls._configured:
            CalculatorConfig.ensure_directories()
            logger.setLevel(logging.INFO)
            handler = logging.FileHandler(CalculatorConfig.LOG_FILE, encoding=CalculatorConfig.DEFAULT_ENCODING)
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            cls._configured = True
        return logger
