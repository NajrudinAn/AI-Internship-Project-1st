from django.db import models
import json
import os
import pandas as pd
import numpy as np
import math
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score



class project_model:
    def __init__(self,path):
        self.data = pd.read_csv(path)
        self.data = self.data.dropna()
        self.maped_dist={}

    # project Name
    def projectName(self,name):
        self.projectName = name

    # map data to number
    def mapToNumber(self,*column_name):
        columns = list(column_name) #list convert

        for col in columns:
            unique_values = self.data[col].unique()
            value_map = {}
            value_map_p ={}
            for i, value in enumerate(unique_values):
                value_map[value] = i
                value_map_p[i] = value
            self.data[col] = self.data[col].map(value_map)
            self.maped_dist[col] = value_map_p

    # handel missing values in number columns
    def toNum(self,*column):
        for col in column:
            self.data[col] = pd.to_numeric(self.data[col],errors="coerce")
            self.data[col] = self.data[col].interpolate(method='linear')

    # input values selection
    def inputData(self,types,*values):
        values_list = list(values) # coverting to list

        if types == 'select':
            self.inputs = self.data[values_list]
        elif types == "drop":
            self.inputs = self.data.drop(values_list,axis=1)
        else:
            print("Specify what to do, like input_data(drop/select, 'firstname','lastname',...)")
            
    # output values selection
    def outputData(self,types,*values):
        values_list = list(values) #list conversion

        if types == 'select':
            self.output = self.data[values_list]
        elif types == "drop":
            self.output = self.data.drop(values_list,axis=1)
        else:
            print("Specify what to do, like output_data(drop/select, 'firstname','lastname',...)")

    #  split data as x_train y_train x_test y_test and preprocess it
    def splitData(self,process=None):
        self.x_train,self.x_test,self.y_train,self.y_test = train_test_split(self.inputs,self.output,train_size=0.8)
        if process == 'processData':
            self.sc=StandardScaler()
            self.preProcessing = self.sc
            self.x_train=self.sc.fit_transform(self.x_train)
            self.x_test = self.sc.fit_transform(self.x_test)
    
    # pre-test random selected data from dataset
    def pre_predict(self,process=None):
        rowsData = self.inputs.sample(n=3)
        output_colunm = self.output.columns[0]
        expected_values = self.data.loc[rowsData.index, output_colunm].tolist()
        if process == "processData":
            rowsData_processed = self.sc.transform(rowsData)
        pred = self.model.predict(rowsData_processed).tolist()
        rowsData = rowsData.to_dict(orient='list')
        pre_test = {'rowsData':rowsData,'pred':pred,'expected_pred':expected_values,'accuracy':self.accuracy}
        return pre_test
    
    # train mode and accuracy measured
    def trainModel(self,model):
        self.model = model
        self.model.fit(self.x_train,self.y_train)
        y_pred = self.model.predict(self.x_test)
        self.accuracy = accuracy_score(self.y_test,y_pred)*100
        self.test_accuracy = self.pre_predict('processData')

    def data_info(self):
        total_rows,total_columns = self.inputs.shape
        total_columns = total_columns + self.output.shape[1]
        input_field = self.inputs.columns.tolist()
        total_train_rows = self.x_train.shape[0]
        total_test_rows = self.x_test.shape[0]
        preprocessing_model = self.preProcessing
        model_name = self.model
        maped_dist = dict(self.maped_dist)
        info = {'rows':total_rows,'columns':total_columns,'train_rows':total_train_rows,'test_rows':total_test_rows,'model_name':model_name,'preprocessing_model':preprocessing_model,'input_field':input_field,'maped_dist':maped_dist}
        return info
    
    def pred_input(self,input_values,process=None):
        inputData = pd.DataFrame([input_values])
        if process == "processData":
            inputData = self.sc.transform(inputData) #self.sc = standardScaller()
        pred = self.model.predict(inputData)
        return pred[0]



class projects:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)) # For Project directory Path
        self.dataset_paths = {
            'project1': os.path.join(self.base_dir, 'DataSets', 'bmd.csv'),         # Project 1 dataset path
            'project2': os.path.join(self.base_dir, 'DataSets', 'churn_data.csv')   # project 2 dataset path
    }
        
    def project1(self):
        
    #    path = 'E:\project\Internship\Project\Intern_Project\DataSets\bmd.csv'         #Datasets Path
        
        path = self.dataset_paths['project1']  # Path of dataset
        projectName = 'Predict fracture or not using KNN'
        self.project1 = project_model(path)
        self.project1.projectName(projectName)
        self.project1.mapToNumber('sex','medication')
        self.project1.inputData('drop','id','fracture')
        self.project1.outputData('select','fracture')
        self.project1.splitData("processData")
        self.project1.trainModel(KNeighborsClassifier(n_neighbors=12))

    def project2(self):
        
    #    path = 'E:\project\Internship\Project\Intern_Project\DataSets\churn_data.csv'         #Datasets Path
        
        path = self.dataset_paths['project2'] # Path of dataset
        projectName = 'Customer Churn Prediction using Logistic Regression'
        self.project2 = project_model(path)
        self.project2.projectName(projectName)
        self.project2.toNum('TotalCharges')
        self.project2.mapToNumber('PhoneService','Contract','PaperlessBilling','PaymentMethod')
        self.project2.inputData('drop','customerID','Churn')
        self.project2.outputData('select','Churn')
        self.project2.splitData("processData")
        self.project2.trainModel(LogisticRegression())
    








