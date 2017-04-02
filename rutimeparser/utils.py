import calendar
import datetime
from pytz import timezone

from collections import namedtuple
Node = namedtuple('Node', ['i', 'cat', 'word', 'value'])

def get_now(tz):
	if tz:
		now = datetime.datetime.utcnow()
	else:
		now = datetime.datetime.now()
	
	#убрать микросекунды:
	t = now.time()
	t = datetime.time(t.hour, t.minute, t.second)
	now = datetime.datetime.combine(now.date(), t)
	
	if not tz:
		return now
	return timezone(tz).fromutc(now)


def change_timezone(dt, tz):
	'Изменить часовой пояс для datetime/time'
	if not tz:
		return dt
	if dt.tzname():
		#изменить часовой пояс
		return dt.astimezone(timezone(tz))
	else:
		#установить часовой пояс
		return timezone(tz).localize(dt, is_dst=None)


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
	
	seconds = getattr(sourcedate, 'second', 0) + seconds
	minutes += seconds // 60
	seconds = seconds % 60
	
	minutes = getattr(sourcedate, 'minute', 0) + minutes
	hours += minutes // 60
	minutes = minutes % 60
	
	hours = getattr(sourcedate, 'hour', 0) + hours
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
	
	is_datetime = isinstance(sourcedate, datetime.datetime)
	if any([is_datetime, hours, minutes, seconds]):
		return datetime.datetime(year, month, day, hours, minutes, seconds)
	else:
		return datetime.date(year, month, day)


def annihilator(sourcedate, delta_sizes, offset=0):
	i = 10
	for delta_size in delta_sizes:
		if delta_size == 'weeks':
			continue
		i = min(i, annihilator.sizes.index(delta_size))
	i -= offset
	
	#если обнуляем по неделе - приводим дату к понедельнику этой недели
	if i >= 2 and 'weeks' in delta_sizes:
		sd_wday = datetime.datetime.weekday(sourcedate)
		sourcedate = sourcedate - datetime.timedelta(days=sd_wday)
		return sourcedate.date()
	
	#не должно происходить, но на всякий случай
	if i == 10:
		return sourcedate
	
	#создаём timetuple с обнуленными значениями
	default = (0, 1, 1, 0, 0, 0)
	sourcedate = sourcedate.timetuple()
	if len(sourcedate) == 3:
		sourcedate = sourcedate + (0, 0, 0)
	result = sourcedate[:i+1] +  default[i+1:]
	
	if i >= 3:
		return datetime.datetime(*result)
	else:
		return datetime.date(*result[:-3])
annihilator.sizes = ('years', 'months', 'days', 'hours', 'minutes', 'seconds')


class my_timedelta:
	'''
	Класс для работы с add_delta2datetime. Альтернатива типу timedelta,
	который не умеет работать с неделями, месяцами и годами.
	'''
	
	def __init__(self, **kwargs):
		self.elements = []
		self.positive = True
		self.is_absolute = True
		self.is_next = False
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
		
		#если "следующий [месяц]", обнуляем всё, что меньше [месяц]
		if self.is_absolute:
			obj = annihilator(obj, self.elements[0].keys(), offset=1)
		if self.is_next:
			obj = annihilator(obj, self.elements[0].keys())
		
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
