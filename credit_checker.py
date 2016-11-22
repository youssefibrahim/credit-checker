# http://stackoverflow.com/questions/7460938/how-to-run-python-script-in-webpage

ECE_1A = [100, 105, 140, 150]

COURSES_1A = ['CHE 102', 'MATH 117']

ECE_1B = ['ECE 100', 'ECE 103', 'ECE 106', 'ECE 124', 'ECE 155']

lines = [line.rstrip('\n') for line in open('transcript.txt')]
lines = filter(None, lines)
# print lines
SEPERATOR = '__________________________________________________________________________________________'
COURSES_START = 'Course      Description                Attempt/Earn  Grade  Credit InGPA  Desig   DesGrd  '

def get_terms(transcript):
	indices = find_indices(transcript, SEPERATOR)
	terms = []
	for index, element in enumerate(indices):
		if index < len(indices)-1:
			terms.append(transcript[indices[index]:indices[index+1]])

	return terms


def find_indices(lst, text):
	indices = [i for i, x in enumerate(lst) if x == text]
	return indices


def get_courses_per_term(term):
	start_index = term.index(COURSES_START)
	courses = []
	for line in term[start_index+1:]:
		course = line.split()
		courses.append(course)
	return courses



terms = get_terms(lines)
courses = []
for term in terms:
	courses.extend(get_courses_per_term(term))
courses = filter(None, courses)
import pdb
pdb.set_trace()