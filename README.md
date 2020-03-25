# DonovanPython
Python projects I have worked on.

The "Genetic Algorithm Feature Selection" folder contains some of my work with data reduction techniques.
This folder contain the following code:
  GA_Driver.py - this code creates a historic class object and saves the object for further analysis
  HistoricAnalysis.py - This code loads a historic object and uses built in functions to analyse the genetic algorithm.
  results.py - This is a simple script that imports a historic and prints the highest fitness score (<accuracy of model>, <number of features used>).
  GeneticAlgorithm/ This folder contains all the required scripts to create a genetic algorithm historic class object.

The "Weighted Cluster Graph" folder contains some of my work with population analysis.
The folder contains the following code:
  Clustering.py - contains the code used to create weighted graph class objects.
  CreateGraphs.py - This python script imports a xlsx file, detects all the sheet_names, and creates a network models where the sheet names is the session.
                  - It also has a function that combines common edge weights from multiple tasks.
  EdgeDefinitions.py - This file contains functions that defines when an edge between two nodes should be added.
                     - These functions are passed to Clustering.py WeightedGraph class objects.
