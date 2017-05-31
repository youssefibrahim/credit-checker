from flask import Flask, render_template, redirect, request, send_file
from credit_checker import *
from user import *
from credits import *
import os

TOTAL_TERMS = 8
TOTAL_ECE_COUNT = len(manditory) + len(manditory_EE)
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

	# build dictionary based off users transcript and initialize student object	
	user = student(check_requirements(courses, coop, eng))

	# courses
	PD = user.PD
	WKRPT = user.WKRPT
	COOP = user.COOP
	ECE = user.ECE
	CSE = user.CSE
	NSE = user.NSE
	TE = user.TE
	
	completion_percent = int(((TOTAL_ECE_COUNT - ECE['num_missing'])/float(TOTAL_ECE_COUNT))*100)
	print CSE
	print PD
	print WKRPT
	print COOP
	
	if completion_percent == 100:
		return redirect("https://youtu.be/SC4xMk98Pdc?t=35s")

	return render_template('result.html', sort=sorted, convert=convert_to_string, cp=completion_percent, PD=PD, WKRPT=WKRPT, COOP=COOP, ECE=ECE, CSE=CSE, NSE=NSE, TE=TE)

  
@app.route("/disclaimer")
def present_disclaimer():
	return send_file('static/disclaimer.pdf')

def convert_to_string(courses):
	return ', '.join(courses)

if __name__ == "__main__":
    # port = int(os.environ.get('PORT', 8000))
    # app.run(host='0.0.0.0', port=port)
    app.run()