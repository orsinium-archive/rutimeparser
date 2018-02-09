from .core import TimeParser


__all__ = ['parse_time', 'get_clear_text', 'get_last_clear_text']


def parse_time(text, *, tz=None, now=None, remove_junk=True, debug=False):
    """
    Для тех, кто не любит классы. Выполняет все необходимые операции
    с текстом и возвращает результат.
    """
    tp = TimeParser(text, tz=tz, now=now)
    tp.make_nodes()
    if debug:
        from pprint import pprint
        pprint(tp.nodes)
    if remove_junk:
        tp.remove_junk()
    tp.reduce()
    return tp.get_datetime()


def get_clear_text(text, debug=False):
    """
    Возвращает фрагменты, не связанные с датой и временем
    """
    tp = TimeParser(text)
    tp.make_nodes()
    if debug:
        from pprint import pprint
        pprint(tp.nodes)
    return tp.get_clear_text()


def get_last_clear_text(text, debug=False):
    """
    Возвращает последний фрагмент, не связанный с датой и временем
    """
    tp = TimeParser(text)
    tp.make_nodes()
    if debug:
        from pprint import pprint
        pprint(tp.nodes)
    return tp.get_last_clear_text()
