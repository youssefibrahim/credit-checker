from credits import *

# Multi-purpose method for finding all indices for a given 
# element within a list
def find_indices(lst, text):
	indices = [i for i, x in enumerate(lst) if text in x]
	return indices

# Given a list of courses, returns only passed courses
def get_passed_courses(courses):
	passed = []
	for course in courses:
		if is_passed(course):
			passed.append(course)
	return passed

# This method is used to trip down the fat
# from a string, specifically given a string 
# that contains Course name, credit value, etc.
# Returns just course code (i.e. 'ECE 124')
def extract_course_name(course):
	return ' '.join(course[:2])

# Method to check what type of ECE student
# based off the dropdown input from the main app.py
def is_ee(dropdown_string):
	if dropdown_string == 'Electrical Engineering':
		return True
	print(dropdown_string)
	return False

# This method, given a course, checks if the student has
# earned the course credit, if not, will proceed to check
# if they have passed a supplementary
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

# Given courses, and type of student
# this method attempts to group courses accordingly
# to their correct requirement grouping
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

		# Checks manditory courses for EE and CE seperately
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

# With 3 possible lists for a CSE, this method checks 
# each list seperately and returns if the course is found
# to be within them
def check_if_cse(course):
	return check_if_list_c_cse(course) or check_if_list_a_cse(course) or check_if_list_d_cse(course)

# Method checks if is in allowed CSE list D or if from a department fitting of CSE list D
def check_if_list_d_cse(course):
	return True if course in set(cse_courses_list_d) or any([course.startswith(dprtmnt) for dprtmnt in dprtmns_list_d]) else False

# Method returns boolean, given a course to check if in List C CSE
def check_if_list_c_cse(course):
	is_cse = False

	if course in cse_courses_list_c:
		is_cse = True

	if course not in not_list_c and any([course.startswith(dprtmnt) for dprtmnt in dprtmns_list_c]):
		is_cse = True

	return is_cse

# Method returns boolean, given a course to check if in List A CSE
def check_if_list_a_cse(course):
	return True if course in set(cse_courses_list_a) else False
	
# This is the main method of this file, given a group of passed courses
# this method checks missing courses, and creates a dictionary, with keys 
# as program requirements, returning a dictionary of all the requirements with
# completed courses, missing courses, number of missing courses as values 
# for each key
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

# A method used to allow the re-usability of building a dictionary
# with required keys/values
def build_dict(courses=[], missing_courses=[], num_required=None):
	if not num_required:
		num_required = len(courses)

	if missing_courses and not num_required:
		return {'completed': courses, 'missing': missing_courses, 'num_missing': len(missing_courses)} 

	return {'completed': courses, 'missing': missing_courses, 'num_missing': num_required-len(courses)}


# Given ECE courses and students program, this method checks to see
# if the student has met the required core courses, returning a 
# built dictionary
def check_ece_courses(ece_courses, EE_flag):
	dict = {}
	if EE_flag:
		return build_dict(ece_courses, list(set(manditory + manditory_EE) - set(ece_courses)), len(manditory) + len(manditory_EE))

	return build_dict(ece_courses, list(set(manditory + manditory_CE) - set(ece_courses)), len(manditory + manditory_CE))

# Given all NSE courses completed by student, this method
# checks if courses are found in both list 1 and list 2 of NSE
# requirements, then returns the required dictionary
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

# Given all CSE courses completed by student, this method
# checks if the requirements have been met. The requirement is 
# to have at least 2 courses from list C, and any other 2 from 
# lists A/C/D. Returns required dictionary 
def check_cse_courses(cse_courses):

	list_a_d = []
	list_c = []

	for course in cse_courses:
		if check_if_list_c_cse(course):
			list_c.append(course)
		elif check_if_list_a_cse(course) or check_if_list_d_cse(course):
			list_a_d.append(course)

	if ((len(list_c) + len(list_a_d)) == 4) and len(list_c) >= 2:
		return build_dict(cse_courses)

	return build_dict(cse_courses,[] ,4)

# This method checks all TE course count
# as the requirement is 3 ECE courses and any other
# 2 technical electives from any department
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
