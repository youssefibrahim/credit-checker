ECE_1A = [100, 105, 140, 150]

COURSES_1A = ['CHE 102', 'MATH 117']

ECE_1B = ['ECE 100', 'ECE 103', 'ECE 106', 'ECE 124', 'ECE 155']

lines = [line.rstrip('\n') for line in open('transcript.txt')]
lines = filter(None, lines)
print lines


def get_classes_from_transcript(user_input):
	return 0
