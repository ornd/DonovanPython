# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 15:12:34 2019

@author: Donovan

Loads a genetic algorithm historic object for analysis
"""
from pickle import load
import pandas as pd
from FeatureSelection.GeneticAlgorithm.checkStop import populationConvergence

def printConvergence(historic):
    true_list = []
    for generation in historic.historic:
        individuals = []
        for individual_and_score in generation.population:
            individuals.append(individual_and_score[1])
        true_list.append(populationConvergence(individuals))
    print(true_list)
    for idx, value in enumerate(true_list):
        if value == True:
            print(idx)
            break
    print('\n')

def printBestScore(historic):
    score_list = []
    for generation in historic.historic:
        score_list.append(generation.best_fit_score)
    print(str(score_list) + '\n')
        
def getFeatures(data, historic):
    count = 0
    for index, feature in enumerate(historic.best_individual):
        if feature == False:
            data = data.drop(data.columns[index - count], axis = 1)
            count = count + 1
    return data

def writeCSV(data, filename):
    import csv
    with open(filename, 'a', newline = '\n') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter = ',')
        row = str(data.columns[:-1].values)[1:-1].split(' ')
        csvwriter.writerow(row)

def countFeatures(csvfile_name):
    import csv
    with open(csvfile_name) as csvfile:
        csvreader = csv.reader(csvfile)
        word_counter = {}
        for row in csvreader:
            for col in row:
                if col in word_counter.keys():
                    word_counter[col] = word_counter[col] + 1
                else:
                    word_counter[col] = 1
    return word_counter

def writeDictKeysList(dict_keys, file_name = 'Feature_Set.txt'):
    with open(file_name, 'w') as file:
        file.write(str(dict_keys)[12:-3].replace('"', ''))
    
import numpy as np
average_unique = []
csv_filename = 'Feature_Sets.csv'
data = pd.read_csv('Data.csv')
historic = load(open('GA_Models/Historic.sav', 'rb'))
historic.savePopulationSize(file_extention = '.png')
historic.saveBestPopulationScores()
printConvergence(historic)
new_data = getFeatures(data.copy(), historic)
writeCSV(new_data, csv_filename)
historic.saveNumberUniqueIndividuals()
average_unique.append(np.mean(historic.getNumberUniqueIndividuals()))
print(average_unique)
print(np.mean(average_unique))
