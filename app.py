from flask import Flask, render_template, redirect, request, send_file
from credit_checker import *
from user import *
from credits import *
import os

TOTAL_TERMS = 8
TOTAL_COURSE_COUNT = len(manditory) + len(manditory_EE)
SEASONS = ['Winter', 'Spring', 'Fall']

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/result", methods=['POST'])
def my_form_post():
	text = request.form['transcript']
	eng = request.form['dropdown']
	lines = text.split('\n')

	# terms found on transcript
	terms = set([line.split()[2] for line in lines if any(x in line for x in SEASONS)])
	
	# find all courses taken
	# '/' used to identify if course was completed i.e. Credits - 0.5/0.5
	courses = [line.split() for line in lines if '/' in line and "Course" not in line]

	# find all coops
	coop = [line.rstrip() for line in lines if "COOP" in line and "CR" in line]
	courses = get_passed_courses(courses)
	courses = [extract_course_name(course) for course in courses]
	coop = [extract_course_name(work.split()) for work in coop]

	# build dictionary based off users transcript
	crs = check_requirements(courses, coop, eng)
	
	user = student(crs)

	# completed courses
	PD_cc = user.PD
	WKRPT_cc = user.WKRPT
	COOP_cc = user.COOP
	ECE_cc = user.ECE
	CSE_cc = user.CSE
	NSE_cc = user.NSE
	TE_cc = user.TE

	# missing courses
	PD_m = convert_to_string(get_missed_courses(crs, 'PD'))
	WKRPT_m = convert_to_string(get_missed_courses(crs, 'WKRPT'))
	COOP_m = convert_to_string(get_missed_courses(crs, 'COOP'))
	ECE_m = convert_to_string(get_missed_courses(crs, 'ECE'))
	CSE_m = convert_to_string(get_missed_courses(crs, 'CSE'))
	NSE_m = convert_to_string(get_missed_courses(crs, 'NSE'))
	TE_m = convert_to_string(get_missed_courses(crs, 'TE'))

	# missing number
	PD_mn = get_missing_number(crs, 'PD')
	WKRPT_mn = get_missing_number(crs, 'WKRPT')
	COOP_mn = get_missing_number(crs, 'COOP')
	ECE_mn = get_missing_number(crs, 'ECE')
	CSE_mn = get_missing_number(crs, 'CSE')
	NSE_mn = get_missing_number(crs, 'NSE')
	TE_mn = get_missing_number(crs, 'TE')

	completion_percent = int(((TOTAL_COURSE_COUNT - ECE_mn)/float(TOTAL_COURSE_COUNT))*100)

	if completion_percent == 100:
		return redirect("https://youtu.be/SC4xMk98Pdc?t=35s")

	#return render_template('result.html', cp=completion_percent, PD=PD_cc, WKRPT=WKRPT_cc, COOP=COOP_cc, ECE=ECE_cc, CSE=CSE_cc, NSE=NSE_cc, TE=TE_cc, PD_mn=PD_mn, WKRPT_mn=WKRPT_mn, COOP_mn=COOP_mn, ECE_mn=ECE_mn, CSE_mn=CSE_mn, NSE_mn=NSE_mn, TE_mn=TE_mn, PD_m=PD_m, WKRPT_m=WKRPT_m, COOP_m=COOP_m, ECE_m=ECE_m, CSE_m=CSE_m, NSE_m=NSE_m, TE_m=TE_m)
	return render_template('result.html', cp=completion_percent, PD=PD_cc, WKRPT=WKRPT_cc, COOP=COOP_cc, ECE=ECE_cc, CSE=CSE_cc, NSE=NSE_cc, TE=TE_cc)

# @app.route("/download")
# def get_user_data():

  
@app.route("/disclaimer")
def present_disclaimer():
	return send_file('static/disclaimer.pdf')

def convert_to_string(courses):
	return ', '.join(courses)

def get_completed_courses(courses, key):
	return courses[key]['completed']

def get_missed_courses(courses, key):
	return courses[key]['missing']

def get_missing_number(courses, key):
	return courses[key]['num_missing']

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)