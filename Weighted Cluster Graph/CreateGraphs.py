# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 12:31:26 2020

@author: Donovan
"""
import pandas as pd
from Clustering import WeightedClusterGraph
from EdgeDefinitions import SpearmansCorrelation, CosineSimilarity
import xlrd

def averageTrialsPerSubject(data):
    """
    Multiple Subjects performed each task multiple times. 
    This function averages each feature by subject.
    """
    average_data = data.drop('Trial', axis = 1)
    return average_data.groupby('Subject').mean()

def graphsPerTasks(file_names):
    for file_name in file_names:
        file_information = xlrd.open_workbook(r'Data/' + file_name + '.xlsx', on_demand = True)
        sheet_names = file_information.sheet_names()

        for sheet_name in sheet_names:
            data = pd.read_excel('Data/' + str(file_name) + '.xlsx', sheet_name = str(sheet_name))
            average_data = averageTrialsPerSubject(data)
            X = average_data.values
            y = average_data.index.values
            WG = WeightedClusterGraph(X, y, SpearmansCorrelation, name = 'AVG_' + str(sheet_name))
            WG.DrawGraph(folder_extention = str(file_name) + '/')
            WG.convert2Excel(file_name + '_')

def combineEdgeWeights(file_names, file_paths, folder_location):
    """
    This function combines multiple WG.convert2Excel Files.
    """
    for path in file_paths:
        sum_weights = pd.read_csv(str(folder_location) + str(file_names[0]) + str(path) + '.csv')
        for i in range(len(file_names) - 1):
            temp_data = pd.read_csv(str(folder_location) + str(file_names[i+1] + str(path) + '.csv'))
            sum_weights = sum_weights.append(temp_data)
        sum_weights = sum_weights.groupby(['SOURCE', 'TARGET']).sum()
        sum_weights.to_csv(str(folder_location) + 'Combined_' + str(path) + '.csv')
        
file_names = ['Task1', 'Task2', 'Task3']
file_paths = ['_AVG_0', '_AVG_1 wk', '_AVG_4 wks']
folder_location = 'Graphs/Spearman/All_Features/99_975_95/Combined/'
graphsPerTasks(file_names)
file_names = ['PT', 'NP', 'WB']
combineEdgeWeights(file_names, file_paths, folder_location)