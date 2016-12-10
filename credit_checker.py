# http://stackoverflow.com/questions/7460938/how-to-run-python-script-in-webpage

# Does not take in FINE as a CSE

from credits import *


def get_terms(transcript):

	# Change seperator to 'startwith' rather hard code
	indices = find_indices(transcript, SEPERATOR)
	terms = []
	for index, element in enumerate(indices):
		if index < len(indices)-1:
			terms.append(transcript[indices[index]:indices[index+1]])

	return terms


def find_indices(lst, text):
	indices = [i for i, x in enumerate(lst) if text in x]
	return indices


# TODO
def get_passed_courses(courses):
	passed = []
	for course in courses:
		if is_passed(course):
			passed.append(course)
	return passed
	


def passed_course(course_line):
	if int(course_line[-3]) >= 1:
		return True
	else:
		import pdb
		pdb.set_trace()

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
	import pdb
	pdb.set_trace()
	EE_flag = is_ee(courses)
	PD = []
	ECE = []
	CSE = []
	NSE = []
	WKRPT = []
	TE = []
	for course in courses:
		if course.startswith('PD'):
			PD.append(course)

		elif course in manditory or (EE_flag and course in manditory_EE) or (not EE_flag and course in manditory_CE):
			ECE.append(course)

		elif course.startswith('WKRPT'):
			WKRPT.append(course)

		elif course in nse_courses_list_1 or course in nse_courses_list_2:
			NSE.append(course)

		elif check_if_cse(course):
			CSE.append(course)

		else:
			TE.append(course)
	return PD, ECE, CSE, NSE, TE, WKRPT


def check_if_cse(course):
	return check_if_list_c_cse(course) or check_if_list_a_cse(course) or check_if_list_d_cse(course)

def check_if_list_d_cse(course):
	return True if course in set(cse_courses_list_d) else False


def check_if_list_c_cse(course):
	is_cse = False

	if course in cse_courses_list_c:
		is_cse = True

	if course not in not_list_c and any([course.startswith(dprtmnt) for dprtmnt in dprtmns_list_c]):
		is_cse = True

	return is_cse


def check_if_list_a_cse(course):
	return True if course in set(cse_courses_list_a) else False
	

def check_requirements(courses, coop):
	PD, ECE, CSE, NSE, TE, WKRPT = group_courses(courses)

	check_non_course(PD, 5)
	check_non_course(WKRPT, 3)
	check_non_course(coop, 5)

	check_ece_courses(ECE)
	check_cse_courses(CSE)
	check_nse_courses(NSE)
	check_te_courses(TE)


def check_non_course(satisfied, requirement):
	name = satisfied[0].split()[0]

	if len(satisfied)<requirement:
		print("WARNING: You currently have {} {}, but require at least {}".format(len(satisfied), name, requirement))
	else:
		print("You've met requirements for {}".format(name))
		

def check_ece_courses(ece_courses):
	EE_flag = is_ee(ece_courses)

	if EE_flag:
		return set(ece_courses) == set(manditory + manditory_EE)
	return set(ece_courses) == set(manditory_EE + manditory_CE)


def check_nse_courses(nse_courses):
	list_1 = False
	list_2 = False
	for course in nse_courses:
		if course in nse_courses_list_1:
			list_1 = True
		if course in nse_courses_list_2:
			list_2 = True

		if list_2 and list_1:
			break

	return list_1 and list_2


def check_cse_courses(cse_courses):

	list_a_d = []
	list_c = []

	for course in cse_courses:
		if check_if_list_c_cse(course):
			list_c.append(course)
		elif check_if_list_a_cse(course) or check_if_list_d_cse(course):
			list_a_d.append(course)

	if (len(list_c) == 2 and len(list_a_d) == 2) or len(list_c) >= 4:
		print("You've completed your CSE requirements")

	else:
		print("WARNING: You have completed {} from list C and {} from list A/C/D while required is 2 from list C and 2 from any of A/C/D".format(len(list_c),len(list_a_d)))


def check_te_courses(te_courses):
	ece_count = 0
	for course in te_courses:
		if course.startswith('ECE'):
			ece_count += 1

	if ece_count >= 3 and len(te_courses) >= 5:
		print("You've satisfied all TE requirements")

	else:
		if ece_count < 3:
			print("You haven't satisfied the required 3 ECE TE's, and only recieved {}\n".format(ece_count))

		if len(te_courses) < 5:
			print("You have only completed {} out of the 5 required TE courses".format(len(te_courses)))
			print(' '.join(te_courses))



def is_passed(course):
	slash = '/'
	indices = find_indices(course, slash)
	for index in indices:
		units = course[index].split(slash)
		if float(units[1]) > 0:
			return True
		elif course[-2] == 'SUPP':
			if course[-1] == 'S':
				return True
	return False


if __name__ == "__main__":
	courses = [line.split() for line in open('transcript.txt') if '/' in line and "Course" not in line]
	coop = [line.rstrip() for line in open('transcript.txt') if "COOP" in line and "CR" in line]

	courses = get_passed_courses(courses)
	courses = [extract_course_name(course) for course in courses]
	check_requirements(courses, coop)
	

