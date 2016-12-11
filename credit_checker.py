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
	

def check_requirements(courses, COOP):
	PD, ECE, CSE, NSE, TE, WKRPT = group_courses(courses)
	requirement = ''
	requirement += check_non_course(PD, 5)
	requirement += check_non_course(WKRPT, 3)
	requirement += check_non_course(COOP, 5)

	requirement += check_ece_courses(ECE)
	requirement += check_cse_courses(CSE)
	requirement += check_nse_courses(NSE)
	requirement += check_te_courses(TE)
	return requirement, PD, WKRPT, COOP, ECE, CSE, NSE, TE


def check_non_course(satisfied, requirement):
	name = satisfied[0].split()[0]

	if len(satisfied)<requirement:
		return "WARNING: You currently have {} {}, but require at least {}\n".format(len(satisfied), name, requirement)
	else:
		return "You've met requirements for {}\n".format(name)
		

def check_ece_courses(ece_courses):
	EE_flag = is_ee(ece_courses)

	if set(ece_courses) == set(manditory + manditory_EE) or set(ece_courses) == set(manditory_EE + manditory_CE):
		rslt = "You've met all your "
		if EE_flag:
			rslt += "Electrical Engineering course requirements\n"
		else:
			rslt += "Computer Engineering course requirements\n"
	else:
		rslt = "You have not me your manditory core course requirements\n"

	return rslt


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

	rqrmnt = ""
	if list_1:
		rqrmnt += "You've met your NSE list 1 requirements\n"
	else:
		rqrmnt += "You haven't met your NSE list 1 requirements\n"
	if list_2:
		rqrmnt += "You've met your NSE list 2 requirements\n"
	else:
		rqrmnt += "You haven't met your NSE list 2 requirements\n"
	return rqrmnt


def check_cse_courses(cse_courses):

	list_a_d = []
	list_c = []

	for course in cse_courses:
		if check_if_list_c_cse(course):
			list_c.append(course)
		elif check_if_list_a_cse(course) or check_if_list_d_cse(course):
			list_a_d.append(course)

	if (len(list_c) == 2 and len(list_a_d) == 2) or len(list_c) >= 4:
		return "You've completed your CSE requirements\n"

	else:
		return "WARNING: You have completed {} from list C and {} from list A/C/D while required is 2 from list C and 2 from any of A/C/D\n".format(len(list_c),len(list_a_d))


def check_te_courses(te_courses):
	ece_count = 0
	for course in te_courses:
		if course.startswith('ECE'):
			ece_count += 1

	if ece_count >= 3 and len(te_courses) >= 5:
		return "You've satisfied all TE requirements"

	else:
		if ece_count < 3:
			return "You haven't satisfied the required 3 ECE TE's, and only recieved {}\n".format(ece_count)

		if len(te_courses) < 5:
			courses = (' '.join(te_courses))
			return "You have only completed {} ({}) out of the 5 required TE courses\n".format(len(te_courses), courses)



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