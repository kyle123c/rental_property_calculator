# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 19:41:37 2020

@author: 12253
"""
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib as plt

#Default Values based on Denver, CO in July 2020y
costs = {
        'interest rate' : 4.5,
        'loan term' : 30,
        'closing cost' : 3.0,
        'property tax' : 0.5,
        'insurance' : 0.5,
        'maintenance' : 1.0,
        'vacancy rate' : 5,
        'management' : 0,
        'expense growth' : 3,
        'rent growth' : 3,
        'appreciation' : 3,
        'cost to sell' : 6,
        }

def dictionary_to_table(dictionary):
    keys=list(dictionary.keys())
    values=list(dictionary.values())
    new_dictionary = {'Parameter' : keys, 'Value' : values}
    df = pd.DataFrame(new_dictionary)
    return df

def change_defaults(costs_dict):
    keys = list(costs_dict.keys())
    for x in range(len(costs_dict)):
        costs_dict[keys[x]] = float(input('Please enter your value for ' + keys[x] + ': '))
    return costs_dict

def principal_payment(price, down_payment, interest, loan_term, x):
    r = interest / 1200.0
    N = loan_term * 12.0
    P = price - down_payment
    payment = np.ppmt(r, x, N, P)
    return payment * (-1)

def interest_payment(price, down_payment, interest, loan_term, x):
    r = interest / 1200.0
    N = loan_term * 12.0
    P = price - down_payment
    payment = np.ipmt(r, x, N, P)
    return payment * (-1)

def rent_income(rent, growth, x):
    if (x < 13):
        current_rent = rent
        return current_rent
    elif ((x-1) % 12 == 0):
        current_rent = rent * (1 + growth/100.0)**((x-1)/12)
        return current_rent
    else:
        current_rent = rent * (1 + growth/100.0)**(((x-1) - ((x-1) % 12)) / 12)
        return current_rent
def expenses(price, taxes, insurance, maintenance, management, growth, vacancy, rent, x):
    if (x < 13):
        current_expenses = price * ((taxes + insurance + maintenance + management)/1200.0) + rent * (vacancy/100.0)
        return current_expenses
    elif ((x-1) % 12 == 0):
        current_expenses = (price * ((taxes + insurance + maintenance + management)/1200.0)) * (1 + growth/100.0)**((x-1)/12) + rent * (vacancy/100.0)
        return current_expenses
    else:
        current_expenses = (price * ((taxes + insurance + maintenance + management)/1200.0)) * (1 + growth/100.0)**(((x-1) - ((x-1) % 12)) / 12) + rent * (vacancy/100.0)
        return current_expenses
        
print('Welcome to Rental Property Calculator')
print('Here are our default values: ')
data = dictionary_to_table(costs)
print(data)
y_or_n = input('Would you like to use our default values? (Y or N): ')
if (y_or_n == 'n') or (y_or_n == 'n'):
    costs = change_defaults(costs)
    data = dictionary_to_table(costs)
    print(data)
user_input_labels = ['purchase price', 'down payment', 'intial repairs', 'rent', 'timeline']

for x in range(len(user_input_labels)):
    temp = float(input('Please enter your ' + user_input_labels[x] + ': '))
    costs[user_input_labels[x]] = temp

data = dictionary_to_table(costs)

table = pd.DataFrame(range(1, int(costs['timeline'])*12 + 1), columns = ['Month'])
print(table)
table['Monthly Income'] = table.apply(lambda row: rent_income(costs['rent'], costs['rent growth'], row['Month']), axis=1)
table['Principal Payment'] = table.apply(lambda row: principal_payment(costs['purchase price'], costs['down payment'], costs['interest rate'], costs['loan term'], row.Month), axis=1)
table['Interest Payment'] = table.apply(lambda row: interest_payment(costs['purchase price'], costs['down payment'], costs['interest rate'], costs['loan term'], row.Month), axis=1)
table['Total Payment'] = table.apply(lambda row: row['Principal Payment'] + row['Interest Payment'], axis=1)
table['Monthly Expenses'] = table.apply(lambda row: expenses(costs['purchase price'], costs['property tax'], costs['insurance'], costs['maintenance'], costs['management'], costs['expense growth'], costs['vacancy rate'], row['Monthly Income'], row['Month']), axis=1)
table['Cash Flow'] = table.apply(lambda row: row['Monthly Income'] - row['Total Payment'] - row['Monthly Expenses'], axis=1)
print(table.head(36))




#def mortgage(price, down_payment, interest, loan_term, timeline):
#    x = 1
#    sum_ipmt = 0
#    sum_ppmt = 0
#    database = pd.DataFrame(columns = ['Year', 'Interest', 'Principal', 'Total Mortgage'])
#    r = interest / 1200.0
#    N = loan_term * 12.0
#    T = timeline * 12.0
#    P = price - down_payment
#    while (x < T):
#        sum_ipmt += np.impt(r, x, N, P)
#        sum_ppmt += np.ppmt(r, x, N, P)
#        if (x % 12 == 0):
#            database.loc[x/12]=
#            
#        
#def cash_on_cash(cash_flow, investment):