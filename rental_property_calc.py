# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 19:41:37 2020

@author: 12253
"""
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


#Default Values based on Denver, CO in July 2020
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

#Turns dictionary of parameters into a easily viewable table
def dictionary_to_table(dictionary):
    keys=list(dictionary.keys())
    values=list(dictionary.values())
    new_dictionary = {'Parameter' : keys, 'Value' : values}
    df = pd.DataFrame(new_dictionary)
    return df
#Allows the user to change the default parameters
def change_defaults(costs_dict):
    keys = list(costs_dict.keys())
    for x in range(len(costs_dict)):
        costs_dict[keys[x]] = float(input('Please enter your value for ' + keys[x] + ': '))
    return costs_dict
#Calculates the amount paid towards the principal of the loan
def principal_payment(price, down_payment, interest, loan_term, x):
    r = interest / 1200.0
    N = loan_term * 12.0
    P = price - down_payment
    payment = np.ppmt(r, x, N, P)
    return payment * (-1)

#Calculates the amount paid towards the principal of the loan
def interest_payment(price, down_payment, interest, loan_term, x):
    r = interest / 1200.0
    N = loan_term * 12.0
    P = price - down_payment
    payment = np.ipmt(r, x, N, P)
    return payment * (-1)

#Calculates the current monthly rent
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

#Calculates the current monthly expenses    
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
    
#Calculates the cash on cash return
def cash_on_cash(cash_flow, down_payment, closing_costs, price, repairs):
    upfront_cost = price * closing_costs / 100.0 + down_payment + repairs
    cash_on_cash = cash_flow / (upfront_cost) * 1200.0
    return cash_on_cash

#Calculates home appreciation
def appreciation(price, appreciation, x):
    new_price = price * (1 + (appreciation/1200.0))**(x)
    return new_price

#Calculates the Internal Rate of Return
def irr(list_cash, x, sale):
    cash_flow = list_cash[0:(int(x))]
    last_value = cash_flow[(int(x)-1)]
    replacement = sale + last_value
    cash_flow[(int(x)-1)] = replacement
    irr = np.irr(cash_flow)
    return irr * 1200.0
print('******************************************************************************************')
print('Welcome to Rental Property Calculator')
print()
print('Here are our default values: ')
print()
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
print()
print(data)    

#Building dataframe from calculations
table = pd.DataFrame(range(1, int(costs['timeline'])*12 + 1), columns = ['Month'])
table['Monthly Income'] = table.apply(lambda row: rent_income(costs['rent'], costs['rent growth'], row['Month']), axis=1)
table['Principal Payment'] = table.apply(lambda row: principal_payment(costs['purchase price'], costs['down payment'], costs['interest rate'], costs['loan term'], row.Month), axis=1)
table['Interest Payment'] = table.apply(lambda row: interest_payment(costs['purchase price'], costs['down payment'], costs['interest rate'], costs['loan term'], row.Month), axis=1)
table['Total Payment'] = table.apply(lambda row: row['Principal Payment'] + row['Interest Payment'], axis=1)
table['Monthly Expenses'] = table.apply(lambda row: expenses(costs['purchase price'], costs['property tax'], costs['insurance'], costs['maintenance'], costs['management'], costs['expense growth'], costs['vacancy rate'], row['Monthly Income'], row['Month']), axis=1)
table['Cash Flow'] = table.apply(lambda row: row['Monthly Income'] - row['Total Payment'] - row['Monthly Expenses'], axis=1)
#Make cashflow into a list that can be indexed in the IRR formula
list_cash = table['Cash Flow'].tolist()
upfront_cost = (costs['purchase price'] * costs['closing cost'] / 100.0 + costs['down payment'] + costs['intial repairs']) * -1
list_cash.insert(0, upfront_cost)
table['Cash on Cash APR'] = table.apply(lambda row: cash_on_cash(row['Cash Flow'], costs['down payment'], costs['closing cost'], costs['purchase price'], costs['intial repairs']), axis=1)
table['Home Value'] = table.apply(lambda row: appreciation(costs['purchase price'], costs['appreciation'], row['Month']), axis=1)
table['Equity from Payments'] = table['Principal Payment'].cumsum()
table['Total Equity'] = table.apply(lambda row: row['Equity from Payments'] + costs['down payment'] + row['Home Value'] - costs['purchase price'], axis=1)
table['Cash to Receive from Sale'] = table['Total Equity'] - table['Home Value'] * costs['cost to sell'] / 100.0
table['IRR APR'] = table.apply(lambda row: irr(list_cash, row['Month'], row['Cash to Receive from Sale']), axis=1)

x_axis = [int(x) / 12.0 for x in table['Month']]
sns.set(style='darkgrid', palette='muted')
plt.figure(figsize=(16,8))
ax = plt.subplot(1, 2, 1)
ax2 = plt.subplot(1, 2, 2)
ax.plot(x_axis, table['Home Value'])
ax.plot(x_axis, table['Cash to Receive from Sale'])
ax.plot(x_axis, table['Total Equity'])
ax.set_title('Equity over Time')
ax.set_xlabel('Time (Years)')
ax.set_ylabel('Value ($)')
ax.legend(['Home Value', 'Cash from Sale', 'Total Equity'])
ax.set_xticks(range(int(costs['timeline'])+1))
ax.set_xticklabels(range(int(costs['timeline'])+1))
ax2.plot(x_axis, table['Monthly Income'])
ax2.plot(x_axis, table['Monthly Expenses'])
ax2.plot(x_axis, table['Cash Flow'])
ax2.set_title('Monthly Cashflow')
ax2.set_xlabel('Time (Years)')
ax2.set_ylabel('Value ($)')
ax2.legend(['Monthly Income', 'Monthly Expenses', 'Cash Flow'])
ax2.set_xticks(range(int(costs['timeline'])+1))
ax2.set_xticklabels(range(int(costs['timeline'])+1))
plt.tight_layout()
plt.show()

#Checking when properties become positive return investments
cash_on_cash_list = table['Cash on Cash APR']
irr_list = table['IRR APR']
for x in range(len(cash_on_cash_list)):
    if (cash_on_cash_list[x] > 0):
        time = x
        print()
        print('This property should have a positive cash on cash return at month: ' + str(x))
        break
    elif (x == range(len(cash_on_cash_list))):
        print('This property does not become cash on cash postive')
        break
        
for x in range(len(irr_list)):
    if (irr_list[x] > 0):
        time = x
        print()
        print('This property should have a positive IRR at month: ' + str(x))
        break
    elif (x == range(len(irr_list))):
        print('This property does not become IRR postive')
        break

print()
print(table.to_string())
table.to_csv('test.csv')


