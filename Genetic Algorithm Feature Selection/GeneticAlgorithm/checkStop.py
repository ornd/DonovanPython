# -*- coding: utf-8 -*-
"""
Created on Wed Jan 23 09:04:58 2019

@author: dorn

Each checkStop function returns the stop flag, a boolean
    
"""
def maxNumberGenerations(population, max_number_generations, current_generation):
    """
    returns true if the current generation number is >= max number of generations
    
    Parameters
    ----------
    population: [] Individual
        The individuals of the current generation. (not used)
    max_number_generations: int
        Number of generations before stop flag set to true.
    current_generation: int
        Number of current generation, passed in all checkStop functions 
        as final argument.
    Returns
    -------
    bool: bool
        stop_flag
    """
    if (current_generation - 1) % max_number_generations == max_number_generations - 1:
        return True
    else:
        return False

def populationConvergence(population, *args):
    """
    returns true if the difference between any two individuals are > 2
    
    Parameters
    ----------
    population: Individual
        The individuals of the current generation.
    *args: iterable any
        Catches extra arguments
    Returns
    -------
    bool: bool
        stop_flag
    """
    def calculateParentDifference(individual1, individual2):
        """
        returns the difference between two individuals
        
        Parameters
        ----------
        individual1, individual2: Individual
            The individuals to be compaired.
        Returns
        -------
        difference: int
            The difference between the two individuals
        """
        difference = 0
        for idx, i in enumerate(individual1):
            if i != individual2[idx]:
                difference += 1
        return difference
    
    for individual1 in population:
        for individual2 in population:
            if calculateParentDifference(individual1, individual2) > 2:
                return False
    return True

def maxNumberGenerationsOrPopulationConvergence(population, max_number_generations, current_generation):
    """
    returns true if the current generation number is >= max number of generations
    or the difference between any two individuals are > 2
    
    Parameters
    ----------
    population: Individual
        The individuals of the current generation.
    max_number_generations: int
        Number of generations before stop flag set to true.
    current_generation: int
        Number of current generation, passed in all checkStop functions 
        as final argument.
    Returns
    -------
    bool: bool
        stop_flag
    """
    return maxNumberGenerations(current_generation, max_number_generations) or populationConvergence(population)