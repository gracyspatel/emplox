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

    def main(self):

        # data information
        self.edaObj.data_information()

        # visualizations
        self.edaObj.visualization()

        # data cleaning
        self.data = self.preprocessObj.data_cleaning(data = self.data)

        # model training object
        training = ModelTraining(data = self.data)
        training.model_training()

# main
if __name__ == "__main__":
    # main class object
    mainObj = Main()
    mainObj.main()