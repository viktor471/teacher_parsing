import logging
from logging import Handler

unloaded_values = 'logs/unloaded_values.log'
class ConsoleOutput: pass

class Logger:
    def __init__(self, logger_name: str, level, handler: ConsoleOutput | "string with filename"):
        self._logger = logging.getLogger(logger_name)
        self._log_formatter = logging.Formatter('[%(asctime)s] %(message)s', datefmt='%d/%m/%Y %H:%M:%S')

        self.handler = handler
        self.handler.setLevel(level)

        self._logger.addHandler(handler)

    @property
    def handler(self):
        return self._handler

    @handler.setter
    def handler(self, handler: ConsoleOutput | "string with filename"):
        if handler is ConsoleOutput:
            self._handler = logging.StreamHandler()
        elif isinstance(handler, str):
            self._handler = logging.FileHandler(handler)
        elif isinstance(handler, Handler):
            self._handler = handler

        self._handler.setFormatter(self._log_formatter)

        return self._handler

    def info(self, msg, *args, **kwargs):
        self._logger.info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self._logger.warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self._logger.error(msg, *args, **kwargs)


class UnloadedValuesLog(Logger):
    def __init__(self):


file_handler = logging.FileHandler(unloaded_values)
file_handler.setFormatter(log_formatter)
file_handler.setLevel(logging.WARN)

#Setup Stream Handler (i.e. console)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(log_formatter)
stream_handler.setLevel(logging.INFO)

#Get our logger
log = logging.getLogger('root')
log.setLevel(logging.INFO)

#Add both Handlers
log.addHandler(file_handler)
log.addHandler(stream_handler)
