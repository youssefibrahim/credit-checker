from credit_checker import *
MISSING, COMPLETED, MISSING_NUM = 'missing', 'completed', 'num_missing'
class student:

	def __init__(self, courses):
		self.PD = courses['PD']
		self.WKRPT = courses['WKRPT']
		self.COOP = courses['COOP']
		self.ECE = courses['ECE']
		self.CSE = courses['CSE']
		self.NSE = courses['NSE']
		self.TE = courses['TE']


	def get_PD(self):
		return convert_to_string(self.PD_CC)


def convert_to_string(courses):
	return ', '.join(courses)