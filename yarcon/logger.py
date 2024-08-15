import logging


class Logger:
    def __init__(self, debug_enabled=False):
        self.debug_enabled = debug_enabled

        self.__logger = logging.getLogger(__name__)
        self.__setup_handlers()

    def __setup_handlers(self):
        debug_level = "DEBUG" if self.debug_enabled else "INFO"
        self.__logger.setLevel(debug_level)

        formatter = self.__get_formatter()

        console_logger = logging.StreamHandler()
        console_logger.setFormatter(formatter)

        console_logger.setLevel(debug_level)
        self.__logger.addHandler(console_logger)

    def __get_formatter(self) -> logging.Formatter:
        formatter = logging.Formatter(
            "{asctime} - {levelname} - {message}",
            style="{",
            datefmt="%H:%M:%S",
        )

        return formatter

    def error(self, message: str):
        self.__logger.error(message)

    def info(self, message: str):
        self.__logger.info(message)

    def debug(self, message: str):
        self.__logger.debug(message)
