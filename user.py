from credit_checker import *

class user:

	def __init__(self, courses):
		# completed courses
		self.PD_CC = get_completed_courses(crs, 'PD')
		self.WKRPT_cc = get_completed_courses(crs, 'WKRPT')
		self.COOP_cc = get_completed_courses(crs, 'COOP')
		self.ECE_cc = get_completed_courses(crs, 'ECE')
		self.CSE_cc = get_completed_courses(crs, 'CSE')
		self.NSE_cc = get_completed_courses(crs, 'NSE')
		self.TE_cc = get_completed_courses(crs, 'TE')

		# missing courses
		self.PD_m = get_missed_courses(crs, 'PD')
		self.WKRPT_m = get_missed_courses(crs, 'WKRPT')
		self.COOP_m = get_missed_courses(crs, 'COOP')
		self.ECE_m = get_missed_courses(crs, 'ECE')
		self.CSE_m = get_missed_courses(crs, 'CSE')
		self.NSE_m = get_missed_courses(crs, 'NSE')
		self.TE_m = get_missed_courses(crs, 'TE')

		# missing number
		self.PD_mn = get_missing_number(crs, 'PD')
		self.WKRPT_mn = get_missing_number(crs, 'WKRPT')
		self.COOP_mn = get_missing_number(crs, 'COOP')
		self.ECE_mn = get_missing_number(crs, 'ECE')
		self.CSE_mn = get_missing_number(crs, 'CSE')
		self.NSE_mn = get_missing_number(crs, 'NSE')
		self.TE_mn = get_missing_number(crs, 'TE')

	def get_