# -*- coding: utf-8 -*-
"""
Created on Wed Jan 23 09:04:58 2019

@author: dorn

Contains two classes nessessary for genetic algoriths. 
These two classes are Generation and Historic. They were built in mind that 
genetic algorithms are highly modifiable.
The goal of these two classes is to allow the user to create there own 
genetic algorithms by passing in their own functions and parameters.

Generation
---------
Evaluates a single generation based on the passed fitness function. 
If lenght of population is less then population size, random individuals 
will be created based on the generateIndividual function until 
the length of population = population size. This functionality is for 
the initial population and reinitializing the population.

Historic
--------
Creates multiple generations based on the passed 
fitness and generateIndividual functions. 
After the initial generation is created, the next populations will be 
created based on the passed 
selectFromPopulation, createChildren, and mutatePopulation functions.

Examples
-------
>>> from GeneticAlgorithm import Historic
>>> from fitness import multiEnvMLFitnessLOOCV
>>> from generateIndividual import generateBoolSetIndividual
>>> from createChildren import random
>>> from mutatePopulation import singleIndexMutation
>>> from selectFromPopulation import luckyTrueRandom, allIndividuals
>>> from checkStop import populationConvergence
...
>>> from sklearn.svm import SVC
>>> from sklearn.neighbors import KNeighborsClassifier
>>> from sklearn.naive_bayes import GaussianNB
>>> from sklearn.tree import DecisionTreeClassifier
>>> from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
...
>>> data = #Pandas DataFrame
>>> classifiers = []
>>> classifiers.append(SVC(kernel = 'linear'))
>>> classifiers.append(KNeighborsClassifier())
>>> classifiers.append(GaussianNB())
>>> classifiers.append(DecisionTreeClassifier())
>>> classifiers.append(RandomForestClassifier())
>>> classifiers.append(AdaBoostClassifier())
...
>>> historic = Historic(generateIndividual = generateBoolSetIndividual, 
...                    fitness = multiEnvMLFitnessLOOCV, 
...                    selectFromPopulation = luckyTrueRandom, 
...                    createChildren = random, 
...                    mutatePopulation = singleIndexMutation,
...                    stopFunction = populationConvergence,
...                    reinitializeSelection = allIndividuals,
...                    initial_size = 40, best_percent = .25, 
...                    lucky_percent = .25, max_initialize_count = 10, 
...                    generateIndividual_args = (len(data.columns) - 1, ), 
...                    fitness_args = (data, classifiers), selectFromPopulation_args = (True, ), 
...                    createChildren_args = (.85, ), mutatePopulation_args = (.14, ),
...                    stopFunction_args = (), reinitializeSelection_args = ())
>>> historic.printResult()
"""
from time import clock
timer = clock()
from math import ceil
class Generation:
    """
    Evaluates a single generation based on the passed fitness function. 
    If lenght of population is less then population size, random individuals 
    will be created based on the generateIndividual function until 
    the length of population = population size. This functionality is for 
    the initial population and reinitializing the population.
        
    Parameters
    ----------
    generateIndividual: function
        This function needs to create a single individual for the population.
    fitness: class
        This class evaluates each individual. 
        fitness.population_sorted needs to be the sorted population.
    population: list
        Current population to be evaluated
    population_size = 100: int
        The size population should be at this generation. 
        Historic will pass the initial population size for the first generation 
        and for reinitializing the population. 
    generateIndividual_args: tuple
        Use this if the generateIndividual function requires arguments. 
        This tuple will be passed into the generateIndivual function.
    fitness_args: tuple
        Use this if the fitness __init__ function requires arguments. 
        This tuple will be passed into the fitness __init__ function.
    """
    def __init__(self, generateIndividual, fitness, population = [], 
                 population_size = 100, **kwargs):
        def initializePopulation(population_size, current_pop,
                                 generateIndividual, *args):
            i = len(current_pop)
            while i < population_size:
                current_pop.append(generateIndividual(*args))
                i+=1
            return current_pop
        
        #__init__
        if len(population) < population_size:
            fit = fitness(initializePopulation(population_size, population, 
                                               generateIndividual, 
                                               *kwargs[generateIndividual.__name__]), 
                          *kwargs[fitness.__name__])
        else:
            fit = fitness(population, *kwargs[fitness.__name__])
        population = fit.population_sorted
        self.fitness = fit
        self.population = population
        best_individual_and_score = population[0]
        self.best_individual = best_individual_and_score[1]
        self.best_fit_score = best_individual_and_score[0]
        
    def getPopulationSize(self):
        return len(self.population)
    
    def getUniqueCounts(self):
        import numpy as np
        individuals = [individual[1] for individual in self.population]
        unique_individuals, counts = np.unique(individuals, return_counts = True, 
                                               axis = 0)
        return unique_individuals

class Historic:
    """
    Creates multiple generations based on the passed 
    fitness and generateIndividual functions. 
    After the initial generation is created, the next populations will be 
    created based on the passed 
    selectFromPopulation, createChildren, and mutatePopulation functions.
            
    Parameters
    ----------
    generateIndividual: function
        This function needs to create a single individual for the population.
    fitness: class
        This class evaluates each individual. 
        fitness.population_sorted needs to be the sorted population.
        fitness.getBestScore takes two individuals' score and returns 
        the individual with the better score.
    selectFromPopulation: function
        This function selects individuals for crossover. This function uses 
        the number of best and the number of lucky individuals.
        These number of best and number of lucky individuals are found using 
        best_percent, lucky_percent, and the current population size.
    createChildren: function
        This function takes the selected individuals from selectFromPopulation
        and returns the population after crossover with these individuals.
    mutatePopulation: function
        Takes the population returned from createChildren and mutates 
        the population based on the chance_of_mutation
    stopFunction: function
        returns if stop flag = True
    reinitializeSelection: function
        This function selects individuals that will be carried to reinitialization
    initial_size = 100: int
        The size  of the initial population. 
        Historic will pass the initial population size for the first generation 
        and for reinitializing the population.
    best_percent = .25: decimal between 0 and 1
        The percent of best individuals to be chosen for selection.
    lucky_percent = .25: decimal between 0 and 1
        The percent of lucky individuals to be chosen for selection.
    max_initialize_count = 1: int
        Number of times reinitialization will occur when stop flag is set to True.
    generateIndividual_args: tuple
        Use this if the generateIndividual function requires arguments. 
        This tuple will be passed into the generateIndivual function.
    fitness_args: tuple
        Use this if the fitness __init__ function requires arguments. 
        This tuple will be passed into the fitness __init__ function.
    selectFromPopulation_args: tuple
        Use this if the selectFromPopulation function requires arguments. 
        This tuple will be passed into the selectFromPopulation_args function.
    createChildren_args: tuple
        Use this if the createChildren function requires arguments. 
        This tuple will be passed into the createChildren function.
    mutatePopulation_args: tuple
        Use this if the mutatePopulation function requires arguments. 
        This tuple will be passed into the mutatePopulation function.
    stopFunction_args: tuple
        Use this if the stopFunction function requires arguments. 
        This tuple will be passed into the stopFunction function.
    reinitializeSelection_args: tuple
        Use this if the reinitializeSelection function requires arguments. 
        This tuple will be passed into the reinitializeSelection function.
    """
    def __init__(self, generateIndividual, fitness, selectFromPopulation, 
                 createChildren, mutatePopulation, stopFunction, reinitializeSelection,
                 initial_size = 100, best_percent = .25, lucky_percent = .25, 
                 max_initialize_count = 1, **kwargs):
        
        def createFirstGen(generateIndividual = generateIndividual, 
                           fitness = fitness, population_size = initial_size, 
                           **kwargs):
            first_gen = Generation(generateIndividual, fitness, [], 
                                   initial_size, **kwargs)
            best_individual = first_gen.best_individual
            best_fit_score = first_gen.best_fit_score
            return first_gen, best_individual, best_fit_score
            
        
        def createNextPop(population, best_percent, lucky_percent, 
                          current_generation, **kwargs):
            
            breeders = selectFromPopulation(population.copy(), best_percent, lucky_percent, 
                                            *kwargs[selectFromPopulation.__name__])
            print('Survivors,' + str(clock() - timer))
            number_of_child = ceil(len(population) / 
                                   ((ceil(best_percent * len(population)) + 
                                     ceil(lucky_percent * len(population))) / 2))
            
            children = createChildren(breeders, number_of_child, 
                                      *kwargs[createChildren.__name__])
            print('Crossover,' + str(clock() - timer))
            population = mutatePopulation(children, *kwargs[mutatePopulation.__name__])
            print('Mutation,' + str(clock() - timer))
            stop = stopFunction(population, *kwargs[stopFunction.__name__], current_generation)
            print('Stop,' + str(clock() - timer))
            return population, stop
        
        def getRestOfGenerations(historic, best_fit_score, best_individual, generateIndividual, fitness, 
                                 selectFromPopulation, createChildren, 
                                 mutatePopulation, stopFunction, 
                                 reinitializeSelection, initial_size, 
                                 best_percent, lucky_percent,
                                 max_initialize_count, **kwargs):
            
            stop = False
            initialize_count = 1       
            i = 1
            while stop == False:
                next_pop, stop = createNextPop(population = historic[-1].population, 
                                               best_percent = best_percent, 
                                               lucky_percent = lucky_percent, 
                                               current_generation = len(historic), 
                                               **{ key: value for key, value in kwargs.items() if key not in {generateIndividual.__name__, fitness.__name__}})
                size_population = len(next_pop)
                
                if stop == True:
                    initialize_count = initialize_count + 1
                    
                    if initialize_count <= max_initialize_count:
                        stop = False
                        size_population = initial_size
                        next_pop = reinitializeSelection(next_pop, best_percent, 
                                                         lucky_percent, 
                                                         *kwargs[reinitializeSelection.__name__])
                        print(best_fit_score)
                        
                historic.append(Generation(population = next_pop, 
                                           population_size = size_population, 
                                           generateIndividual = generateIndividual, 
                                           fitness = fitness, 
                                           **{ key: value for key, value in kwargs.items() if key in {generateIndividual.__name__, fitness.__name__}}))
                print('Evaluation,' + str(clock() - timer))
                if(historic[-1].best_fit_score == 
                   historic[-1].fitness.getBestScore(historic[-1].best_fit_score, best_fit_score)):
                    best_individual = historic[-1].best_individual
                    best_fit_score = historic[-1].best_fit_score
                i = i + 1
                print('Generation ' + str(i) + ',' + str(clock() - timer))
            return historic, best_individual, best_fit_score

        # __init__  

        historic = []
        
        first_gen, best_individual, best_fit_score = createFirstGen(
                generateIndividual = generateIndividual, fitness = fitness,
                population_size = initial_size, 
                **{ key: value for key, value in kwargs.items() if key in {generateIndividual.__name__, fitness.__name__}})
        
        historic.append(first_gen)
        print('Initial Generation,' + str(clock() - timer))
        historic, best_individual, best_fit_score = getRestOfGenerations(
                historic, best_fit_score, best_individual, generateIndividual, fitness, selectFromPopulation, 
                createChildren, mutatePopulation, stopFunction, 
                reinitializeSelection, initial_size, best_percent, lucky_percent, 
                max_initialize_count, **kwargs)
                            
        self.historic = historic
        self.best_individual = best_individual
        self.best_fit_score = best_fit_score
        print('Historic,' +  str(clock() - timer) + '\n')
        
    def getPopulationSizes(self):
        population_sizes = []
        for generation in self.historic:
            population_sizes.append(generation.getPopulationSize())
        return population_sizes 

    def getBestPopulationScores(self):
        best_population_scores = []
        for generation in self.historic:
            if hasattr(generation.best_fit_score, '__iter__'):
                best_population_scores.append(generation.best_fit_score[0])
            else :
                best_population_scores.append(generation.best_fit_score)
        return best_population_scores 
    
    def getBestPopulationFeatureNum(self):
        best_population_scores = []
        for generation in self.historic:
            if hasattr(generation.best_fit_score, '__iter__'):
                best_population_scores.append(generation.best_fit_score[1])
            else :
                best_population_scores.append(generation.best_fit_score)
        return best_population_scores
    
    def printBestIndividual(self):
        print(self.best_individual)
            
    def printBestScore(self):
        print(self.best_fit_score)
        
    def printBestAccuracy(self):
        print(self.best_fit_score[0])
            
    def printResult(self):
        print('Best Individual: ' + str(self.best_individual))
        print('Accuracy: ' + str(self.best_fit_score[0]))
        print('Number of Features: ' + str(self.best_fit_score[1]))
        print('Generations: ' + str(len(self.historic)) + '\n')
            
    def writeResult(self, path = '', file_extention = ''):
        with open(path + 'Feature Sets' + file_extention + '.txt', 'a') as file:
            file.write(str(self.best_individual) + '\n')
        with open(path + 'Results' + file_extention + '.txt', 'a') as file:
            file.write('Best Individual: ' + str(self.best_individual) + '\n')
            file.write('Accuracy: ' + str(self.best_fit_score[0]) + '\n')
            file.write('Number of Features: ' + str(self.best_fit_score[1]) + '\n')
            file.write('Generations: ' + str(self.getPopulationSizes()) + '\n\n')
    
    def displayPopulationSize(self):
        plt = createBasicLineGraph(self.getPopulationSizes(), 'Population Sizes by Generation', 'Generations', 'Population Size')
        plt.show()
        
    def savePopulationSize(self, path = '', file_extention = ''):
        plt = createBasicLineGraph(self.getPopulationSizes(), 'Population Sizes by Generation', 'Generations', 'Population Size')
        plt.savefig(path + 'Population_Size' + file_extention + '.png')
        plt.show()
        
    def displayBestPopulationScores(self):
        plt = createMultipleLineGraph(self.getBestPopulationScores(), 'Best scores by Generation', 'Generations', 'Score Value')
        plt.show()
    
    def saveBestPopulationScores(self, path = '', file_extention = ''):
        data = []
        data.append(self.getBestPopulationScores())
        data.append(self.getBestPopulationFeatureNum())
        plt = createMultipleLineGraph(data, 'Best scores by Generation', 'Generations', 'Score Value')
        plt.savefig(path + 'Population_Score' + file_extention + '.png')
        plt.show()

    def getNumberUniqueIndividuals(self):
        number_unique_individuals_per_generation = []
        for generation in self.historic:
            number_unique_individuals_per_generation.append(len(generation.getUniqueCounts()))
        return number_unique_individuals_per_generation
    
    def displayNumberUniqueIndividuals(self):
        plt = createBasicLineGraph(self.getNumberUniqueIndividuals(), 'Unique Individuals by Generation', 'Generations', 'Number Unique Individuals')
        plt.show()
    
    def saveNumberUniqueIndividuals(self, path = '', file_extention = ''):
        plt = createBasicLineGraph(self.getNumberUniqueIndividuals(), 'Unique Individuals by Generation', 'Generations', 'Number Unique Individuals')
        plt.savefig(path + 'Unique_Individuals' + file_extention + '.png')
        plt.show()

def createBasicLineGraph(data, title= '', xlabel = '', ylabel = ''):
    from matplotlib import pyplot as plt
    plt.plot(data)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    return plt

def createMultipleLineGraph(data, title= '', xlabel = '', ylabel = ''):
    from matplotlib import pyplot as plt
    for row in data:
        plt.plot(row)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    return plt