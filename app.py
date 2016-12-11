from flask import Flask, render_template, redirect, request
import credit_checker

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/", methods=['POST'])
def my_form_post():
	text = request.form['transcript']
	lines = text.split('\n')
	courses = [line.split() for line in lines if '/' in line and "Course" not in line]
	coop = [line.rstrip() for line in lines if "COOP" in line and "CR" in line]
	courses = get_passed_courses(courses)
	courses = [extract_course_name(course) for course in courses]

	return redirect('result.html', output=check_requirements(courses, coop))
    
if __name__ == "__main__":
    app.run()