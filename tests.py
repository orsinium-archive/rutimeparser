import unittest
from main import parse_time
from datetime import datetime, timedelta, time

templates = (
	'Я приеду {}',
	'Вызови такси {}. Мне нужно будет съездить в ленту',
	'Напомни мне {} купить билеты',
	'Что у меня запланировано {}?',
	'Напомни {} купить 10 яиц и 2 литра молока.',
	)

def make_mutations(*texts):
	for text in texts:
		cases = text, text.title(), text.upper()
		for case in cases:
			yield case
			for template in templates:
				yield template.format(case)


def date_with_year(month, day):
	now = datetime.now()
	result = datetime(now.year, month, day).date()
	if result >= now.date():
		return result
	else:
		return datetime(now.year+1, month, day).date()

def datetime_with_year(month, day, hours=0, minutes=0, seconds=0):
	d = date_with_year(month, day)
	t = time(hours, minutes, seconds)
	return datetime.combine(d, t)

now = datetime.now()
morning = datetime.combine(now.date(), time(9, 0))
monday = now - timedelta(days=datetime.weekday(now))
monday_morning = datetime.combine(monday.date(), morning.time())

common_tests = (
	('сегодня', now, True),
	('завтра', now + timedelta(days=1), True),
	('вчера', now - timedelta(days=1), True),
	('послезавтра', now + timedelta(days=2), True),
	('позавчера', now - timedelta(days=2), True),
	
	('в декабре', date_with_year(12, 1), True),
	('1 декабря', date_with_year(12, 1), True),
	('в январе', date_with_year(1, 1), True),
	('1 января', date_with_year(1, 1), True),
	('28.02.2017 17:45', datetime(2017, 2, 28, 17, 45), False),
	('2017-02-28 18:49', datetime(2017, 2, 28, 18, 49), False),
	('18 февраля в 17:49', datetime_with_year(2, 18, 17, 49), False),
	('31 декабря в 17:49', datetime_with_year(12, 31, 17, 49), False),
	
	('сейчас', now, False),
	('через час', now + timedelta(hours=1), False),
	('через полчаса', now + timedelta(minutes=30), False),
	('через полтора часа', now + timedelta(hours=1, minutes=30), False),
	('через 2 часа', now + timedelta(hours=2), False),
	('через два часа', now + timedelta(hours=2), False),
	('через 3 часа 19 минут', now + timedelta(hours=3, minutes=19), False),
	('через три часа девятнадцать минут', now + timedelta(hours=3, minutes=19), False),
	
	('час назад', now - timedelta(hours=1), False),
	('полчаса назад', now - timedelta(minutes=30), False),
	('полтора часа назад', now - timedelta(hours=1, minutes=30), False),
	('2 часа назад', now - timedelta(hours=2), False),
	('два часа назад', now - timedelta(hours=2), False),
	('2 часа 17 минут назад', now - timedelta(hours=2, minutes=17), False),
	('два часа семнадцать минут назад', now - timedelta(hours=2, minutes=17), False),
	
	('через день 2 часа', now + timedelta(days=1, hours=2), False),
	('через 2 дня 3 часа', now + timedelta(days=2, hours=3), False),
	
	('через день', now + timedelta(days=1), False),
	('через 2 дня', now + timedelta(days=2), False),
	('через неделю', now + timedelta(days=7), False),
	('через 2 недели', now + timedelta(days=14), False),
	('через 2 недели в 17:39', datetime.combine(now.date(), time(17, 39)) + timedelta(days=14), False),
	
	('утром', morning, False),
	('сегодня утром', morning, False),
	('завтра утром', morning + timedelta(days=1), False),
	('вчера утром', morning - timedelta(days=1), False),
	('28.02.2017 утром', datetime(2017, 2, 28, 9, 0), False),
	
	('завтра в десять часов', morning + timedelta(days=1, hours=1), False),
	('завтра в 10 часов 14 минут', morning + timedelta(days=1, hours=1, minutes=14), False),
	('послезавтра в 10 часов 17 минут', morning + timedelta(days=2, hours=1, minutes=17), False),
	('послезавтра в 10:17', morning + timedelta(days=2, hours=1, minutes=17), False),
	
	('в понедельник', monday, True),
	('в следующий понедельник', monday + timedelta(days=7), True),
	('в предыдущий понедельник', monday - timedelta(days=7), True),
	('в среду', monday + timedelta(days=2), True),
	('в следующую среду', monday + timedelta(days=9), True),
	('в предыдущую среду', monday - timedelta(days=5), True),
	('на следующей неделе в среду', monday + timedelta(days=9), True),
	('на следующей неделе', monday + timedelta(days=7), True),
	
	('в следующий час', datetime.combine(now.date(), time(now.hour+1, 0)), False),
	('в следующий час в 15 минут', datetime.combine(now.date(), time(now.hour+1, 15)), False),
	('на следующий день', now + timedelta(days=1), True),
	('в следующем месяце', datetime(now.year, now.month+1, 1, 0, 0).date(), True),
	
	('в три часа', morning - timedelta(hours=6), False),
	)


class TestParser(unittest.TestCase):
	
	def compare(self, result, good, is_date):
		good_floor = good - timedelta(seconds=2)
		good_ceil = good + timedelta(seconds=2)
		if is_date and isinstance(good, datetime):
			good_floor = good_floor.date()
			good_ceil = good_ceil.date()
		self.assertGreaterEqual(result, good_floor)
		self.assertLessEqual(result, good_ceil)
	
	def test_common(self):
		for src_text, good, is_date in common_tests:
			with self.subTest(src_text=src_text):
				for text in make_mutations(src_text):
					result = parse_time(text)
					self.compare(result, good, is_date)
	
	def test_delta(self):
		texts = (
			'8 апреля у меня поезд. Напомни за день.',
			'9 апреля у меня поезд. Напомни за 2 дня.',
			'6 апреля через день',
			)
		year = now.year
		good = datetime(year, 4, 7)
		if good < now:
			good = datetime(year + 1, 4, 7)
		for text in make_mutations(*texts):
			with self.subTest(text=text):
				result = parse_time(text)
				self.compare(result, good, True)
	
	def test_weekday(self):
		year = now.year
		good = datetime(year, 4, 1).date()
		if good < now.date():
			good = datetime(year + 1, 4, 1).date()
		
		wd = datetime.weekday(good)
		days = 7 - (wd - 2) % 7
		good = good + timedelta(days=days)
		
		for text in make_mutations('в апреле в среду'):
			with self.subTest(text=text):
				result = parse_time(text)
				self.compare(result, good, True)
	
	def test_weekday_and_time(self):
		good = datetime(now.year, 4, 1, 17, 43)
		if good < now:
			good = datetime(now.year+1, 4, 1, 17, 43)
		
		wd = datetime.weekday(good)
		days = 7 - (wd - 3) % 7
		good = good + timedelta(days=days)
		
		src_text = 'в апреле в четверг в 17:43'
		with self.subTest(text=src_text):
			for text in make_mutations(src_text):
				result = parse_time(text)
				self.compare(result, good, False)


if __name__ == '__main__':
    unittest.main()
