# -*- coding: utf-8 -*-
"""
Created on Wed Jan 23 09:04:58 2019

@author: dorn

Each selectFromPopulation function returns selected individual(s) from population.
    
"""

def luckyTrueRandom(population, best_percent, lucky_percent, shuffle = True):
    """
    Select x best and y random individuals from population. 
    These individuals can be selected more than once.
        
    Parameters
    ----------
    population: [] Individual
        The individuals that can be selected from.
    best_percent: decimal between 0 and 1
        Used to find the number of best individuals (x) to select.
    lucky_percent: decimal between 0 and 1
        Used to find the number of random individuals (y) to select. 
        These individuals can be selected more than once and can be selected from best individuals.
    shuffle: boolean
        If True Shuffle the resulting selected individuals.
    Returns
    -------
    selected_population: [] Individual
        Selected Individuals
    """
    from random import shuffle
    def getBestAndLuckySampleSizes(population, best_percent, lucky_percent):
        from math import ceil
        best_sample_size = ceil(best_percent * len(population))
        lucky_sample_size = ceil(lucky_percent * len(population))
        return best_sample_size, lucky_sample_size
    
    def getSelectedPopulation(population, best_sample_size, lucky_sample_size):
        def getBestSample(population, best_sample_size, selected_population = []):
            for i in range(best_sample_size):
                selected_population.append(population[i][1])
            return selected_population
        
        def getLuckySample(population, lucky_sample_size, selected_population = []):
            from random import choice
            for i in range(lucky_sample_size):
                selected_population.append(choice(population)[1])
            return selected_population
        
        #getSelectedPopulation
        selected_population = getBestSample(population, best_sample_size)
        selected_population = getLuckySample(population, lucky_sample_size, selected_population)
        return selected_population
    
    #luckyRandom
    best_sample_size, lucky_sample_size = getBestAndLuckySampleSizes(population, best_percent, lucky_percent)
    selected_population = getSelectedPopulation(population, best_sample_size, lucky_sample_size)
    if shuffle: 
        shuffle(selected_population)
    return selected_population

def luckyRandom(population, best_percent, lucky_percent, shuffle = True):
    """
    Select x best and y random individuals from population. 
    These individuals can only be selected once.
        
    Parameters
    ----------
    population: [] Individual
        The individuals that can be selected from.
    best_percent: decimal between 0 and 1
        Used to find the number of best individuals (x) to select.
    lucky_percent: decimal between 0 and 1
        Used to find the number of random individuals (y) to select. 
        These individuals can be selected only once and cannot be selected from best individuals.
    shuffle: boolean
        If True Shuffle the resulting selected individuals.
    Returns
    -------
    selected_population: [] Individual
        Selected Individuals
    """
    from random import shuffle
    def getBestAndLuckySampleSizes(population, best_percent, lucky_percent):
        from math import ceil
        best_sample_size = ceil(best_percent * len(population))
        lucky_sample_size = ceil(lucky_percent * len(population))
        return best_sample_size, lucky_sample_size
    
    def getSelectedPopulation(population, best_sample_size, lucky_sample_size):
        def getBestSample(population, best_sample_size, selected_population = []):
            for i in range(best_sample_size):
                selected_population.append(population[i][1])
                population.remove(population[i])
            return population, selected_population
        
        def getLuckySample(population, lucky_sample_size, selected_population = []):
            from random import choice
            for i in range(lucky_sample_size):
                selected_individual = choice(population)
                selected_population.append(selected_individual[1])
                population.remove(selected_individual)
            return population, selected_population
        
        #getSelectedPopulation
        population, selected_population = getBestSample(population, best_sample_size)
        population, selected_population = getLuckySample(population, best_sample_size, selected_population)
        return selected_population
    
    #luckyRandom
    best_sample_size, lucky_sample_size = getBestAndLuckySampleSizes(population, best_percent, lucky_percent)
    selected_population = getSelectedPopulation(population, best_sample_size, lucky_sample_size)
    if shuffle: 
        shuffle(selected_population)
    return selected_population

def allIndividuals(population, *args):
    """
    Return all individuals from population.
        
    Parameters
    ----------
    population: [] Individual
        The individuals that will be returned.
    *args: any
        Catches extra arguments and does not use them.
    Returns
    -------
    selected_population: [] Individual
        Selected Individuals
    """
    return population

def bestIndividuals(population, best_percent, *args):
    """
    Select x best individuals from population.
        
    Parameters
    ----------
    population: [] Individual
        The individuals that will be returned.
    best_percent: decimal between 0 and 1
        Used to find the number of best individuals (x) to select.
    *args: any
        Catches extra arguments and does not use them.
    Returns
    -------
    selected_population: [] Individual
        Selected Individuals
    """
    def getBestSampleSize(population, best_percent):
        from math import ceil
        best_sample = ceil(best_percent * len(population))
        return best_sample

    def getBestSample(population, best_sample_size):
        selected_population = []
        for i in range(best_sample_size):
            selected_population.append(population[i])
        return selected_population
    
    return getBestSample(population, getBestSampleSize(population, best_percent))

def bestIndividual(population, *args):
    """
    Select only the best individual from population.
        
    Parameters
    ----------
    population: [] Individual
        The individuals in the population.
    *args: any
        Catches extra arguments and does not use them.
    Returns
    -------
    selected_population: [] Individual
        Selected Individuals
    """
    return population[0]