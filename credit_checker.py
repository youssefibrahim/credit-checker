# http://stackoverflow.com/questions/7460938/how-to-run-python-script-in-webpage

# Does not take in FINE as a CSE

from credits import *


lines = [line.rstrip() for line in open('transcript.txt')]
lines = filter(None, lines)


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

def get_courses(terms):
	courses = []
	for term in terms:
		courses.extend(get_courses_per_term(term))
	return courses

def extract_course_name(course):
	return ' '.join(course[:2])

def is_ee(courses):
	EE_flag = False

	if set(manditory_EE).issubset(set(courses)):
		EE_flag = True

	return EE_flag

def group_courses(courses):
	EE_flag = is_ee(courses)
	PD = []
	ECE = []
	CSE = []
	NSE = []
	WKRPT = []
	COOP = []
	TE = []
	import pdb
	pdb.set_trace()
	for course in courses:
		if course.startswith('PD'):
			PD.append(course)

		elif course in manditory or (EE_flag and course in manditory_EE) or (not EE_flag and course in manditory_CE):
			ECE.append(course)

		elif course.startswith('WKRPT'):
			WKRPT.append(course)

		elif course.startswith('COOP'):
			COOP.append(course)

		elif course in nse_courses_list_1 or course in nse_courses_list_2:
			NSE.append(course)

		elif check_if_cse(course):
			CSE.append(course)

		else:
			TE.append(course)
	return PD, ECE, CSE, NSE, TE, WKRPT, COOP


def check_if_cse(course):
	return check_if_list_c_cse(course) or check_if_list_a_cse(course)


def check_if_list_c_cse(course):
	is_cse = False

	if course in cse_courses_list_c:
		is_cse = True

	if course not in not_list_c and any([course.startswith(dprtmnt) for dprtmnt in dprtmns_list_c]):
		is_cse = True

	return is_cse

def check_if_list_a_cse(course):
	return True if course in set(cse_courses_list_a) else False
	

def check_requirements(courses):
	PD, ECE, CSE, NSE, TE, WKRPT, COOP = group_courses(courses)
	import pdb
	pdb.set_trace()
	check_non_course(PD, 5)
	check_non_course(WKRPT, 3)
	check_non_course(COOP, 5)

	check_ece_courses(ECE)
	# check_courses(CSE)
	# check_courses(NSE)


def check_non_course(satisfied, requirement):
	name = satisfied[0].split()[0]

	if len(satisfied)<requirement:
		print("WARNING: You currently have {} {}, but require at least {}".format(len(satisfied), name, requirement))
	else:
		print("You've met requirements for {}".format(name))
		

def check_ece_courses(ece_courses, te_courses):
	return


if __name__ == "__main__":
	terms = get_terms(lines)
	courses = get_courses(terms)
	courses = [course for course in courses if len(course) >= 5]
	courses = [extract_course_name(course) for course in courses]
 	for item in remove:
		courses = filter(lambda course: not course.startswith(item[0]), courses)
	
	check_requirements(courses)
	

