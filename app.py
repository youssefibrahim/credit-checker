from flask import Flask, render_template, redirect, request
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
	
	PD = reformat(sorted(PD))
	WKRPT = reformat(sorted(WKRPT))
	COOP = reformat(sorted(COOP))
	ECE = reformat(sorted(ECE))
	CSE = reformat(sorted(CSE))
	NSE = reformat(sorted(NSE))
	TE = reformat(sorted(TE))

	return render_template('result.html', rqrmnt=rqrmnt, PD=PD, WKRPT=WKRPT, COOP=COOP, ECE=ECE, CSE=CSE, NSE=NSE, TE=TE)
    
def reformat(courses):
	return ', '.join(courses)



if __name__ == "__main__":
    app.run()