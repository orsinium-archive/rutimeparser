from datetime import datetime, date, time

from .get_words import get_words
from .get_cat import get_cat
from .utils import ngrams, Node, get_now, change_timezone
from .reducers import templates


class TimeParser(object):
    """
    Класс для получения из текста на естественном языке даты и времени.
    Возвращает datetime, date или None.
    """

    allowed_results = (datetime, date, time, None)
    default_time = time(9, 0)

    def __init__(self, text='', words=None, tz=None, now=None):
        self.nodes = []
        if not words:
            if not text:
                raise ValueError('Please, set text or words for TimeParser.')
            self.words = tuple(get_words(text))
        else:
            self.words = words

        self.tz = tz
        self.now = now if now else get_now(self.tz)

        if not self.tz and now and now.tzinfo:
            self.tz = str(now.tzinfo)

    def make_nodes(self):
        """
        Генерирует список нод на основе слов исходного текста
        """
        self.nodes = []
        for i, word in enumerate(self.words):
            cat, value = get_cat(word, self.now)
            self.nodes.append(Node(i, cat, word, value))
        return self.nodes

    def get_nodes_by_template(self, *template):
        """
        Возвращает списки нод, соответствующих переданному списку категорий
        """

        def test(nodes, template):
            """
            Проверяет список нод на соответствие шаблону
            """
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
        """
        Заменяет диапазон нод новой нодой
        """
        new_nodes = []
        for node in self.nodes:
            if node.i < node_from.i or node.i > node_to.i:
                new_nodes.append(node)
            elif node.i == node_from.i:
                new_nodes.append(new_node)
        self.nodes = new_nodes
        return new_nodes

    def get_junk_chains(self):
        chains = []
        chain = []
        for node in self.nodes:
            if node.cat == 'junk':
                chain.append(node)
            else:
                chains.append(chain)
                chain = []
        chains.append(chain)

        good_chains = []
        for chain in chains:
            if len(chain) > 2 or any([len(node.word) > 3 for node in chain]):
                good_chains.append(chain)
        return good_chains

    def remove_junk(self):
        """
        Удаляет из текста все слова, не связанные с датой и временем
        """
        self.nodes = [node for node in self.nodes if node.cat != 'junk']

    def reduce(self):
        """
        Объединяет несколько нод в одну по заданным правилам
        """
        for f, *template in templates:
            nodes_samples = list(self.get_nodes_by_template(*template))
            for nodes in nodes_samples:
                new_node = f(nodes, now=self.now)
                self.replace(nodes[0], nodes[-1], new_node)

    def to_dict(self):
        """
        Возвращает словарь "категория_ноды: значение_ноды"
        """
        if not self.nodes:
            self.make_nodes()
        return {node.cat: node.value for node in self.nodes}

    def parse(self):
        """
        Возвращает результат на основе обработанных нод
        """
        nodes = self.to_dict()

        # получаем значения нод, отвечающих за дату и время
        result_datetime = nodes.get('datetime')
        result_date = nodes.get('date')
        result_time = nodes.get('time')

        if result_datetime is None:
            if result_date is not None and result_time is not None:
                result_datetime = datetime.combine(result_date, result_time)

        # цепляем часовой пояс
        if result_datetime is not None:
            result_datetime = change_timezone(result_datetime, self.tz)
        if result_date is not None:
            result_date = change_timezone(result_date, self.tz)
        if result_time is not None:
            result_time = change_timezone(result_time, self.tz)

        # возвращаем ожидаемый результат, если такой есть
        if datetime in self.allowed_results and result_datetime is not None:
            return result_datetime
        if date in self.allowed_results and result_date is not None:
            return result_date
        if time in self.allowed_results and result_time is not None:
            return result_time

        # ищем адаптированный результат
        if datetime in self.allowed_results and result_time is not None:
            result = datetime.combine(self.now.date(), result_time)
            return change_timezone(result, self.tz)
        if datetime in self.allowed_results and result_date is not None:
            result = datetime.combine(result_date, self.default_time)
            return change_timezone(result, self.tz)

        # возвращаем результат по умолчанию
        if None not in self.allowed_results:
            if datetime in self.allowed_results:
                return self.now
            if date in self.allowed_results:
                return self.now.date()
            if time in self.allowed_results:
                return self.now.time()
            raise KeyError('Не найден результат, соответствующий значению allowed_results')

    def get_datetime(self):
        return self.parse()

    def get_clear_text(self):
        result = []
        for chain in self.get_junk_chains():
            for node in chain:
                result.append(node.word)
        return ' '.join(result)

    def get_last_clear_text(self):
        chains = list(self.get_junk_chains())
        if not chains:
            return ''
        chain = chains[-1]
        return ' '.join([node.word for node in chain])
