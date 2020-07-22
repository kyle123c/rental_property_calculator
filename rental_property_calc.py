# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 19:41:37 2020

@author: 12253
"""

import numpy as np
import seaborn as sns
import matplotlib as plt

#Default Values based on Denver, CO in July 2020y
costs = {
        'interest_rate' : 3.25,
        'loan_term' : 30,
        'closing_cost' : 3.0,
        'property_tax' : 0.5,
        'insurance' : 1850,
        'maintenance' : 1.0,
        'vacancy_rate' : 10,
        'management' : 0,
        'appreciation' : 3,
        'cost_to_sell' : 6,
        }

def change_defaults(costs_dict):
    keys = list(costs_dict.keys())
    print(keys)
    for x in range(len(keys)):
        keys[x] = keys[x].replace('_', ' ')
    print(keys)
    for x in range(len(costs_dict)):
        costs_dict[x] = input('Please enter your value for ' + keys[x] + ': ')
    print(costs)

print('Welcome to Rental Property Calculator')
print(costs)
y_or_n = input('Would you like to use our default values? (Y or N): ')
if (y_or_n == 'n') or (y_or_n == 'n'):
    change_defaults(costs)
purchase_price = input('Please enter your purchase price: ')
down_payment = input('Please enter your down payment amount: ')
repairs =  input('Please enter your necessary repairs cost: ')
rent =  input('Please enter your anticipated rent: ')
timeline =  input('Please enter your desired timeline: ')
