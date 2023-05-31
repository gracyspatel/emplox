# Pre-processing
# EMPLOYEE PERFORMANCE PREDICTION

# Importing Dependencies
import pickle
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import CountVectorizer

# Common function
# generating word token
def word_tok(paragraph):
    val_list = [w for w in paragraph.split(',')]
    return val_list

# Preprocessing class
class Preprocessing:
    def __init__(self):
        self.path = "./Data/EmployeeData.csv"
        self.data = None
        self.model = None
        self.encoders = {}
        self.tech_words = []
        self.tech_dict = {}

    # getting the data
    def read_data(self):
        return pd.read_csv(self.path)

    def lower_values(self,column_list):
        for column in column_list:
            self.data[column] = self.data[column].apply(lambda x: x.lower())

    def replace_values(self,column_list,value,to_value):
        for column in column_list:
            self.data[column] = self.data[column].replace(value,to_value)

    # getting department skills
    def get_department_skills(self,filepath):
        # getting encoders
        file = open(filepath, 'rb')
        self.encoders = pickle.load(file)
        file.close()
        return self.encoders['department_skills']

    # input data cleaning
    def input_data_cleaning(self,random_data):
        # changing tech skills from list to string
        random_data['Technical Skills'] = ', '.join(random_data['Technical Skills'])
        # encoding values
        for key in self.encoders:
            for value in random_data:
                if value == key:
                    random_data[value] = self.encoders[key].transform([random_data[value]])[0]
            if key == 'other-columns':
                for value in ['employee-code-quality','employee-quality-of-work',
                              'employee-debugging-skills','employee-time-management']:
                    random_data[value] = self.encoders[key].transform([random_data[value]])[0]
            if key == 'skills':
                random_data['Technical Skills'] = self.encoders[key].transform([random_data[
                                                                                   'Technical Skills']]).toarray()
                random_data['Technical Skills']  = list(random_data['Technical Skills'].sum(axis=0))

        new_data = [random_data['Education Level'],random_data['Department'],random_data[
            'employee-job-tenure']]
        new_data.extend(random_data['Technical Skills'])
        new_data.extend([random_data['employee-quality-of-work'],random_data['Workload'],random_data[
            'employee-peer-feedback'],random_data['employee-code-quality'],random_data[
            'employee-project-completion-rate'],random_data['employee-debugging-skills'],
                         random_data['employee-time-management'],random_data['Learning_Growth']])
        return new_data

    def new_prediction(self,data_to_predict,filepath):
        # getting encoders
        file = open(filepath, 'rb')
        self.model = pickle.load(file)
        file.close()

        return self.model.predict(np.array([data_to_predict]))

    # data encoding function common
    def encoding(self,column_list):
        for column_name in column_list:
            label_encoder = LabelEncoder()
            self.data[column_name] = label_encoder.fit_transform(self.data[column_name])
            self.encoders[column_name] = label_encoder

    # encoding good excellent poor
    def encoding_common(self,column_list):
        label_encoder = LabelEncoder()
        encoder = label_encoder.fit(self.data[column_list[0]])
        self.encoders['other-columns'] = encoder
        for column_name in column_list:
            self.data[column_name] = encoder.transform(self.data[column_name])

    # wordlist function
    def wordsList(self,sentence):
        for word in sentence.split(','):
            word = word.replace(' ','')
            if word not in self.tech_words:
                self.tech_words.append(word)

    # bag of words approach
    def bow_encoding(self,words_list1):
        # Applying Count Vectorize (Bag of Words)
        dictionary_Words_bow = CountVectorizer(encoding=None,lowercase=False,decode_error=None,stop_words=None,tokenizer=None)
        dictionary_Words_bow.fit(self.tech_words)
        self.encoders['skills'] = dictionary_Words_bow
        bow_x = dictionary_Words_bow.transform(words_list1).toarray()
        bow_x  = bow_x.sum(axis=0)
        return list(bow_x)

    # cleaning the datasets
    def data_cleaning(self,data):
        self.data = data

        # dropping Employee ID column
        data.drop(columns=['Employee Id'],inplace=True)

        # removing apostrophe
        data['Education Level'].replace(regex=True,inplace=True,to_replace=r"'",value=r"")

        # changing to lower case
        self.lower_values(column_list = ['Debugging_Skills', 'Learning_Growth', 'Quality_of_Work',
									   'Workload','Code_Quality', 'Time_Management'])

        # changing low to poor
        self.replace_values(column_list = ['Quality_of_Work','Code_Quality','Debugging_Skills'],
							value="low",to_value="poor")

        # changing time management
        self.data['Time_Management'] = self.data['Debugging_Skills'].replace("poor","good")

        # creating dictionary
        for index, row in self.data.iterrows():
            department = row["Department"]
            skills = row["Technical Skills"].split(",")
            if department in self.tech_dict:
                self.tech_dict[department].update(skills)
            self.tech_dict[department] = set(skills)

        self.encoders['department_skills'] = self.tech_dict

        # Encoding Feature column
        self.encoding(column_list=['Education Level','Department','Workload','Learning_Growth','Performance'])

        # Encoding other columns
        self.encoding_common(column_list=['Quality_of_Work','Code_Quality','Debugging_Skills','Time_Management'])

        # Encoding Technical Skills
        self.data['Technical Skills'].map(lambda sent:self.wordsList(sent))
        self.data['Technical Skills'] = self.data['Technical Skills'].apply(lambda sent:
                                                                          self.bow_encoding(word_tok(sent)))
        # creating a pickle object
        pkl_file = open(".\Pickle\cleaning.pkl","wb")
        pickle.dump(self.encoders,pkl_file)
        pkl_file.close()

        self.data['Employee Data'] =  self.data['Education Level']
        self.data['Employee Data'] = self.data['Employee Data'].apply(lambda x : [x])

        # appending other columns to Technical Skills
        for index,row in self.data.iterrows():
            row['Employee Data'].extend([row["Department"],row["Job Tenure"]])
            row['Employee Data'].extend(row["Technical Skills"])
            row['Employee Data'].extend([row["Quality_of_Work"],
                                            row["Workload"],row["Peer_Feedback"],
                                            row["Code_Quality"],row["Project_Completion_Rate"],
                                            row["Debugging_Skills"],row["Time_Management"],
                                            row["Learning_Growth"]])

        self.data.drop(['Education Level','Department','Job Tenure','Technical Skills','Quality_of_Work','Workload',
                        'Peer_Feedback','Code_Quality','Project_Completion_Rate','Debugging_Skills',
                        'Time_Management','Learning_Growth'], axis=1,inplace=True)
        return self.data