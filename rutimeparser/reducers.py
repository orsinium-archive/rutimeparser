from datetime import datetime, timedelta
from .utils import my_timedelta, Node, extract_word, extract_values

def number_and_month(nodes):
	'[22] [февраля]'
	number, month = extract_values(nodes, 'number', 'month')
	if not number:
		number = 1
	year = datetime.now().year
	value = datetime(year, month, number).date()
	if value < datetime.now().date():
		value = datetime(year + 1, month, number).date()
	return Node(nodes[0].i, 'date', extract_word(nodes), value)

def make_delta(nodes):
	'[1] [час]'
	number, size = extract_values(nodes, 'number', 'delta_size')
	if not number:
		number = 1
	value = my_timedelta(**{size: number})
	return Node(nodes[0].i, 'delta', extract_word(nodes), value)

def offset(nodes):
	'[неделю] [назад]'
	delta, offset = extract_values(nodes, 'delta', 'delta_offset')
	if offset < 0:
		delta.positive = False
	delta.is_absolute = False
	if offset == 1:
		delta.is_next = True
	return Node(nodes[0].i, 'delta', extract_word(nodes), delta)


def sum_delta(nodes):
	'[2 часа] [17 минут]'
	value = my_timedelta()
	for node in nodes:
		value += node.value
	return Node(nodes[0].i, 'delta', extract_word(nodes), value)
	
def date_and_time(nodes):
	'[22.02.2017] [17:45]'
	date, time = extract_values(nodes, 'date', 'time')
	if not date:
		date = extract_values(nodes, 'datetime')[0]
		if date:
			date = date.date()
		else:
			date = datetime.now().date()
	value = datetime.combine(date, time)
	return Node(nodes[0].i, 'datetime', extract_word(nodes), value)

def dt_and_delta(nodes):
	'[завтра утром] [через час]'
	dt, delta = extract_values(nodes, 'datetime', 'delta')
	if not dt:
		dt = datetime.now()
	value = delta + dt
	return Node(nodes[0].i, 'datetime', extract_word(nodes), value)

def date_and_delta(nodes):
	'[завтра утром] [через час]'
	date, delta = extract_values(nodes, 'date', 'delta')
	twilight = datetime(2000, 1, 1, 0, 0).time()
	value = delta + datetime.combine(date, twilight)
	if value.time() == twilight:
		value = value.date()
		cat = 'date'
	else:
		cat = 'datetime'
	return Node(nodes[0].i, cat, extract_word(nodes), value)

def weekday(nodes):
	'[в апреле] [в следующий] [вторник]'
	offset, wday, dt = extract_values(nodes, 'delta_offset', 'weekday', 'datetime')
	if not dt:
		dt = extract_values(nodes, 'date')[0]
		if not dt:
			dt = datetime.now().date()
	
	cat = 'datetime' if isinstance(dt, datetime) else 'date'
	
	dt_wday = datetime.weekday(dt)
	if (offset and offset == 1) \
	or cat == 'date' and dt != datetime.now().date() \
	or cat == 'datetime' and dt.date() != datetime.now().date():
		days = 7 - (dt_wday - wday) % 7
	else:
		days = wday - dt_wday
	value = dt + timedelta(days=days)
	if offset and offset == -1:
		value -= timedelta(days=7)
	
	return Node(nodes[0].i, cat, extract_word(nodes), value)


templates = (
	(number_and_month, 'number', 'month'), # -> date
	(number_and_month, 'month'), # -> date
	
	(make_delta, 'number', 'delta_size'), # -> delta
	(make_delta, 'number', 'delta_size'), # -> delta
	(make_delta, 'delta_size'), # -> delta
	
	(sum_delta, 'delta', 'delta'), # -> delta
	(sum_delta, 'delta', 'delta'), # -> delta
	
	(offset, 'delta_offset', 'delta'), # -> delta
	(offset, 'delta', 'delta_offset'), # -> delta
	
	(date_and_time, 'date', 'time'), # -> datetime
	(date_and_time, 'time', 'date'), # -> datetime
	
	(dt_and_delta, 'datetime', 'delta'), # -> datetime
	(dt_and_delta, 'delta', 'datetime'), # -> datetime
	(date_and_delta, 'date', 'delta'), # -> datetime/date
	(date_and_delta, 'delta', 'date'), # -> datetime/date
	
	(dt_and_delta, 'delta'), # -> datetime
	
	(weekday, 'delta_offset', 'weekday', 'datetime'), # -> datetime
	(weekday, 'datetime', 'delta_offset', 'weekday'), # -> datetime
	(weekday, 'delta_offset', 'weekday', 'date'), # -> date
	(weekday, 'date', 'delta_offset', 'weekday'), # -> date
	(weekday, 'delta_offset', 'weekday'), # -> date
	
	(weekday, 'weekday', 'datetime'), # -> datetime
	(weekday, 'datetime', 'weekday'), # -> datetime
	(weekday, 'weekday', 'date'), # -> date
	(weekday, 'date', 'weekday'), # -> date
	(weekday, 'weekday'), # -> date
	
	(date_and_time, 'date', 'time'), # -> datetime
	(date_and_time, 'time', 'date'), # -> datetime
	(date_and_time, 'datetime', 'time'), # -> datetime
	(date_and_time, 'time', 'datetime'), # -> datetime
	(date_and_time, 'time'), # -> datetime
	)
