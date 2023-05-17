# EDA
# EMPLOYEE PERFORMANCE PREDICTION

# Importing Dependencies
import matplotlib.pyplot as mlt
import seaborn as sns

# Defining a class
class DataEDA:
	def __init__(self,data):
		self.data = data

	# printing the data
	def print_data(self):
		print("Data : \n",self.data.head())

	# data information
	def data_information(self):
		print("\nData Information")
		
		print("\nData Describe :")
		print(self.data.describe())
		
		print("\nData Information")
		self.data.info()
		
		# Data Shape
		print("\nData Shape : ")
		print(self.data.shape)
		
		# Columns
		print("\nColumns : ",self.data.columns.values)
		
		# Columns and Rows
		print("\nTotal Number of Columns : ",len(self.data.columns))
		print("\nTotal Number of Rows : ",self.data.shape[0])
		
		# Column Dtypes
		print("\nD-types of object : ")
		print(self.data.dtypes)
		
		# Checking Duplicates
		print("\nTotal Duplicated rows",self.data.duplicated().sum())
		
		# Checking Null
		print("\nTotal Null Values",self.data.isnull().sum())

		# row information
		self.data_row_info()
		
		# Checking values of Columns
		print("\nEducation Level : ")
		print("Unique Values of Education Level Column : ")
		print(self.data['Education Level'].unique())
		print("Total number of unique values are : ",self.data['Education Level'].nunique())


	# count plot
	def count_plot(self):
		print("\nGenerating Count Plot for target column.......")
		mlt.figure(figsize=(6,4))
		sns.countplot(x=self.data['Performance'])
		mlt.show()

		# count plot for database
		print("\nGenerating Count Plot for Department column.......")
		mlt.figure(figsize=(6,4))
		sns.countplot(x=self.data['Department'])
		mlt.show()

		# count plot for Education Level
		print("\nGenerating Count Plot for Department column.......")
		mlt.figure(figsize=(6,4))
		sns.countplot(x=self.data['Education Level'])
		mlt.show()

	def get_unique(self,col_name):
		# Working on a particular column
		print("\nUnique values of target column : ")
		print(self.data[col_name].nunique())
		print(self.data[col_name].unique())

	def data_row_info(self):
		# target
		self.get_unique('Performance')
		# feature
		self.get_unique('Education Level')
		self.get_unique('Department')
		self.get_unique('Quality_of_Work')
		self.get_unique('Workload')
		self.get_unique('Code_Quality')
		self.get_unique('Debugging_Skills')
		self.get_unique('Time_Management')
		self.get_unique('Learning_Growth')

	# co-relation matrix
	def correlation_matrix(self):
		print("\nGenerating Co-relation matrix......")
		co_relation = self.data.corr()
		print("Co-relation Matrix : ")
		print(co_relation)

		mlt.figure(figsize=(6,4))
		sns.heatmap(data=co_relation)
		mlt.show()

	# Box Plots
	def box_plots(self):
		print("Generating Box Plots......")

		# Box plot for data
		mlt.figure(figsize=(7,4))
		sns.set_style("whitegrid")
		sns.boxplot(data = self.data)
		mlt.show()

		# Project Completion Rate
		sns.set_style("whitegrid")
		sns.boxplot(x = 'Department', y = 'Project_Completion_Rate', data = self.data)
		mlt.show()

		# Job Tenure
		sns.set_style("whitegrid")
		sns.boxplot(x = 'Department', y = 'Job Tenure', data = self.data)
		mlt.show()

		# Education Level Completion Rate
		sns.set_style("whitegrid")
		sns.boxplot(x = 'Education Level', y = 'Project_Completion_Rate', data = self.data)
		mlt.show()

		# Education Level Job Tenure
		sns.set_style("whitegrid")
		sns.boxplot(x = 'Education Level', y = 'Job Tenure', data = self.data)
		mlt.show()

	# scatter plots
	def scatter_plots(self):
		# Scatter plot for education level and project completion rate
		mlt.figure(figsize=(7,4))
		mlt.scatter(x=self.data['Education Level'],y=self.data[
			'Project_Completion_Rate'])
		mlt.show()

		# Scatter plot for Department and project completion rate
		mlt.figure(figsize=(7,4))
		mlt.scatter(x=self.data['Department'],y=self.data[
			'Project_Completion_Rate'])
		mlt.show()

	# pie charts
	def pie_charts(self):

		# pie chart for unique department column
		mlt.figure(figsize=(6,4))
		print("\nValue Counts of each department : ")
		print(self.data['Department'].value_counts())
		mlt.pie(self.data['Department'].value_counts(),labels=self.data['Department'].unique())
		mlt.show()

		# pie chart for unique Education Level column
		mlt.figure(figsize=(6,4))
		print("\nValue Counts of each type of Education Level : ")
		print(self.data['Education Level'].value_counts())
		mlt.pie(self.data['Education Level'].value_counts(),labels=self.data['Education Level'].unique())
		mlt.show()

	# visualization calls
	def visualization(self):
		# pie chart
		self.pie_charts()
		# count plot
		self.count_plot()
		# co-relation matrix
		self.correlation_matrix()
		# box plot
		self.box_plots()
		# scatter plot
		self.scatter_plots()