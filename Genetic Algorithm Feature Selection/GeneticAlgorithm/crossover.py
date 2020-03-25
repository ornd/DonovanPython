# -*- coding: utf-8 -*-
"""
Created on Wed Jan 23 09:04:58 2019

@author: dorn

Each crossover function takes a pair of individuals and crosses them over to create a child of the pair.
The child is returned
    
"""

def createChild(individual1, individual2):
    """
    Does crossover between two individuals. Each gene is selected individualy 
    with a equal chance of being from one or the other individual.
    
    Parameters
    ----------
    individual1, individual2: Individual
        The individuals to be crossed over.
    Returns
    -------
    child: Individual
        The child created from the pair of individuals.
    """
    from random import choice
    child = []
    for i in range(len(individual1)):
        child.append(choice([individual1[i], individual2[i]]))
    return child

