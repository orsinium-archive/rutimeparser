from .numbers import numbers, replaces

import re
rex = re.compile(r'[^\w\.\-\:\/]+')


def normalize_text(text):
	'Нормализует текст'
	text = text.lower().replace('ё', 'е')
	for replace_from, replace_to in replaces:
		text = text.replace(replace_from, replace_to)
	return text

def normalize_word(word):
	'Нормализует отдельное слово'
	word = word.strip()
	word = word.strip('.-:/')
	if word in numbers:
		return numbers[word]
	return word

def get_words(text):
	'Возвращает список нормализованных слов'
	text = normalize_text(text)
	ns = []
	for word in rex.split(text):
		word = normalize_word(word)
		if type(word) is int:
			ns.append(word)
			continue
		if not word:
			continue
		if ns:
			yield str(sum(ns))
			ns = []
		yield word
	if ns:
		yield str(sum(ns))
