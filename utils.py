import calendar
import datetime

from collections import namedtuple
Node = namedtuple('Node', ['i', 'cat', 'word', 'value'])


def ngrams(l, n):
	'Возвращает n-грамы из списка'
	return zip(*[l[i:] for i in range(n)])


def extract_word(nodes):
	'Извлекает и объединяет все слова из переданных нод'
	return ' '.join([node.word for node in nodes])

def extract_values(nodes, *template):
	'''
	Возвращает список значений в соответствии со списком типов нод.
	Если ноды соответствующего типа нет среди переданных, возвращает
	в соответствующей позиции None.
	'''
	result = dict.fromkeys(template)
	for node in nodes:
		if node.cat in result:
			result[node.cat] = node.value
	return [result[cat] for cat in template]


def add_delta2datetime(sourcedate, years=0, months=0, weeks=0, days=0, hours=0, minutes=0, seconds=0):
	'''
	Прибавляет заданное значение к datetime. В отличиче от timedelta,
	может принимать недели, месяцы и годы.
	'''
	days += weeks * 7
	
	seconds = sourcedate.second + seconds
	minutes += seconds // 60
	seconds = seconds % 60
	
	minutes = sourcedate.minute + minutes
	hours += minutes // 60
	minutes = minutes % 60
	
	hours = sourcedate.hour + hours
	days += hours // 24
	hours = hours % 24
	
	month = sourcedate.month - 1 + months
	year = sourcedate.year + month // 12 + years
	month = month % 12 + 1
	
	day = sourcedate.day + days
	days_limit = calendar.monthrange(year, month)[1]
	while day > days_limit:
		month += 1
		if month > 12:
			month = 1
			year += 1
		day = day - days_limit
		days_limit = calendar.monthrange(year, month)[1]
	
	return datetime.datetime(year, month, day, hours, minutes, seconds)


class my_timedelta:
	'''
	Класс для работы с add_delta2datetime. Альтернатива типу timedelta,
	который не умеет работать с неделями, месяцами и годами.
	'''
	
	def __init__(self, **kwargs):
		self.elements = []
		self.positive = True
		if kwargs:
			self.elements.append(kwargs)
	
	def __add__(self, obj):
		'''
		Прибавление timedelta или my_timedelta добавляет его в self.elements.
		Прибавление datetime/date складывает с ним self.elements
		с помощью add_delta2datetime.
		'''
		if isinstance(obj, datetime.timedelta):
			new = my_timedelta()
			new.elements = self.elements.copy()
			new.elements.append(obj)
			return new
		if isinstance(obj, my_timedelta):
			new = my_timedelta()
			new.elements = self.elements.copy()
			new.elements.extend(obj.elements)
			return new
		for el in self.elements:
			# +dict
			if type(el) is dict:
				if not self.positive:
					el = {k: -v for k, v in el.items()}
				obj = add_delta2datetime(obj, **el)
			# +timedelta
			else:
				if self.positive:
					obj = obj + el
				else:
					obj = obj - el
		return obj
	
	def __str__(self):
		return str(self.elements)
	
	def __list__(self):
		return self.elements
