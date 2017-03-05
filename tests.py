import unittest
from main import parse_time
from datetime import datetime, timedelta

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


class TestDate(unittest.TestCase):
	
	def compare(self, result, good):
		good_floor = good - timedelta(seconds=2)
		good_ceil = good + timedelta(seconds=2)
		
		if isinstance(good, datetime):
			good_floor = good_floor.date()
			good_ceil = good_ceil.date()
		
		self.assertGreaterEqual(result, good_floor)
		self.assertLessEqual(result, good_ceil)
	
	def test_today(self):
		good = datetime.now()
		for text in make_mutations('сегодня'):
			with self.subTest(text=text):
				result = parse_time(text)
				self.compare(result, good)
	
	def test_tomorrow(self):
		good = datetime.now() + timedelta(days=1)
		for text in make_mutations('завтра'):
			with self.subTest(text=text):
				result = parse_time(text)
				self.compare(result, good)
	
	def test_yesterday(self):
		good = datetime.now() - timedelta(days=1)
		for text in make_mutations('вчера'):
			with self.subTest(text=text):
				result = parse_time(text)
				self.compare(result, good)
	
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
