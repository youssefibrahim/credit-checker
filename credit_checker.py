# http://stackoverflow.com/questions/7460938/how-to-run-python-script-in-webpage

# Does not take in FINE as a CSE

from credits import *


def find_indices(lst, text):
	indices = [i for i, x in enumerate(lst) if text in x]
	return indices


def get_passed_courses(courses):
	passed = []
	for course in courses:
		if is_passed(course):
			passed.append(course)
	return passed


def extract_course_name(course):
	return ' '.join(course[:2])

def is_ee(dropdown_string):
	if dropdown_string == 'Electrical Engineering':
		return True
	print(dropdown_string)
	return False

def group_courses(courses, EE_flag):
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
	return True if course in set(cse_courses_list_d) or any([course.startswith(dprtmnt) for dprtmnt in dprtmns_list_d]) else False

def check_if_list_c_cse(course):
	is_cse = False

	if course in cse_courses_list_c:
		is_cse = True

	if course not in not_list_c and any([course.startswith(dprtmnt) for dprtmnt in dprtmns_list_c]):
		is_cse = True

	return is_cse


def check_if_list_a_cse(course):
	return True if course in set(cse_courses_list_a) else False
	

def check_requirements(unorganized_courses, COOP, dropdown_string):
	EE_flag = is_ee(dropdown_string)
	PD, ECE, CSE, NSE, TE, WKRPT = group_courses(unorganized_courses, EE_flag)

	courses = {}
	courses['PD'] = build_dict(PD,[],5)
	courses['WKRPT'] = build_dict(WKRPT,[],3)
	courses['COOP'] = build_dict(COOP,[],5)

	courses['ECE'] = check_ece_courses(ECE, EE_flag)
	courses['CSE'] = check_cse_courses(CSE)
	courses['NSE'] = check_nse_courses(NSE)
	courses['TE'] = check_te_courses(TE)

	return courses

def build_dict(courses=[], missing_courses=[], num_required=None):
	if not num_required:
		num_required = len(courses)

	if missing_courses and not num_required:
		return {'completed': courses, 'missing': missing_courses, 'num_missing': len(missing_courses)} 

	return {'completed': courses, 'missing': missing_courses, 'num_missing': num_required-len(courses)}




def check_ece_courses(ece_courses, EE_flag):
	dict = {}
	if EE_flag:
		return build_dict(ece_courses, list(set(manditory + manditory_EE) - set(ece_courses)), len(manditory) + len(manditory_EE))

	return build_dict(ece_courses, list(set(manditory + manditory_CE) - set(ece_courses)), len(manditory + manditory_CE))


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

	missing = []
	if list_1 and list_2:
		return build_dict(nse_courses)
	else:
		if not list_1:
			missing.append('List 1 NSE')
		if not list_2:
			missing.append('List 2 NSE')
	return build_dict(nse_courses, missing)


def check_cse_courses(cse_courses):

	list_a_d = []
	list_c = []

	for course in cse_courses:
		if check_if_list_c_cse(course):
			list_c.append(course)
		elif check_if_list_a_cse(course) or check_if_list_d_cse(course):
			list_a_d.append(course)

	if ((len(list_c) + len(list_a_d)) == 4):
		return build_dict(cse_courses)

	return build_dict(cse_courses,[] ,4-(len(list_c) + len(list_a_d)))


def check_te_courses(te_courses):
	ece_count = 0
	for course in te_courses:
		if course.startswith('ECE'):
			ece_count += 1		

	missing = []
	
	if ece_count < 	3:
		missing.append("ECE Courses: {}".format(3-ece_count))

	if len(te_courses) < 5:
		missing.append("Other TEs: {}".format(5-len(te_courses)-(3-ece_count)))
	
	return build_dict(te_courses,missing,5)


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