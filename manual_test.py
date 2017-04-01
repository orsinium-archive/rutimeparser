from timeparser import parse_time, get_clear_text, get_last_clear_text

if __name__ == '__main__':
	for test in open('test_strings', 'r'):
		print(test.strip(), '\x1B[31m', parse_time(test), '\x1B[0m')
	
	while 1:
		text = input('> ')
		print('\x1B[32m ', get_clear_text(text), '\x1B[0m')
		print('\x1B[33m ', get_last_clear_text(text), '\x1B[0m')
