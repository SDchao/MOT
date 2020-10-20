import loguru
import sys

logger = loguru.logger

logger.add("error.log", rotation="50 MB", level="ERROR")

