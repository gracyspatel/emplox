# PROJECT
# EMPLOYEE PERFORMANCE PREDICTION

# Importing Dependencies

# importing files
from Visualization.eda import DataEDA
from ModelTraining.preprocessing import Preprocessing
from ModelTraining.model import ModelTraining

class Main:
    def __init__(self):
        self.preprocessObj = Preprocessing()
        self.data = self.preprocessObj.read_data()
        self.edaObj = DataEDA(self.data)
        self.modelTrainingObj = None
        self.encoders = {}

    def test_new_data(self):
        # Entering input values
        education_level = input("Enter Education Level (Masters,Bachelors, PhD) : ")
        department = input("Enter Department (Python & ML, Database) : ")
        job_tenure = int(input("Enter your Job Tenure : "))
        skills = input("Enter Comma separated list of skills MySQL,HTML,CSS,SSRS,MSSQL,Oracle,CSS,Python: ")
        quality_of_work = input("Enter Quality of work GOOD EXCELLENT POOR : ")
        workload = input("Enter workload high low medium : ")
        peer_feedback = int(input("Enter peer feedback from the range of 1 to 10 : "))
        code_quality = input("Enter code quality Excellent, Good, poor : ")
        project_completion_rate = int(input("Enter Project Completion Rate in percentage : "))
        debugging_skills = input("Enter Debugging skills Excellent, Good, poor :")
        time_management = input("Enter Time management skills Excellent, Good: ")
        learning_rate = input("Enter learning Rate (yes/no) : ")

        random_data = {'employee-id': '1', 'employee-first-name': 'Gracy', 'employee-last-name':
            'Patel', 'employee-job-tenure': job_tenure, 'Education Level': education_level,
                       'Department': department, 'employee-skills': skills,
                       'employee-code-quality': code_quality, 'employee-quality-of-work':
                           quality_of_work, 'employee-debugging-skills': debugging_skills,
                       'employee-time-management': time_management, 'Workload': workload,
                       'employee-peer-feedback': peer_feedback, 'employee-project-completion-rate': project_completion_rate,
                       'Learning_Growth': learning_rate}

        random_data = self.preprocessObj.input_data_cleaning(random_data,
                                                             filepath="Pickle/cleaning.pkl")

        print("\nRESULT : ")
        result = self.preprocessObj.new_prediction(random_data,filepath="Pickle/cleaning.pkl")[0]
        if result == 0:
            print("Exceeds Expectations")
        elif result == 1:
            print("Meets Expectations")
        else:
            print("Needs Improvement")

    def main(self):

        # data information
        # self.edaObj.data_information()

        # visualizations
        # self.edaObj.visualization()

        # data cleaning
        self.data = self.preprocessObj.data_cleaning(data = self.data)

        # model training object
        self.modelTrainingObj = ModelTraining(data = self.data)
        self.modelTrainingObj.model_training()
        # self.test_new_data()

# main
if __name__ == "__main__":

    # main class object
    mainObj = Main()

    # main function calling
    mainObj.main()