import pandas as pd
import numpy as np

import gurobipy as gp
from gurobipy import GRB

import os
import json

def true_mean_cov(data, units, num_sectors, num_units):
    if data == 'Fama-French':
        df = pd.read_csv(os.path.join('data','Fama-French',str(num_sectors)+' Sector',units+'.csv'))

        returns = np.array(df.iloc[-num_units:,1:])

        print('Considering Fama-French '+str(num_sectors)+'-sector '+units+' data')
        
    elif data == 'GICS':
        df = pd.read_csv(os.path.join('data','GICS','GICS_returns.csv'), header=None)
    
        returns = np.array(df)*100

        print('Considering GICS data')
            
    true_mean = np.mean(returns, axis=0)
    true_cov = np.cov(returns, rowvar=False)

    return true_mean, true_cov

def simulate(true_mean, true_cov, N):
    simulated_returns = np.random.multivariate_normal(true_mean, true_cov, N)    
    return simulated_returns

def robust(mean, cov, Xi, v, kappa):
    # Create a new model
    m = gp.Model("Robust")
    
    # Supress output
    m.setParam('OutputFlag', 0)

    # FeasibilityTol and OptimalityTol -- for when Xi is very small and we need to manage numerical issues
    # m.setParam('FeasibilityTol', 1e-9)
    # m.setParam('OptimalityTol', 1e-9)

    # Create variables

    num_sectors = len(mean)

    x = m.addMVar(num_sectors, lb=0, ub=np.inf, vtype=GRB.CONTINUOUS, name='x')
    z = m.addVar(lb=0,ub=np.inf, vtype=GRB.CONTINUOUS, name='z')

    # Set objective
    
    m.setObjective(mean@x - kappa*z , GRB.MAXIMIZE)    
    
    # Add constraints
    
    m.addConstr(z*z >= x @ Xi @ x, name='robust term')
        
    m.addConstr(x @ cov @ x <= v, name='variance')
    
    m.addConstr(np.ones(num_sectors)@x == 1, name='total asset')

    # Optimize model

    m.optimize()

    m.printQuality()
    
    portfolio = [var.x for var in m.getVars() if "x" in var.VarName]

#     print('Obj: %g' % m.objVal)
    
    return portfolio, m.objVal

def markowitz(mean, cov, v):
    # Create a new model
    m = gp.Model("Markowitz")
    
    m.setParam('OutputFlag', 0)

    # Create variables

    num_sectors = len(mean)

    x = m.addMVar(num_sectors, lb=0, ub=np.inf, vtype=GRB.CONTINUOUS, name='x')

    # Set objective

    m.setObjective(mean@x , GRB.MAXIMIZE)

    # Add constraints

    m.addConstr(x @ cov @ x <= v, name='variance')
    
    m.addConstr(np.ones(num_sectors)@x == 1, name='total asset')

    # Optimize model

    m.optimize()

    m.printQuality()

    portfolio = [var.x for var in m.getVars() if "x" in var.VarName]

    # print('Obj: %g' % m.objVal)
    
    return portfolio, m.objVal

def min_variance(cov):
    # Create a new model
    m = gp.Model("Minimum Variance Portfolio")

    m.setParam('OutputFlag', 0)
    
    # Create variables

    num_sectors = cov.shape[0]
    
    x = m.addMVar(num_sectors, lb=0, ub=np.inf, vtype=GRB.CONTINUOUS, name='x')

    # Set objective

    m.setObjective(x @ cov @ x, GRB.MINIMIZE)

    # Add constraints
    
    m.addConstr(np.ones(num_sectors)@x == 1, name='total asset')

    # Optimize model

    m.optimize()

    m.printQuality()
    
    portfolio = [var.x for var in m.getVars() if "x" in var.VarName]

#     print('Obj: %g' % m.objVal)
    
    return portfolio, m.objVal

def choose_kappa(mu_hat,sigma,Xi,v,lb=2,ub=4):

    mid_point = (lb+ub)/2
    
    lin_term = np.abs(mu_hat.mean())
    
    inv_diagXi = 1/np.diag(Xi)
    quad_term_portfolio = inv_diagXi/inv_diagXi.sum()  # alternate choice for \bar\bar x where we normalize Xi    
        
    quad_term = np.sqrt(quad_term_portfolio@Xi@quad_term_portfolio)
        
    kappa = float(lin_term/(mid_point*quad_term))    
        
    stop_criteria = False

    iter_count = 0
    
    while not stop_criteria:
        
        robust_estimated_portfolio, robust_estimated_obj = robust(mu_hat, sigma, Xi, v, kappa)        
                        
        lin_term = np.abs(mu_hat@robust_estimated_portfolio)
        quad_term = np.sqrt(robust_estimated_portfolio@Xi@robust_estimated_portfolio)
        ratio = lin_term/(kappa*quad_term)
        
        if ratio <= lb or ratio >= ub:
            kappa = float(lin_term/((mid_point)*quad_term))
            if iter_count >= 100:
                print('Iteration Depth Exceeded.')
                break
        else:
            stop_criteria = True
            
        iter_count += 1
    # print('Number of Iterations in Kappa Heuristic:',iter_count)
    return kappa