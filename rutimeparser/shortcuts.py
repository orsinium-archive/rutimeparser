from .core import TimeParser


__all__ = ['parse_time', 'get_clear_text', 'get_last_clear_text']


def parse_time(text, *, tz=None, now=None, remove_junk=True):
    """
    Для тех, кто не любит классы. Выполняет все необходимые операции
    с текстом и возвращает результат.
    """
    parser = TimeParser(text, tz=tz, now=now)
    if remove_junk:
        parser.remove_junk()
    return parser.parse()


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
