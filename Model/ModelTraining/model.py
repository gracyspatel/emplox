# model
# EMPLOYEE PERFORMANCE PREDICTION

# Importing Dependencies
import pickle
import pandas as pd
import numpy as np
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split,GridSearchCV
from sklearn.metrics import classification_report,confusion_matrix,accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB, MultinomialNB

# model training class
class ModelTraining:
    def __init__(self,data):
        self.data = data
        self.features,self.target = pd.DataFrame(),pd.Series()
        self.x_train,self.x_test,self.y_train,self.y_test = None,None,None,None
        self.y_predicted = None
        self.model = None
        self.models_list = [RandomForestClassifier(),SVC(),DecisionTreeClassifier(),
							KNeighborsClassifier(),GaussianNB(),MultinomialNB()]

    # data splitting
    def data_splitting(self):
        # splitting into target and feature
        self.features = self.data.iloc[:,1]
        self.target = self.data.iloc[:,0]

        # splitting test and train
        self.x_train,self.x_test,self.y_train,self.y_test = train_test_split(self.features,
																			 self.target,
																			 test_size=0.30)

        self.x_train = self.x_train.tolist()
        self.x_train = np.array(self.x_train)
        self.x_test = self.x_test.tolist()
        self.x_test = np.array(self.x_test)

        # applying SMOTE
        smote_obj = SMOTE()
        self.x_train,self.y_train = smote_obj.fit_resample(self.x_train,self.y_train)

    # training different set of models
    def all_model(self):
        for model in self.models_list:
            print("\nModel : ",model)
            model.fit(X=self.x_train,y=self.y_train)
            model_predict = model.predict(self.x_test)
            self.performance(predicted=model_predict)

    # training the model
    def model_train(self):
        print('\nTraining Model................')
        self.model = RandomForestClassifier(criterion='gini',max_depth=10,max_features=12)
        # forest_params = [{'max_depth': list(range(10, 15)), 'max_features': list(range(0,14))}]
        # clf = GridSearchCV(self.model, forest_params, cv = 10, scoring='accuracy')
        # print(clf)
        # clf.fit(X=self.x_train,y=self.y_train)
        self.model.fit(X=self.x_train,y=self.y_train)
        # print(clf.best_score_)
        # print(clf.best_params_)

    # predicting the value of xtest
    def predicting_xtest(self):
        self.y_predicted = self.model.predict(self.x_test)
        return self.y_predicted

    # getting performance metrix
    def performance(self,predicted):
        accuracyScore = accuracy_score(y_pred=predicted,y_true=self.y_test)
        print("\nAccuracy Score : ",accuracyScore*100)
        print("\nConfusion Matrix : ")
        print(confusion_matrix(y_pred=predicted, y_true=self.y_test))
        print("\nClassification Report : ")
        print(classification_report(y_pred=predicted,y_true=self.y_test))

    # generating pickle file
    def generating_pickle(self):
        print("\nGENERATING MODEL ......")
        # creating a pickle object
        pkl_file = open(".\Pickle\model.pkl","wb")
        pickle.dump(self.model,pkl_file)
        pkl_file.close()
        print("\nMODEL GENERATED READY TO USE [Pickle file created]\n")

    def model_training(self):
        # splitting data
        self.data_splitting()

        # for all the models
        # self.all_model()

        # model train
        self.model_train()
        # predicting xtest and checking performance
        self.performance(self.predicting_xtest())

        # generating pickle file
        self.generating_pickle()