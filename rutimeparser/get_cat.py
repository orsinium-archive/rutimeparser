'''
Содержит функции, которые либо возвращает значение ноды по переданному
ей слову, либо None. Имя функции является типом ноды (cat).
'''

from datetime import datetime, timedelta

from . import rules


def date(word, now):
    for rd in rules.dates:
        try:
            result = datetime.strptime(word, rd).date()
        except ValueError:
            pass
        else:
            return result

    if word in rules.from_now:
        delta = rules.from_now[word]
        return now.date() + timedelta(delta)


def time(word, **kwargs):
    for rd in rules.times:
        try:
            result = datetime.strptime(word, rd).time()
        except ValueError:
            pass
        else:
            return result

    if word in rules.times_of_day:
        hour = rules.times_of_day[word]
        dt = datetime(2000, 1, 1, hour).time()
        return dt


def my_datetime(word, now):
    if word == 'сейчас':
        return now


my_datetime.__name__ = 'datetime'


def number(word, **kwargs):
    if word.isdigit():
        return int(word)


def delta_offset(word, **kwargs):
    for offset, *words in rules.offset:
        if word in words:
            return offset


def delta_size(word, **kwargs):
    for result, words in rules.delta_sizes:
        if word in words:
            return result


def weekday(word, **kwargs):
    for ws in rules.weekdays:
        if word in ws:
            return ws.index(word)


def month(word, **kwargs):
    for ms in rules.months:
        if word in ms:
            return ms.index(word) + 1


fs = (date, time, number, delta_offset, delta_size, weekday, month, my_datetime)


def get_cat(word, now):
    'Принимает на вход слово и возвращает ноду'
    for f in fs:
        result = f(word, now=now)
        if result is not None:
            return f.__name__, result
    return 'junk', word
