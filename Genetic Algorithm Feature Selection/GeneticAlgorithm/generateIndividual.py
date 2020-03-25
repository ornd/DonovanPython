# -*- coding: utf-8 -*-
"""
Created on Wed Jan 23 09:04:58 2019

@author: dorn

Contains functions that returns a single random individual.

"""
def generateBoolListIndividual(length):
    """
    Creates a random individual as a list of size length that contains boolean 
    values of True and False.
    
    Parameters
    ----------
    length: int
        length of the individual
    
    Returns
    -------
    individual: list
        The list of size length containing True and False values.

    """
    from random import choices
    individual = choices([True, False], k = length)
    return individual

def generateDiscreteListIndividual(length, options):
    """
    Creates a random individual as a list of size length that contains values 
    that were passed down as a list of options.
    
    Parameters
    ----------
    length: int
        length of the individual
    
    Returns
    -------
    individual: list
        The list of size length containing option values.

    """
    from random import choices
    individual = choices(options, k = length)
    return individual