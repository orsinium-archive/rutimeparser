from datetime import datetime, date, time
import warnings

from .core import TimeParser


__all__ = ['parse', 'parse_time', 'get_clear_text', 'get_last_clear_text']


def parse(words, tz=None, now=None, remove_junk=True,
          allowed_results=(datetime, date, time, None),
          default_time=time(9, 0), default_datetime=None):
    """
    Выполняет все необходимые операции с текстом и возвращает результат.
    """
    parser = TimeParser(
        words, tz=tz, now=now,
        allowed_results=allowed_results,
        default_time=default_time, default_datetime=default_datetime,
    )
    if remove_junk:
        parser.remove_junk()
    return parser.parse()


def parse_time(*args, **kwargs):
    warnings.warn(
        "parse_time function deprecated. Use parse function instead",
        DeprecationWarning,
    )
    return parse(*args, **kwargs)


def get_clear_text(text):
    """
    Возвращает фрагменты, не связанные с датой и временем
    """
    parser = TimeParser(text)
    return parser.get_clear_text()


def get_last_clear_text(text):
    """
    Возвращает последний фрагмент, не связанный с датой и временем
    """
    parser = TimeParser(text)
    return parser.get_last_clear_text()
