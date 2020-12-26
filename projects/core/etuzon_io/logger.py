"""
@author: Eyal Tuzon
"""

from enum import Enum
from inspect import stack
from logging import ERROR, CRITICAL, WARN, INFO, DEBUG
import logging
import ntpath
import os

from projects.core.exceptions.core_exceptions import ApplicationException


class LoggerFormatterEnum(Enum):
    BASIC = 'Basic'
    DETAILED = 'Detailed'


class LogLevelEnum(Enum):
    """
    Colors of each log level
    """

    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARN = logging.WARN
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL
    EXCEPTION = logging.CRITICAL


def _create_log_directory_if_not_exists(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)


def _create_empty_logger_file(file_path):
    if file_path:
        file = os.path.join(file_path)
        directory = os.path.dirname(file)

        if not os.path.exists(directory):
            os.makedirs(directory)


class ApplicationLogger(object):
    """
    Application logger
    """

    BASIC_FORMATTER = '%(asctime)s [%(levelname)s] %(message)s'
    DETAILED_FORMATTER = '%(asctime)s - ' \
                         '[%(filename2)s:%(functionname)s:%(linenumber)s] ' \
                         '[%(levelname)s] %(message)s'

    LOGS_MAIN_DIRECTORY = './logs/'
    OLD_DIRECTORY = LOGS_MAIN_DIRECTORY + 'old/'

    _instance = None
    _is_closed = False
    _is_init: bool
    _logger = None

    def __init__(
            self,
            console_log_level=LogLevelEnum.INFO,
            file_log_level=LogLevelEnum.DEBUG,
            console_formatter: LoggerFormatterEnum = None,
            file_path=None,
            file_formatter: LoggerFormatterEnum = None):
        """
        Constructor
        """
        if ApplicationLogger._instance:
            ApplicationLogger._instance.info(
                'Constructor should not run more than one time.'
                ' Please use get_instance()')
            return

        ApplicationLogger._instance = self
        self._is_init = False
        self.console_log_level = console_log_level
        self.file_log_level = file_log_level
        _create_empty_logger_file(file_path)
        self._create_logger(console_log_level)
        self._set_console_handler(console_log_level)
        self._set_logging_file_handler(file_path, file_log_level)
        self._set_formatter(console_formatter, file_formatter)
        self._add_handlers_to_logging()
        self._init_logger_adapter()
        self._is_init = True

    @classmethod
    def get_instance(cls):
        if ApplicationLogger._instance is None:
            raise ApplicationException(
                f'Bug: {cls.__name__} was not initiated'
                ' so cannot get active instance.\n'
                'Constructor should be run one time'
                ' before calling to get_instance()')
        return ApplicationLogger._instance

    @staticmethod
    def is_instance():
        return True if ApplicationLogger._instance else False

    @staticmethod
    def destroy():
        ApplicationLogger._instance = None

    def debug(self, msg):
        self._log(DEBUG, msg)

    def info(self, msg):
        self._log(INFO, msg)

    def warn(self, msg):
        self._log(WARN, msg)

    def error(self, msg):
        self._log(ERROR, msg)

    def critical(self, msg):
        self._log(CRITICAL, msg)

    def exception(self, msg):
        self._log(ERROR, msg)

    @property
    def is_logger_init(self) -> bool:
        return self._is_init

    def close(self):
        self._is_closed = True
        handlers = self._logger.handlers[:]

        for handler in handlers:
            handler.close()
            self._logger.removeHandler(handler)

    @property
    def is_logger_closed(self):
        return self._is_closed

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def _log(self, level, msg):
        self._validate_logger_not_closed()
        self.logger_adapter.log(level, msg, self.extra)

    def _validate_logger_not_closed(self):
        if self.is_logger_closed:
            raise ApplicationException('Logger is closed')

    def _create_logger(self, console_log_level):
        self._logger = logging.getLogger('Logger')
        self._logger.setLevel(console_log_level.value)

    def _set_console_handler(self, console_log_level):
        ch = logging.StreamHandler()
        ch.setLevel(console_log_level.value)
        self.console_handler = ch

    def _set_logging_file_handler(self, file_path, file_log_level):
        if file_path:
            _create_log_directory_if_not_exists(file_path)
            fh = logging.FileHandler(file_path, mode='w', encoding='utf-8')
            fh.setLevel(file_log_level.value)
            self.file_handler = fh
        else:
            self.file_handler = None

    def _set_formatter(self, console_formatter, file_formatter):
        if console_formatter is None:
            console_formatter = LoggerFormatterEnum.BASIC

        self.console_handler.setFormatter(
            self._get_formatter(console_formatter))

        if self.file_handler:
            if file_formatter is None:
                file_formatter = LoggerFormatterEnum.DETAILED

            self.file_handler.setFormatter(self._get_formatter(file_formatter))

    def _init_logger_adapter(self):
        self._set_extra()
        self.logger_adapter = logging.LoggerAdapter(self._logger, self.extra)

    def _set_extra(self):
        s = stack()
        row_index = 3
        file_name = ntpath.basename(s[row_index][1])

        if file_name == 'logger.py':
            row_index = 4
            file_name = ntpath.basename(s[row_index][1])

        line_number = str(s[row_index][2])
        function_name = s[row_index][3]

        self.extra = {
            'filename2': file_name,
            'linenumber': line_number,
            'functionname': function_name
        }

    def _get_formatter(self, formatter_type):
        if formatter_type == LoggerFormatterEnum.BASIC:
            return logging.Formatter(self.BASIC_FORMATTER)
        elif formatter_type == LoggerFormatterEnum.DETAILED:
            return logging.Formatter(self.DETAILED_FORMATTER)

        raise ApplicationException(
            f'Unable to get log formatter. Formatter Type [{formatter_type}]'
            ' is not one of LoggerFormatterEnum values')

    def _add_handlers_to_logging(self):
        self._logger.addHandler(self.console_handler)
        if self.file_handler:
            self._logger.addHandler(self.file_handler)


def logger() -> ApplicationLogger:
    return ApplicationLogger.get_instance()


def init_logger(console_log_level=LogLevelEnum.INFO,
                file_log_level=LogLevelEnum.DEBUG,
                console_formatter: LoggerFormatterEnum = None, file_path=None,
                file_formatter: LoggerFormatterEnum = None):
    if not ApplicationLogger.is_instance():
        ApplicationLogger(console_log_level, file_log_level,
                          console_formatter, file_path, file_formatter)
