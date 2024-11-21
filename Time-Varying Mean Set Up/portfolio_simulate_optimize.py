#!/usr/bin/env python3

import sys

import pandas as pd
import numpy as np

import gurobipy as gp
from gurobipy import GRB

import os
import json
import re

import argparse

# units='monthly'
# save_units = units.capitalize()
# num_sectors=5
# T=30
# num_years=30

parser = argparse.ArgumentParser()
parser.add_argument("INPREFIX", help="prefix of file (source)", type = str)
parser.add_argument("OUTPREFIX", help="prefix of file (dest)", type = str)

parser.add_argument("num_sectors", help="number of sectors", type = int)
parser.add_argument("T", help="months for true expected returns", type = int)
parser.add_argument("num_years", help="number of years", type = int)

parser.add_argument("-m","--monthly", help="monthly data?", action = "store_true")
parser.add_argument("-d","--daily", help="daily data?", action = "store_true")

args = parser.parse_args()

INPREFIX=args.INPREFIX
OUTPREFIX=args.OUTPREFIX

num_sectors=args.num_sectors
T=args.T
num_years=args.num_years

print('INPREFIX:', INPREFIX)
print('OUTPREFIX:', OUTPREFIX)
print('Number of Sectors:', num_sectors)
print('T:', T)
print('Number of Years:', num_years)

if args.monthly:
    units='monthly'
elif args.daily:
    units='daily'
    
print('Units:', units)
    
save_units = units.capitalize()

# num_sectors=5
# T=30
# num_years=30

if units=='monthly': 
    num_units=int(num_years*12)
else:
    num_units=int(num_years*365*(5/7))
    
if units == 'daily':
    if T == 260:
        N = [1, 10, 25, 50, 100, 150, 200, 250, 300, 350]
    elif T == 120:
        N = [1, 10, 25, 50, 75, 100, 125, 150]
elif units=='monthly':
    if T == 60:
        N = [1, 12, 24, 36, 48, 60, 96, 120]
    elif T == 30:
        N = [1, 6, 9, 12, 24, 36, 48, 60]
           
seed_list = [47,  54,  97, 123, 132, 222, 237, 241, 250, 254]

def true_mean_cov(units, T, num_sectors, num_units):
    print(os.path.join(INPREFIX,'data','Fama-French',str(num_sectors)+' Sector',units+'.csv'))
    df = pd.read_csv(os.path.join(INPREFIX,'data','Fama-French',str(num_sectors)+' Sector',units+'.csv'))
    
    returns = np.array(df.iloc[-num_units:,1:])

    P = returns.shape[0]

    true_expected_returns_set = {}
    
    print('Considering Fama-French '+str(num_sectors)+'-sector '+units+' data\nT =',str(T))
        
    for t in range(int(T/2), P-int(T/2)+1):
        true_expected_returns = np.mean(returns[t-int(T/2):t+int(T/2),:], axis=0)
        
        true_expected_returns_set[t] = true_expected_returns
            
    true_cov = np.cov(returns, rowvar=False)

    return true_expected_returns_set, true_cov

def simulate(true_mean, true_cov, seed):
    np.random.seed(seed=seed)
    simulated_returns = {}
    for k in (true_mean).keys():
        simulated_returns[k] = np.random.multivariate_normal(true_mean[k], true_cov)
    
    return simulated_returns

def markowitz(mean, cov, v):
    # Create a new model
    m = gp.Model("Markowitz")

    # Create variables

    x = {} # portfolio 

    for i in range(num_sectors):
        x[i] = m.addVar(lb=0, ub=np.Inf, vtype=GRB.CONTINUOUS, name="x_"+str(i))

    # Set objective

    m.setObjective(sum(mean[i]*x[i] for i in range(num_sectors)) , GRB.MAXIMIZE)

    # Add constraints

    m.addConstr(sum(cov[i][j] * x[i] * x[j] for i in range(num_sectors) for j in range(num_sectors)) <= v, 
                name='variance')
    
    m.addConstr(sum(x[i] for i in range(num_sectors)) == 1, name='total asset')

    # Optimize model

    m.setParam('OutputFlag', 0)

    m.optimize()

    m.printQuality()

    portfolio = []
    
    for v in m.getVars():
        portfolio.append(v.x)

    return portfolio, m.objVal

def min_variance(cov):
    # Create a new model
    m = gp.Model("Minimum Variance Portfolio")

    # Create variables

    x = {} # portfolio 

    for i in range(num_sectors):
        x[i] = m.addVar(lb=0, ub=np.Inf, vtype=GRB.CONTINUOUS, name="x_"+str(i))

    # Set objective

    m.setObjective(sum(cov[i][j] * x[i] * x[j] for i in range(num_sectors) for j in range(num_sectors)) , GRB.MINIMIZE)

    # Add constraints
    
    m.addConstr(sum(x[i] for i in range(num_sectors)) == 1, name='total asset')

    # Optimize model

    m.setParam('OutputFlag', 0)

    m.optimize()

    m.printQuality()

    portfolio = []
    
    for v in m.getVars():

        portfolio.append(v.x)

    
    return portfolio, m.objVal

true_mu, true_cov = true_mean_cov(units,T,num_sectors,num_units)

r_hat = {}
for seed in seed_list:
    r_hat[seed] = simulate(true_mu, true_cov, seed)

mu_hat = {}

for seed in seed_list:
    mu_hat[seed] = {}
    for n in N:
        mu_hat[seed][n] = {}
        for t in range(T+N[-1], list(r_hat[seed].keys())[-1]-T+1):
            estimated_expected_return = np.mean(np.array([r_hat[seed][i] 
                                                          for i in range((t-n),t)]), axis=0)
            mu_hat[seed][n][t] = np.array(estimated_expected_return)

min_var_portfolio, min_var_obj = min_variance(true_cov)

min_var_expected_return = {}
for t in true_mu.keys():
    min_var_expected_return[t] = np.dot(true_mu[t], min_var_portfolio)

mean_min_var_expected_return = np.mean(np.array([min_var_expected_return[t] for t in true_mu.keys()]))

print('Minimum Variance Objective: ', min_var_obj)

print('Expected Return of Min Variance Portfolio:', np.round(mean_min_var_expected_return,3))

equal_portfolio = np.array([1/num_sectors for i in range(num_sectors)])
equal_weight_variance = sum(true_cov[i][j] * equal_portfolio[i] * equal_portfolio[j] 
                            for i in range(num_sectors) for j in range(num_sectors))

print('Variance of Equal Weight Portfolio', np.round(equal_weight_variance,3))

if units=='monthly':
    v_factor = 1
elif units=='daily':
    v_factor = 0.1

v_begin = next(x[1] for x in enumerate([i*2.5*v_factor for i in range(11)]) if x[1] > min_var_obj)
v_end = v_begin+(20*v_factor)
precision = 2.5*v_factor
num_v = (v_end - v_begin) / precision
v_array = np.linspace(v_begin, v_end, int(num_v) + 1)

true_frontier = {}
estimated_frontier = {}
actual_frontier = {}
equal_frontier = {}

print('Computing Estimated and Actual Frontiers')

for seed in seed_list:
    estimated_frontier[seed] = {}
    actual_frontier[seed] = {}
    print('On seed ', seed)
    for n in N:
        estimated_frontier[seed][n] = {}
        actual_frontier[seed][n] = {}
        print('\tOn n = ', n)
        for t in mu_hat[seed][n].keys():
            if t % 150 == 0:
                print('\t\tOn index ',t)
            
            estimated_frontier[seed][n][t] = {}
            actual_frontier[seed][n][t] = {}
            
            for v in v_array:
                estimated_portfolio, estimated_obj = markowitz(mu_hat[seed][n][t], true_cov, v)
                estimated_frontier[seed][n][t][v] = estimated_obj
                
                actual_frontier[seed][n][t][v] = np.dot(true_mu[t+T], np.array(estimated_portfolio))

print('\nComputing True and Equal-Weight Frontiers')
                
for t in mu_hat[seed][n].keys():
    if t % 150 == 0:
        print('\tOn index ',t)

    true_frontier[t+T] = {}
    
    for v in v_array:
        true_portfolio, true_obj = markowitz(true_mu[t+T], true_cov, v)
        true_frontier[t+T][v] = true_obj
        
    equal_portfolio = np.array([1/num_sectors for i in range(num_sectors)])
    equal_frontier[t+T] = np.dot(true_mu[t+T], equal_portfolio)

with open(os.path.join(OUTPREFIX,'save','Fama-French Simulated',str(num_sectors)+' Sectors',save_units,
                       'actual_frontier ({} years, max_N={}, T={}).json'.format(num_years,N[-1],T)),'w') as f: 
    json.dump(actual_frontier, f, ensure_ascii=False, indent=4)
    
with open(os.path.join(OUTPREFIX,'save','Fama-French Simulated',str(num_sectors)+' Sectors',save_units,
                       'estimated_frontier ({} years, max_N={}, T={}).json'.format(num_years,N[-1],T)),'w') as f:
    json.dump(estimated_frontier, f, ensure_ascii=False, indent=4)
    
with open(os.path.join(OUTPREFIX,'save','Fama-French Simulated',str(num_sectors)+' Sectors',save_units,
                       'true_frontier ({} years, max_N={}, T={}).json'.format(num_years,N[-1],T)),'w') as f:
    json.dump(true_frontier, f, ensure_ascii=False, indent=4)
    
with open(os.path.join(OUTPREFIX,'save','Fama-French Simulated',str(num_sectors)+' Sectors',save_units,
                       'equal_frontier ({} years, max_N={}, T={}).json'.format(num_years,N[-1],T)),'w') as f:
    json.dump(equal_frontier, f, ensure_ascii=False, indent=4)  
