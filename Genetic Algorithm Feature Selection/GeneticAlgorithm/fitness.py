# -*- coding: utf-8 -*-
"""
Created on Wed Jan 23 09:04:58 2019

@author: dorn

Each fitness class finds the fitness of each individual and sorts each
individual based on perfered fitness score.

self.population_sorted = the population sorted based on fitness scores.

getBestScore(self, fit_score1, fit_score2) = helper function that returns the best score

both self.population_sorted and getBestScore are required for all fitness functions.
    
"""

#import warnings
#warnings.filterwarnings('ignore')
import numpy as np
import pandas as pd

class fitness:
    def __init__(self, population, *args, **kwargs):
        self.population_sorted = []
        if self.population_sorted == []:
            raise NotImplementedError("self.population_sorted must be implemented. population_sorted is the population sorted from best to worst fitness scores. It is in the from [scores_and_individuals] where a scores_and_individuals is in the form [fitness, individual]\n")
            
    def getBestScore(self, fit_score1, fit_score2):
        """
        Helper function that returns the best score
        
        Parameters
        ----------
        fit_score1, fit_score2: scores returned by fitness function.
            Scores that are to be compaired.
            
        Returns
        -------
        fit_score: score returned by fitness function
            The score that was better.
        """
        return NotImplementedError("getBestScore(self, fit_score1, fit_score2) function must be implemented. \ngetBestScore(self, fit_score1, fit_score2) returns the better fitness score.")

class multiEnvMLFitnessKFold(fitness):
    """
    Finds the fitness of each individual based on multiple machine learning (ML)
    algorithms accuracy using the K_fold cross validation technique and sorts each
    individual based on highest accuracy first and number of feature second.
        
    Parameters
    ----------
    population: Individual
        The individuals that will be evaluated
    data: Pandas DataFrame
        The data used to build ML models
    classifiers: list ML classifier Objects
        classifiers to be used to obtain accuracies for fitness
    k = 10: int
        represent the number of folds to use in K_fold cross-validation. Has no
        impact if using leave-one out cross-validation
    """
    def __init__(self, population, data, classifiers, k = 10):
        def getFitnessScores(data, population, classifiers, k):
            def individualFitness(data, individual, classifiers, k):
                def getNumberOfFeatures(individual):
                    numberOfFeatures = 0
                    for feature in individual:
                        if feature == True:
                            numberOfFeatures += 1
                    return numberOfFeatures
                
                def getFeatureIndexes(individual):
                    count = 0
                    feature_indexes = []
                    for index in individual:
                        if index == True:
                            feature_indexes.append(count)
                        count += 1
                    return feature_indexes
                
                def getAverageAccuracy(data, classifiers, k):
                    from sklearn.preprocessing import StandardScaler
                    from sklearn.cross_validation import cross_val_score
                    def getAccuracy(classifier, X, y):
                        classifier.fit(X,y)
                        X = pd.DataFrame(X)
                        return np.mean(cross_val_score(classifier, X, y, k)) * 100

                    #getAverageAccuracy
                    X = data.iloc[:, getFeatureIndexes(individual)]
                    y = pd.Series(data.iloc[:, -1].values)
                
                    # Feature Scaling
                    sc = StandardScaler()
                    X = sc.fit_transform(X)
                
                    accuracies = []
                    for classifier in classifiers:
                        accuracies.append(getAccuracy(classifier, X, y, k))
                    return np.mean(accuracies)
                
                #individualFitness
                number_of_features = getNumberOfFeatures(individual)
                if number_of_features == 0:
                    return (0,0)
                else:
                    return (getAverageAccuracy(data, classifiers, k), number_of_features)
            
            #getFitnessScores
            fitness_scores = []
            unique_individuals, counts = np.unique(population, return_counts = True, 
                                                   axis = 0)
            population = []
            for idx, individual in enumerate(unique_individuals):
                individual = list(individual)
                fitness_score = individualFitness(data, individual, classifiers)
                for i in range(counts[idx]):
                    fitness_scores.append(fitness_score)
                    population.append(individual)
            return fitness_scores, population        
        
        fitness_scores, population = getFitnessScores(data, population, classifiers)
        population_sorted = sorted(zip(fitness_scores, population), 
                                   key = lambda x:([-x[0][0], x[0][1]]))
        self.population_sorted = population_sorted
        
    def getBestScore(self, fit_score1, fit_score2):
        """
        Helper function that returns the best score
        
        Parameters
        ----------
        fit_score1, fit_score2: scores returned by fitness function.
            Scores that are to be compaired.
            
        Returns
        -------
        fit_score: score returned by fitness function
            The score that was better.
        """
        if fit_score1[0] > fit_score2[0]:
            return fit_score1
        elif fit_score1[0] == fit_score2[0] and fit_score1[1] <= fit_score2[1]:
            return fit_score1
        else:
            return fit_score2

class multiEnvMLFitnessLOOCV(fitness):
    """
    Finds the fitness of each individual based on multiple machine learning (ML)
    algorithms accuracy using the leave one out cross validation technique and sorts each
    individual based on highest accuracy first and number of feature second.
        
    Parameters
    ----------
    population: Individual
        The individuals that will be evaluated
    data: Pandas DataFrame
        The data used to build ML models
    validation_technique: String
        String value that represents the validation technique to be used.
        Currently "K_fold" for K fold cross-validation and "LOOCV" for leave-one
        out cross-validation are implemented.
    classifiers: list ML classifier Objects
        classifiers to be used to obtain accuracies for fitness
    """
    def __init__(self, population, data, classifiers):
        def getFitnessScores(data, population, classifiers):
            def individualFitness(data, individual, classifiers):
                def getNumberOfFeatures(individual):
                    numberOfFeatures = 0
                    for feature in individual:
                        if feature == True:
                            numberOfFeatures += 1
                    return numberOfFeatures
                
                def getFeatureIndexes(individual):
                    count = 0
                    feature_indexes = []
                    for index in individual:
                        if index == True:
                            feature_indexes.append(count)
                        count += 1
                    return feature_indexes
                
                def getAverageAccuracy(data, classifiers):
                    from sklearn.preprocessing import StandardScaler
                    from Test.LeaveOneOutCrossVal import LeaveOneOutCrossVal as LOOCV
                    def getAccuracy(classifier, X, y):
                        classifier.fit(X,y)
                        X = pd.DataFrame(X)
                        return np.mean(LOOCV(classifier, X, y))

                    #getAverageAccuracy
                    X = data.iloc[:, getFeatureIndexes(individual)]
                    y = pd.Series(data.iloc[:, -1].values)
                
                    # Feature Scaling
                    sc = StandardScaler()
                    X = sc.fit_transform(X)
                
                    accuracies = []
                    for classifier in classifiers:
                        accuracies.append(getAccuracy(classifier, X, y))
                    return np.mean(accuracies) * 100
                
                #individualFitness
                number_of_features = getNumberOfFeatures(individual)
                if number_of_features == 0:
                    return (0,0)
                else:
                    return (getAverageAccuracy(data, classifiers), number_of_features)
            
            #getFitnessScores
            fitness_scores = []
            unique_individuals, counts = np.unique(population, return_counts = True, 
                                                   axis = 0)
            population = []
            for idx, individual in enumerate(unique_individuals):
                individual = list(individual)
                fitness_score = individualFitness(data, individual, classifiers)
                for i in range(counts[idx]):
                    fitness_scores.append(fitness_score)
                    population.append(individual)
            return fitness_scores, population        

        fitness_scores, population = getFitnessScores(data, population, classifiers)
        population_sorted = sorted(zip(fitness_scores, population), 
                                   key = lambda x:([-x[0][0], x[0][1]]))
        self.population_sorted = population_sorted
        
    def getBestScore(self, fit_score1, fit_score2):
        if fit_score1[0] > fit_score2[0]:
            return fit_score1
        elif fit_score1[0] == fit_score2[0] and fit_score1[1] <= fit_score2[1]:
            return fit_score1
        else:
            return fit_score2
        
class mlFitnessKFold(fitness):
    """
    Finds the fitness of each individual based on the machine learning (ML)
    algorithm accuracy using the K_fold cross validation technique and sorts each
    individual based on highest accuracy first and number of feature second.
        
    Parameters
    ----------
    population: Individual
        The individuals that will be evaluated
    data: Pandas DataFrame
        The data used to build ML models
    classifier: ML classifier Object
        ML technique used to obtain fitness score
    k = 10: int
        represent the number of folds to use in K_fold cross-validation. Has no
        impact if using leave-one out cross-validation
    """
    def __init__(self, population, data, classifier, k = 10):
        def getFitnessScores(data, population, classifier):
            def individualFitness(data, individual, classifier):
                def getNumberOfFeatures(individual):
                    numberOfFeatures = 0
                    for feature in individual:
                        if feature == True:
                            numberOfFeatures += 1
                    return numberOfFeatures
                
                def getFeatureIndexes(individual):
                    count = 0
                    feature_indexes = []
                    for index in individual:
                        if index == True:
                            feature_indexes.append(count)
                        count += 1
                    return feature_indexes
                
                def getAccuracy(data, classifier):
                    from sklearn.preprocessing import StandardScaler
                    from sklearn.cross_validation import cross_val_score
                    
                    X = data.iloc[:, getFeatureIndexes(individual)]
                    y = pd.Series(data.iloc[:, -1].values)
                
                    # Feature Scaling
                    sc = StandardScaler()
                    X = sc.fit_transform(X)
                
                    # Fitting classifier to the Training set
                    classifier.fit(X, y)   
                        
                    X = pd.DataFrame(X)
                    return np.mean(cross_val_score(classifier, X, y, k)) * 100
    
                #individualFitness
                number_of_features = getNumberOfFeatures(individual)
                if number_of_features == 0:
                    return (0,0)
                else:
                    return (getAccuracy(data, classifier), number_of_features)
            
            #getFitnessScores
            fitness_scores = []
            unique_individuals, counts = np.unique(population, return_counts = True, 
                                                   axis = 0)
            population = []
            for idx, individual in enumerate(unique_individuals):
                individual = list(individual)
                fitness_score = individualFitness(data, individual, classifier)
                for i in range(counts[idx]):
                    fitness_scores.append(fitness_score)
                    population.append(individual)
            return fitness_scores, population        
        
        fitness_scores, population = getFitnessScores(data, population, classifier)
        population_sorted = sorted(zip(fitness_scores, population), 
                                   key = lambda x:([-x[0][0], x[0][1]]))
        self.population_sorted = population_sorted
        
    def getBestScore(self, fit_score1, fit_score2):
        if fit_score1[0] > fit_score2[0]:
            return fit_score1
        elif fit_score1[0] == fit_score2[0] and fit_score1[1] <= fit_score2[1]:
            return fit_score1
        else:
            return fit_score2
        
class mlFitnessLOOCV(fitness):
    """
    Finds the fitness of each individual based on the machine learning (ML)
    accuracy using the leave one out cross validation technique and sorts each
    individual based on highest accuracy first and number of feature second.
        
    Parameters
    ----------
    population: Individual
        The individuals that will be evaluated
    data: Pandas DataFrame
        The data used to build ML models
    classifier: ML classifier Object
        ML technique used to obtain fitness score
    """
    def __init__(self, population, data, classifier):
        def getFitnessScores(data, population, classifier):
            def individualFitness(data, individual, classifier):
                def getNumberOfFeatures(individual):
                    numberOfFeatures = 0
                    for feature in individual:
                        if feature == True:
                            numberOfFeatures += 1
                    return numberOfFeatures
                
                def getFeatureIndexes(individual):
                    count = 0
                    feature_indexes = []
                    for index in individual:
                        if index == True:
                            feature_indexes.append(count)
                        count += 1
                    return feature_indexes
                
                def getAccuracy(data, classifier):
                    from sklearn.preprocessing import StandardScaler
                    from Test.LeaveOneOutCrossVal import LeaveOneOutCrossVal as LOOCV
                    
                    X = data.iloc[:, getFeatureIndexes(individual)]
                    y = pd.Series(data.iloc[:, -1].values)
                
                    # Feature Scaling
                    sc = StandardScaler()
                    X = sc.fit_transform(X)
                
                    # Fitting classifier to the Training set
                    classifier.fit(X, y)   
                        
                    X = pd.DataFrame(X)
                    return np.mean(LOOCV.LeaveOneOutCrossVal(classifier, X, y)) * 100
    
                #individualFitness
                number_of_features = getNumberOfFeatures(individual)
                if number_of_features == 0:
                    return (0,0)
                else:
                    return (getAccuracy(data, classifier), number_of_features)
            
            #getFitnessScores
            fitness_scores = []
            unique_individuals, counts = np.unique(population, return_counts = True, 
                                                   axis = 0)
            population = []
            for idx, individual in enumerate(unique_individuals):
                individual = list(individual)
                fitness_score = individualFitness(data, individual, classifier)
                for i in range(counts[idx]):
                    fitness_scores.append(fitness_score)
                    population.append(individual)
            return fitness_scores, population        
        
        fitness_scores, population = getFitnessScores(data, population, classifier)
        population_sorted = sorted(zip(fitness_scores, population), 
                                   key = lambda x:([-x[0][0], x[0][1]]))
        self.population_sorted = population_sorted
        
    def getBestScore(self, fit_score1, fit_score2):
        if fit_score1[0] > fit_score2[0]:
            return fit_score1
        elif fit_score1[0] == fit_score2[0] and fit_score1[1] <= fit_score2[1]:
            return fit_score1
        else:
            return fit_score2