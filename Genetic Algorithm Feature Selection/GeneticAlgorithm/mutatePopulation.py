# -*- coding: utf-8 -*-
"""
Created on Wed Jan 23 09:04:58 2019

@author: Donovan

Each mutationPopulation function mutates and returns the population based on chance_of_mutation.
    
"""
def eachIndexMutation(population, chance_of_mutation = .01):
    """
    Mutates the population based on chance_of_mutation per index in all individuals.
        
    Parameters
    ----------
    population: [] Individual
        The individuals that will be mutated
    chance_of_mutation: decimal between 0 and 1
        chance that mutation will occur per index in all individuals.
    *args: Any
        Catches extra arguments.
    Returns
    -------
    Population: [] Individual
    Mutated Population
    """
    from random import random
    def mutatePopulation(population, chance_of_mutation):
        def mutateIndividual(individual):
            """
            Chance to mutate individual at each individual's index. 
            Returns the mutated individual.
        
            Parameters
            ----------
            individual: Individual
                The individual that will be mutated
            Returns
            -------
            individual: Individual
                Mutated Individual
            """
            for index, feature in enumerate(individual):
                if random() < chance_of_mutation:
                    if feature:
                        individual[index] = False
                    else:
                        individual[index] = True
                    return individual
        
        #mutatePopulation
        for idx, individual in enumerate(population):
            population[idx] = mutateIndividual(individual)
        return population
            
    return mutatePopulation(population, chance_of_mutation)

def singleIndexMutation(population, chance_of_mutation = .14):
    """
    Mutates the population based on chance_of_mutation per individual.
        
    Parameters
    ----------
    population: [] Individual
        The individuals that will be mutated
    chance_of_mutation: decimal between 0 and 1
        chance that mutation will occur per individual.
    *args: Any
        Catches extra arguments.
    Returns
    -------
    Population: [] Individual
        Mutated Population
    """
    from random import random
    def mutatePopulation(population, chance_of_mutation):
        def mutateIndividual(individual):
            """
            Mutates the individual at random index. Returns the mutated individual.
        
            Parameters
            ----------
            individual: Individual
                The individual that will be mutated
            Returns
            -------
            individual: Individual
                Mutated Individual
            """
            random_index = int(random() * len(individual))
            if individual[random_index]:
                individual[random_index] = False
            else:
                individual[random_index] = True
            return individual
    
        #mutatePopulation
        for idx, individual in enumerate(population):
            if random() < chance_of_mutation:
                population[idx] = mutateIndividual(individual)
        return population
            
    return mutatePopulation(population, chance_of_mutation)