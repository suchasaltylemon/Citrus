import logging
import sys
from typing import Optional

FORMAT = "[%(asctime)s.%(msecs)03d] (%(name)s/%(levelname)s): %(message)s"
DATE_FORMAT = "%H:%M:%S"

_do_debug = False
_loggers = []
_do_logging = False


class _ErrorMessageFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return not (record.levelno >= logging.ERROR)


def logger(log_name: str):
    _logger = logging.getLogger(log_name)
    _logger.disabled = not _do_logging

    _logger.setLevel(logging.DEBUG if _do_debug else logging.INFO)
    _loggers.append(_logger)

    return _logger


def setup(path: Optional[str] = None, *, log_to_stream: Optional[bool] = False, do_debug: Optional[bool] = False):
    global _do_debug
    global _do_logging
    _do_debug = do_debug

    handlers = []

    if not log_to_stream and not path:
        return

    _do_logging = True

    if log_to_stream:
        error_handler = logging.StreamHandler(sys.stderr)
        error_handler.setLevel(logging.ERROR)

        std_out_handler = logging.StreamHandler(sys.stdout)
        std_out_handler.setLevel(logging.INFO if not do_debug else logging.DEBUG)

        error_filter = _ErrorMessageFilter("error_filter")
        std_out_handler.addFilter(error_filter)

        handlers.extend([std_out_handler, error_handler])

    if path is not None:
        file_handler = logging.FileHandler(path, mode="w")
        file_handler.setLevel(logging.INFO if not do_debug else logging.DEBUG)
        handlers.append(file_handler)

    logging.basicConfig(format=FORMAT, datefmt=DATE_FORMAT, handlers=handlers,
                        level=logging.INFO if not do_debug else logging.DEBUG)

    if do_debug:
        for created_logger in _loggers:
            created_logger.setLevel(logging.DEBUG)

    for _logger in _loggers:
        _logger.disabled = False
