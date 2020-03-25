# -*- coding: utf-8 -*-
"""
Created on Wed Jan 23 09:04:58 2019

@author: dorn

Each createChildren function selects pairs of individuals and crosses them over to create children of the pair.
All children are returned.
    
"""

def incestPrevention(breeders, number_of_child, crossover, chance_of_crossover, start_tolurance = None):
    """
    Select pairs based on how different each pair is. 
    The most different individuals are selected as a pair.
    Each individual is selected only once.
    Returns all children.
    
    Parameters
    ----------
    breeders:[] Individual
        The individuals that will be paired for cross over
    number_of_child: int
        Number of children each individual can make
    chance_of_crossover: decimal between 0 and 1
        Chance a child each child is made.
    start_tolurance = len(breeders[0])/2 : int
    Returns
    -------
    Children: [] Individual
        All children from each pair of individuals.
    References
    ----------
    Choubey, N. S., & Kharat, M. U. (2013). Hybrid system for handling premature convergence in GA–Case of grammar induction. Applied Soft Computing, 13(5), 2923-2931.
    https://www.sciencedirect.com/science/article/pii/S1568494612001846
    """
    from random import choice    
    def makeEvenByAddingRandom(breeders):
        if len(breeders) % 2 == 1:                                             #If length of breeders is odd, add a duplicate a random breeder.
            breeders.append(choice(breeders))
        return breeders

    def getChildren(breeders, number_of_child, crossover, chance_of_crossover, tolurance):
        from random import random
        def selectPair(breeders, tolurance):
            """
            Selects individuals that have differences > tolurance.
            returns these individuals and the remaining breeders
            
            Parameters
            ----------
            breeders: [] Individual
                The individuals that will be paired for cross over
            Returns
            -------
            individual1, individual2: Individual
                The individuals to be crossed over.
            breeders: [] Individual
                The individuals that have not been selected yet.
            """
            def parentDifference(individual1, individual2):
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
            
            #selectPair    
            individual1 = breeders[0]
            individual2 = breeders[1]
            count = 2
            
            while tolurance > parentDifference(individual1, individual2) and len(breeders) > 2:
                individual2 = breeders[count]
                count += 1
                
                if count >= len(breeders):
                    count = 2
                    tolurance -= 1
            breeders.remove(individual1)
            breeders.remove(individual2)
            return individual1, individual2, breeders

        #getChildren
        children = []
        while len(breeders) != 0:
            individual1, individual2, breeders = selectPair(breeders, tolurance)
            for j in range(number_of_child):
                if random() < chance_of_crossover:
                    children.append(crossover(individual1, individual2))
        return children
    
    #IncestPrevention
    if start_tolurance == None:
        start_tolurance = len(breeders[0]) / 2
    breeders = makeEvenByAddingRandom(breeders)
    return getChildren(breeders, number_of_child, crossover, chance_of_crossover, start_tolurance)

def random(breeders, number_of_child, crossover, chance_of_crossover, *args):
    """
    Select pairs at random. Each individual is selected only once.
    Returns all children.
    
    Parameters
    ----------
    breeders: [] Individual
        The individuals that will be paired for cross over
    number_of_child: int
        Number of children each individual can make
    chance_of_crossover: decimal between 0 and 1
        Chance a child each child is made.
    Returns
    -------
    Children: [] Individual
        All children from each pair of individuals.
    """
    from random import choice    
    def makeEvenByAddingRandom(breeders):
        if len(breeders) % 2 == 1:                                             #If length of breeders is odd, add a duplicate a random breeder.
            breeders.append(choice(breeders))
        return breeders

    def getChildren(breeders, number_of_child, crossover, chance_of_crossover):
        from random import random
        def selectPair(breeders):
            def selectAndRemoveBreeder(breeders):
                individual = breeders[randrange(len(breeders))]
                breeders.remove(individual)
                return individual
            
            #selectPair
            from random import randrange
            individual1 = selectAndRemoveBreeder(breeders)
            individual2 = selectAndRemoveBreeder(breeders)
            return individual1, individual2, breeders

        #getChildren
        children = []
        while len(breeders) != 0:
            individual1, individual2, breeders = selectPair(breeders)
            for j in range(number_of_child):
                if random() < chance_of_crossover:
                    children.append(crossover(individual1, individual2))
        return children
    
    #random
    breeders = makeEvenByAddingRandom(breeders)
    return getChildren(breeders, number_of_child, crossover, chance_of_crossover)