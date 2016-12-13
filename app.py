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
	import pdb
	pdb.set_trace()
	PD = crs['PD']
	WKRPT = crs['WKRPT']
	COOP = crs['COOP']
	ECE = crs['ECE']
	CSE = crs['CSE']
	NSE = crs['NSE']
	TE = crs['TE']

	return render_template('result.html', PD=PD[0], WKRPT=WKRPT[0], COOP=COOP[0], ECE=ECE[0], CSE=CSE[0], NSE=NSE[0], TE=TE[0])

  
@app.route("/disclaimer")
def present_disclaimer():
	return send_file('static/disclaimer.pdf')

def convert_to_string(courses):
	return ', '.join(courses)

if __name__ == "__main__":
    app.run()