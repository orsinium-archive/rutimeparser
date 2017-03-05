
dates = (
	'%Y-%m-%d',
	'%d.%m.%Y',
	'%m/%d/%Y',
	)
times = (
	'%H:%M',
	)

delta_sizes = (
	('years',   ('год', 'года', 'лет')),
	('months',  ('месяц', 'месяца', 'месяцев')),
	('days',    ('день', 'дня', 'дней')),
	('hours',   ('час', 'часа', 'часов')),
	('minutes', ('минуту', 'минуты', 'минут')),
	('seconds', ('секунду', 'секунды', 'секунд')),
	('weeks',   ('неделю', 'недели', 'недель', 'неделе')),
	)

from_now = {
	'позавчера': -2,
	'вчера': -1,
	'сегодня': 0,
	'завтра': 1,
	'послезавтра': 2,
	}

times_of_day = {
	'утром': 9, 
	'днем': 15, 
	'вечером': 21,
	'ночью': 3,
	}


months = (
	('января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря'),
	('январе', 'феврале', 'марте', 'апреле', 'мае', 'июне', 'июле', 'августе', 'сентябре', 'октябре', 'ноябре', 'декабре'),
	('январь', 'февраль', 'март', 'апрель', 'май', 'июнь', 'июль', 'август', 'сентябрь', 'октябрь', 'ноябрь', 'декабрь'),
	)

weekdays = (
	('понедельник', 'вторник', 'среду', 'четверг', 'пятницу', 'субботу', 'воскресенье'),
	('понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье'),
	('пн', 'вт', 'ср', 'чт', 'пт', 'сб', 'вс'),
	)
