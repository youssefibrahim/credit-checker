from flask import Flask, render_template, redirect, request, send_file
from credit_checker import *

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/result", methods=['POST'])
def my_form_post():
	text = request.form['transcript']
	eng = request.form['dropdown']
	lines = text.split('\n')
	courses = [line.split() for line in lines if '/' in line and "Course" not in line]
	coop = [line.rstrip() for line in lines if "COOP" in line and "CR" in line]
	courses = get_passed_courses(courses)
	courses = [extract_course_name(course) for course in courses]
	coop = [extract_course_name(work.split()) for work in coop]

	crs = check_requirements(courses, coop, eng)
	
	PD_cc = convert_to_string(get_completed_courses(crs, 'PD'))
	WKRPT_cc = convert_to_string(get_completed_courses(crs, 'WKRPT'))
	COOP_cc = convert_to_string(get_completed_courses(crs, 'COOP'))
	ECE_cc = convert_to_string(get_completed_courses(crs, 'ECE'))
	CSE_cc = convert_to_string(get_completed_courses(crs, 'CSE'))
	NSE_cc = convert_to_string(get_completed_courses(crs, 'NSE'))
	TE_cc = convert_to_string(get_completed_courses(crs, 'TE'))

	PD_m = convert_to_string(get_missed_courses(crs, 'PD'))
	WKRPT_m = convert_to_string(get_missed_courses(crs, 'WKRPT'))
	COOP_m = convert_to_string(get_missed_courses(crs, 'COOP'))
	ECE_m = convert_to_string(get_missed_courses(crs, 'ECE'))
	CSE_m = convert_to_string(get_missed_courses(crs, 'CSE'))
	NSE_m = convert_to_string(get_missed_courses(crs, 'NSE'))
	TE_m = convert_to_string(get_missed_courses(crs, 'TE'))

	PD_mn = get_missing_number(crs, 'PD')
	WKRPT_mn = get_missing_number(crs, 'WKRPT')
	COOP_mn = get_missing_number(crs, 'COOP')
	ECE_mn = get_missing_number(crs, 'ECE')
	CSE_mn = get_missing_number(crs, 'CSE')
	NSE_mn = get_missing_number(crs, 'NSE')
	TE_mn = get_missing_number(crs, 'TE')

	return render_template('result.html', PD=PD_cc, WKRPT=WKRPT_cc, COOP=COOP_cc, ECE=ECE_cc, CSE=CSE_cc, NSE=NSE_cc, TE=TE_cc, PD_mn=PD_mn, WKRPT_mn=WKRPT_mn, COOP_mn=COOP_mn, ECE_mn=ECE_mn, CSE_mn=CSE_mn, NSE_mn=NSE_mn, TE_mn=TE_mn, PD_m=PD_m, WKRPT_m=WKRPT_m, COOP_m=COOP_m, ECE_m=ECE_m, CSE_m=CSE_m, NSE_m=NSE_m, TE_m=TE_m)

  
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