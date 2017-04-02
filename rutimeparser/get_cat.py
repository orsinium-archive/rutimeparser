'''
Содержит функции, которые либо возвращает значение ноды по переданному
ей слову, либо None. Имя функции является типом ноды (cat).
'''

from datetime import datetime, timedelta

from . import rules


def date(word):
	for rd in rules.dates:
		try:
			result = datetime.strptime(word, rd).date()
		except ValueError:
			pass
		else:
			return result
	
	if word in rules.from_now:
		delta = rules.from_now[word]
		return datetime.now().date() + timedelta(delta)

def time(word):
	for rd in rules.times:
		try:
			result = datetime.strptime(word, rd).time()
		except ValueError:
			pass
		else:
			return result
	
	if word in rules.times_of_day:
		hour = rules.times_of_day[word]
		return datetime(2000, 1, 1, hour).time()

def my_datetime(word):
	if word == 'сейчас':
		return datetime.now()
my_datetime.__name__ = 'datetime'

def number(word):
	if word.isdigit():
		return int(word)

def delta_offset(word):
	for offset, *words in rules.offset:
		if word in words:
			return offset

def delta_size(word):
	for result, words in rules.delta_sizes:
		if word in words:
			return result

def weekday(word):
	for ws in rules.weekdays:
		if word in ws:
			return ws.index(word)

def month(word):
	for ms in rules.months:
		if word in ms:
			return ms.index(word) + 1

fs = (date, time, number, delta_offset, delta_size, weekday, month, my_datetime)

def get_cat(word):
	'Принимает на вход слово и возвращает ноду'
	for f in fs:
		result = f(word)
		if result is not None:
			return f.__name__, result
	return 'junk', word
