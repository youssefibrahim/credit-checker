from flask import Flask, render_template, redirect, request, send_file
from credit_checker import *

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/result", methods=['POST'])
def my_form_post():
	text = request.form['transcript']
	lines = text.split('\n')
	courses = [line.split() for line in lines if '/' in line and "Course" not in line]
	coop = [line.rstrip() for line in lines if "COOP" in line and "CR" in line]
	courses = get_passed_courses(courses)
	courses = [extract_course_name(course) for course in courses]
	coop = [extract_course_name(work.split()) for work in coop]

	rqrmnt, PD, WKRPT, COOP, ECE, CSE, NSE, TE = check_requirements(courses, coop)
	
	PD = convert_to_string(sorted(PD))
	WKRPT = convert_to_string(sorted(WKRPT))
	COOP = convert_to_string(sorted(COOP))
	ECE = convert_to_string(sorted(ECE))
	CSE = convert_to_string(sorted(CSE))
	NSE = convert_to_string(sorted(NSE))
	TE = convert_to_string(sorted(TE))

	return render_template('result.html', rqrmnt=rqrmnt, PD=PD, WKRPT=WKRPT, COOP=COOP, ECE=ECE, CSE=CSE, NSE=NSE, TE=TE)
    
@app.route("/disclaimer")
def present_disclaimer():
	return send_file('static/disclaimer.pdf')

def convert_to_string(courses):
	return ', '.join(courses)



if __name__ == "__main__":
    app.run()