import unittest
from main import parse_time
from datetime import datetime, timedelta, time

templates = (
	'Я приеду {}',
	'Вызови такси {}. Мне нужно будет съездить в ленту',
	'Напомни мне {} купить билеты',
	'Что у меня запланировано на {}?',
	'Напомни {} купить 10 яиц и 2 литра молока.',
	)

def make_mutations(*texts):
	for text in texts:
		cases = text, text.title(), text.upper()
		for case in cases:
			yield case
			for template in templates:
				yield template.format(case)


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
	
	('28.02.2017 17:45', datetime(2017, 2, 28, 17, 45), False),
	('2017-02-28 18:49', datetime(2017, 2, 28, 18, 49), False),
	
	('сейчас', datetime.now(), False),
	('через час', datetime.now() + timedelta(hours=1), False),
	('через полчаса', datetime.now() + timedelta(minutes=30), False),
	('через полтора часа', datetime.now() + timedelta(hours=1, minutes=30), False),
	('через 2 часа', datetime.now() + timedelta(hours=2), False),
	('через два часа', datetime.now() + timedelta(hours=2), False),
	('через 3 часа 19 минут', datetime.now() + timedelta(hours=3, minutes=19), False),
	('через три часа девятнадцать минут', datetime.now() + timedelta(hours=3, minutes=19), False),
	
	('час назад', datetime.now() - timedelta(hours=1), False),
	('полчаса назад', datetime.now() - timedelta(minutes=30), False),
	('полтора часа назад', datetime.now() - timedelta(hours=1, minutes=30), False),
	('2 часа назад', datetime.now() - timedelta(hours=2), False),
	('два часа назад', datetime.now() - timedelta(hours=2), False),
	('2 часа 17 минут назад', datetime.now() - timedelta(hours=2, minutes=17), False),
	('два часа семнадцать минут назад', datetime.now() - timedelta(hours=2, minutes=17), False),
	
	('утром', morning, False),
	('сегодня утром', morning, False),
	('завтра утром', morning + timedelta(days=1), False),
	('вчера утром', morning - timedelta(days=1), False),
	
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
	
	('в три часа', morning - timedelta(hours=6), False)
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
			for text in make_mutations(src_text):
				with self.subTest(src_text=src_text, text=text):
					result = parse_time(text)
					self.compare(result, good, is_date)


class TestDate(unittest.TestCase):
	
	def compare(self, result, good):
		good_floor = good - timedelta(seconds=2)
		good_ceil = good + timedelta(seconds=2)
		if isinstance(good, datetime):
			good_floor = good_floor.date()
			good_ceil = good_ceil.date()
		self.assertGreaterEqual(result, good_floor)
		self.assertLessEqual(result, good_ceil)
	
	def test_december(self):
		year = datetime.now().year
		good = datetime(year, 12, 1)
		if good < datetime.now():
			good = datetime(year + 1, 12, 1)
		for text in make_mutations('в декабре', '1 декабря'):
			with self.subTest(text=text):
				result = parse_time(text)
				self.compare(result, good)
	
	def test_january(self):
		year = datetime.now().year
		good = datetime(year, 1, 1)
		if good < datetime.now():
			good = datetime(year + 1, 1, 1)
		for text in make_mutations('в январе', '1 января'):
			with self.subTest(text=text):
				result = parse_time(text)
				self.compare(result, good)


if __name__ == '__main__':
    unittest.main()
