# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 13:02:15 2020

@author: Donovan
"""
from pickle import load

with open('Best_Fit_Scores.txt', 'w') as file:
    historic = load(open('GA_Models/Historic.sav', 'rb'))
    file.write(str(historic.best_fit_score)[1:-1] + '\n')
