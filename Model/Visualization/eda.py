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
		
		print("\nData Describe : \n",self.data.describe())
		
		print("\nData Information")
		self.data.info()
		
		# Data Shape
		print("\nData Shape (rows,columns) : ",self.data.shape)
		
		# Columns
		print("\nColumns : ",self.data.columns.values)
		
		# Column Dtypes
		print("\nD-types of object : \n",self.data.dtypes)
		
		# Checking Duplicates
		print("\nTotal Duplicated rows",self.data.duplicated().sum())
		
		# Checking Null
		print("\nTotal Null Values \n",self.data.isnull().sum())

		# row information target and feature
		for column in ['Education Level', 'Department', 'Quality_of_Work', 'Workload',
              'Code_Quality', 'Debugging_Skills', 'Time_Management', 'Learning_Growth','Performance']:
			self.get_unique(column)

	# count plot
	def count_plot(self,column):
		print("\nGenerating Count Plot for "+column +" column.......")
		mlt.figure(figsize=(6,4))
		sns.countplot(x=self.data[column])
		mlt.show()

	def get_unique(self,col_name):
		print("\nTotal unique values of "+col_name +" column : ",self.data[col_name].nunique())
		print("\nUnique values : ",self.data[col_name].unique())

	# co-relation matrix
	def correlation_matrix(self):
		print("\nGenerating Co-relation matrix......")
		co_relation = self.data.corr()
		print("Co-relation Matrix : ")
		print(co_relation)

		mlt.figure(figsize=(6,4))
		sns.heatmap(data=co_relation)
		mlt.show()

	def generate_box_plot(self,column1, column2):
		mlt.figure(figsize=(7,4))
		sns.set_style("whitegrid")
		sns.boxplot(x=column1, y=column2, data=self.data)
		mlt.show()

	# Box Plots
	def box_plots(self):
		print("Generating Box Plots......")

		# Box plot for data
		mlt.figure(figsize=(7,4))
		sns.set_style("whitegrid")
		sns.boxplot(data = self.data)
		mlt.show()

		# for columns
		self.generate_box_plot('Department','Project_Completion_Rate')
		self.generate_box_plot('Department','Job Tenure')
		self.generate_box_plot('Education Level','Project_Completion_Rate')
		self.generate_box_plot('Education Level','Job Tenure')

	# visualization calls
	def visualization(self):
		# co-relation matrix
		self.correlation_matrix()
		# count plot
		for column in ['Performance','Department','Education Level']:
			self.count_plot(column=column)
		# box plot
		self.box_plots()