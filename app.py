# PROJECT
# EMPLOYEE PERFORMANCE PREDICTION

# Importing Dependencies
from flask import Flask,render_template,request,redirect
# importing method
from Model.ModelTraining.preprocessing import Preprocessing

# defining class
class WebApp:

	# class ctor
	def __init__(self):
		self.result = None
		self.prediction = None
		self.data = {'employee-id':0,'employee-first-name':'','employee-last-name':'',
					 'employee-job-tenure':0,'Education Level':'',
					 'Department':'','Technical Skills':'','employee-code-quality':'',
					 'employee-quality-of-work':'','employee-debugging-skills':'',
					 'employee-time-management':'','Workload':'',
					 'employee-peer-feedback':0,'employee-project-completion-rate':0,
					 'Learning_Growth':''}
		self.loading = True
		self.encoders = {}
		self.model = None
		self.preprocessing = Preprocessing()
		self.department_skills = {'Database': {'Data Modelling', 'PowerBI', 'Data Mining', 'SSRS', 'Oracle', 'MongoDB', 'MSSQL', 'Data Warehouse', 'MySQL'}, 'Frontend': {'CSS', 'Angular JS', 'Bootstrap', 'Node JS', 'Java Script', 'HTML'}, 'DevOps': {'Security', 'Cloud management', 'Automation', 'Jenkins', 'Ansible', 'Git'}, '.Net': {'C#', 'MVC', 'ASP.Net', 'LinQ', 'Visual Basic .Net', 'Entity Framework', 'ADO.Net', '.Net Core Framework'}, 'Mobile': {'iOS', 'Android', 'React Native', 'Flutter'}, 'Python & ML': {'Pytorch', 'TensorFlow', 'ML models', 'Django', 'Flask', 'DL models', 'Postgresql', 'MSSQL', 'Python'}}

	# home employee_info method
	def employee_info(self):
		if request.method == 'POST':
			self.data['employee-id'] = int(request.form.get('employee-id'))
			self.data['employee-first-name'] = request.form.get('employee-first-name')
			self.data['employee-last-name'] = request.form.get('employee-last-name')
			self.data['employee-job-tenure'] = int(request.form.get('employee-job-tenure'))
			self.data['Education Level'] = request.form.get('employee-education-level')
			self.data['Department'] = request.form.get('employee-department')
			return redirect('/skills')
		return render_template('page1.html',data=self.data, department_skills=self.department_skills)

	# home employee_skills method
	def employee_skills(self):
		if request.method == "POST":
			if request.form.get('action1') == 'VALUE1':
				return redirect('/')
			skills = request.form.getlist('Technical Skills')
			self.data['Technical Skills'] = ', '.join(skills)
			return redirect('/ratings')
		return render_template('page2.html',data=self.data, department_skills=self.department_skills)

	# home employee_ratings method
	def employee_ratings(self):
		if request.method == "POST":
			if request.form.get('action1') == 'VALUE1':
				return redirect('/skills')
			self.data['employee-code-quality'] = request.form.get('code-quality')
			self.data['employee-quality-of-work'] = request.form.get('quality-of-work')
			self.data['employee-debugging-skills'] = request.form.get('debugging-skills')
			self.data['employee-time-management'] = request.form.get('time-management')
			self.data['Workload'] = request.form.get('workload')

			return redirect('/project')
		return render_template('page3.html',data=self.data)

	# home employee_project method
	def employee_project(self):
		if request.method == "POST":
			if request.form.get('action1') == 'VALUE1':
				return redirect('/ratings')
			self.data['employee-peer-feedback']=int(request.form.get('peer-feedback'))
			self.data['employee-project-completion-rate']=int(request.form.get(
				'project-completion-rate'))*10
			self.data['Learning_Growth'] = request.form.get('learning-growth')

			cleaned_data = self.preprocessing.input_data_cleaning(dict(self.data),
																  filepath="./Model/Pickle/cleaning.pkl")

			self.result = self.preprocessing.new_prediction(cleaned_data,
															filepath="./Model/Pickle/model.pkl")[0]
			if self.result == 0:
				self.prediction = "Exceeds Expectations"
			elif self.result == 1:
				self.prediction = "Meets Expectations"
			else:
				self.prediction = "Needs Improvement"

			self.loading = False

			return redirect('/performance')
		return render_template('page4.html',data=self.data)

	# performance method
	def employee_performance(self):
		return render_template('performance.html',data=self.data,loading=self.loading,
							   result=self.result,prediction=self.prediction)

# main start
if __name__ == "__main__":
	# app object
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

print("GRACY PATEL")
# End of File
