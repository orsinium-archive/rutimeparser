from get_words import get_words
from get_cat import get_cat
from utils import ngrams, Node
from reducers import templates
from datetime import datetime

class TimeParser:
	'''
	Класс для получения из текста на естественном языке даты и времени.
	Возвращает datetime, date или None.
	'''
	
	def __init__(self, text='', words=None):
		if not words:
			if not text:
				raise ValueError('Please, set text or words for TimeParser.')
			self.words = tuple(get_words(text))
		else:
			self.words = words
	
	def make_nodes(self):
		'''
		Генерирует список нод на основе слов исходного текста
		'''
		
		self.nodes = []
		for i, word in enumerate(self.words):
			cat, value = get_cat(word)
			self.nodes.append(Node(i, cat, word, value))
		return self.nodes
	
	def get_nodes_by_template(self, *template):
		'''
		Возвращает списки нод, соответствующих переданному списку категорий
		'''
		
		def test(nodes, template):
			'''
			Проверяет список нод на соответствие шаблону
			'''
			if len(nodes) < len(template):
				return False
			for node, cat in zip(nodes, template):
				if node.cat != cat:
					return False
			return True
		
		n = len(template)
		for nodes in ngrams(self.nodes, n):
			if test(nodes, template):
				yield nodes
	
	def replace(self, node_from, node_to, new_node):
		'''
		Заменяет диапазон нод новой нодой
		'''
		new_nodes = []
		for node in self.nodes:
			if node.i < node_from.i or node.i > node_to.i:
				new_nodes.append(node)
			elif node.i == node_from.i:
				new_nodes.append(new_node)
		self.nodes = new_nodes
		return new_nodes
	
	def remove_junk(self):
		'''
		Удаляет из текста все слова, не связанные с датой и временем
		'''
		self.nodes = [node for node in self.nodes if node.cat != 'junk']
	
	def reduce(self):
		'''
		Объединяет несколько нод в одну по заданным правилам
		'''
		for f, *template in templates:
			nodes_samples = list(self.get_nodes_by_template(*template))
			for nodes in nodes_samples:
				new_node = f(nodes)
				self.replace(nodes[0], nodes[-1], new_node)
	
	def __dict__(self):
		'''
		Возвращает словарь "категория_ноды: значение_ноды"
		'''
		return {node.cat: node.value for node in self.nodes}
	
	def get_datetime(self):
		'''
		Возвращает результат на основе обработанных нод
		'''
		nodes = self.__dict__()
		if 'datetime' in nodes:
			return nodes['datetime']
		now = datetime.now()
		if 'date' in nodes and 'time' in nodes:
			return datetime.combine(nodes['date'], nodes['time'])
		if 'time' in nodes:
			return datetime.combine(now.date(), nodes['time'])
		if 'date' in nodes:
			return nodes['date']


def parse_time(text, remove_junk=True, debug=False):
	'''
	Для тех, кто не любит классы. Выполняет все необходимые операции
	с текстом и возвращает результат.
	'''
	tp = TimeParser(text)
	tp.make_nodes()
	if debug:
		from pprint import pprint
		pprint(tp.nodes)
	if remove_junk:
		tp.remove_junk()
	tp.reduce()
	return tp.get_datetime()


if __name__ == '__main__':
	for test in open('test_strings', 'r'):
		print(test.strip(), '\x1B[31m', parse_time(test), '\x1B[0m')
