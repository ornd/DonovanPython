# -*- coding: utf-8 -*-
"""
Author Donovan

Saves the genetic algorithm model.
"""

from GeneticAlgorithm.GeneticAlgorithm import Historic
from GeneticAlgorithm.GeneticAlgorithm import Generation
from GeneticAlgorithm.generateIndividual import generateBoolListIndividual
from GeneticAlgorithm.fitness import multiEnvMLFitnessLOOCV
from GeneticAlgorithm.selectFromPopulation import luckyTrueRandom, luckyRandom, allIndividuals, bestIndividuals, bestIndividual
from GeneticAlgorithm.createChildren import random, incestPrevention
from GeneticAlgorithm.mutatePopulation import singleIndexMutation, eachIndexMutation
from GeneticAlgorithm.checkStop import maxNumberGenerations, populationConvergence, maxNumberGenerationsOrPopulationConvergence
from GeneticAlgorithm.crossover import createChild

from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier

import pandas as pd
from pickle import dump
import sys

data_file_name = ''

data = pd.read_csv(data_file_name)
classifiers = []

# classifiers.append(SVC(kernel = 'linear'))
classifiers.append(KNeighborsClassifier())
# classifiers.append(GaussianNB())
# classifiers.append(DecisionTreeClassifier())
# classifiers.append(RandomForestClassifier())
# classifiers.append(AdaBoostClassifier())

generateIndividual = generateBoolListIndividual
fitness = multiEnvMLFitnessLOOCV
selectFromPopulation = luckyTrueRandom
createChildren = random
mutatePopulation = singleIndexMutation
stopFunction = maxNumberGenerations
reinitializeSelection = allIndividuals

historics = []
sys.stdout = open('CompTime.csv', 'a')
historic = Historic(generateIndividual, fitness, selectFromPopulation, 
                    createChildren, mutatePopulation, stopFunction, 
                    reinitializeSelection, 40, .25, .25, 1, 
                    generateBoolListIndividual = (len(data.columns) - 1, ), 
                    multiEnvMLFitnessLOOCV = (data, classifiers), 
                    luckyTrueRandom = (True, ), 
                    random = (createChild, 1, (len(data.columns) - 1) / 2), 
                    singleIndexMutation = (.15, ), maxNumberGenerations = (150, ), 
                    allIndividuals = ())
dump(historic, open('Historic.sav', 'wb'))