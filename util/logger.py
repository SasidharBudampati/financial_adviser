from typing import Optional
from beeai_framework.logger import Logger

# Configure logger with default log level

def get_logger(name: str, level: Optional="Debug") -> Logger:
    return Logger(name=name)
