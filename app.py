# PROJECT
# EMPLOYEE PERFORMANCE PREDICTION

# Importing Dependencies
import json
import pickle
import random
from flask import Flask,render_template,request,redirect
# importing method
from Model.ModelTraining.preprocessing import Preprocessing

# defining class
class WebApp:

	# class ctor
	def __init__(self):
		self.prediction = None
		self.quote, self.author = None, None
		self.quoteDict = None
		self.data = {'employee-id':0,'employee-first-name':'','employee-last-name':'',
					 'employee-job-tenure':0,'Education Level':'',
					 'Department':'','Technical Skills':[],'employee-code-quality':'',
					 'employee-quality-of-work':'','employee-debugging-skills':'',
					 'employee-time-management':'','Workload':'',
					 'employee-peer-feedback':0,'employee-project-completion-rate':0,
					 'Learning_Growth':''}
		self.preprocessing = Preprocessing()
		self.department_skills = self.preprocessing.get_department_skills(filepath="./Model/Pickle/cleaning.pkl")

	# predict method
	def predict_result(self):
		# pre-processing user input values
		cleaned_data = self.preprocessing.input_data_cleaning(dict(self.data))
		# making prediction
		result = self.preprocessing.new_prediction(cleaned_data,filepath="./Model/Pickle/model.pkl")[0]
		self.prediction = "Exceeds Expectations" if result == 0 else "Meets Expectations" if result == 1 else "Needs Improvement"

		# loading quotes json  file
		with open("Model/Data/quote.json") as quotes:
			self.quoteDict = json.load(quotes)
		random_No = random.randint(0,9)
		self.quote = self.quoteDict[self.prediction][random_No]['quote']
		self.author = self.quoteDict[self.prediction][random_No]['author']

	# employee_info method
	def employee_info(self):
		if request.method == 'POST':
			self.data['employee-id'] = int(request.form.get('employee-id'))
			self.data['employee-first-name'] = request.form.get('employee-first-name')
			self.data['employee-last-name'] = request.form.get('employee-last-name')
			self.data['employee-job-tenure'] = int(request.form.get('employee-job-tenure'))
			self.data['Education Level'] = request.form.get('employee-education-level')
			self.data['Department'] = request.form.get('employee-department')
			return redirect('/skills')
		return render_template('employee_information.html',data=self.data, department_skills=self.department_skills)

	# employee_skills method
	def employee_skills(self):
		if self.data['Department'] == "Python":
			self.data['Department'] = "Python & ML"
		if request.method == "POST":
			if request.form.get('action1') == 'previous':
				return redirect('/')
			self.data['Technical Skills'] = request.form.getlist('Technical Skills')
			return redirect('/ratings')
		return render_template('employee_skills.html',data=self.data, department_skills=self.department_skills)

	# employee_ratings method
	def employee_ratings(self):
		if request.method == "POST":
			if request.form.get('action1') == 'previous':
				return redirect('/skills')
			self.data['employee-code-quality'] = request.form.get('code-quality')
			self.data['employee-quality-of-work'] = request.form.get('quality-of-work')
			self.data['employee-debugging-skills'] = request.form.get('debugging-skills')
			self.data['employee-time-management'] = request.form.get('time-management')
			self.data['Workload'] = request.form.get('workload')

			return redirect('/project')
		return render_template('employee_ratings.html',data=self.data)

	# employee_project method
	def employee_project(self):
		if request.method == "POST":
			if request.form.get('action1') == 'previous':
				return redirect('/ratings')
			self.data['employee-peer-feedback']=int(request.form.get('peer-feedback'))
			self.data['employee-project-completion-rate']=int(request.form.get(
				'project-completion-rate'))*10
			self.data['Learning_Growth'] = request.form.get('learning-growth')
			self.predict_result()

			return redirect('/performance')
		return render_template('employee_project.html',data=self.data)

	# performance method
	def employee_performance(self):
		return render_template('performance.html',data=self.data,prediction=self.prediction,
							   quote=self.quote, author = self.author)
# main start
if __name__ == "__main__":
	# class object
	webapp = WebApp()

	# app object
	app = Flask(__name__)

	# creating routes
	app.add_url_rule('/',view_func=webapp.employee_info,methods=['GET','POST'])
	app.add_url_rule('/skills',view_func=webapp.employee_skills,methods=['GET','POST'])
	app.add_url_rule('/ratings',view_func=webapp.employee_ratings,methods=['GET','POST'])
	app.add_url_rule('/project',view_func=webapp.employee_project,methods=['GET','POST'])
	app.add_url_rule('/performance',view_func=webapp.employee_performance,methods=['GET'])

	# app run port = 8000
	app.run(port=8000,debug=True)