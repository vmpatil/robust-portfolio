# Addressing Estimation Errors on Expected Asset Returns through Robust Portfolio Optimization
An associated Github repo for our paper 'Addressing Estimation Errors on Expected Asset Returns through Robust Portfolio Optimization'

Authors:  Gérard Cornuéjols, Özgün Elçi, Vrishabh Patil (vmpatil@andrew.cmu.edu),

**In Submission**

### Abstract ###

It is well known that the classical Markowitz model for portfolio optimization is extremely sensitive to estimation errors on the expected asset returns. Robust optimization mitigates this issue. We focus on ellipsoidal uncertainty sets around a point estimate of the expected asset returns. An important issue is the choice of the parameters that specify this ellipsoid, namely the point estimate and the estimation-error matrix. We show that diagonal estimation-error matrices can in theory achieve an arbitrarily small loss in the expected portfolio return as compared to the optimum. We empirically investigate the sample size needed to compute the point estimate. We also conduct an empirical study of different estimation-error matrices and give a heuristic to choose the size of the uncertainty set. The results of our experiments show that robust portfolio models featuring a family of diagonal estimation-error matrices outperform the classical Markowitz model.

### Data

We conduct our experiments using simulated data modeled on stocks in the U.S. equity market. We use data on the historical returns of stocks in the S&P 500 index as consolidated by  Kocuk and Cornuéjols (2020). The historical stock returns and market capitalization information on stocks in the S&P 500 index were collected from the Wharton Research Database Services and classified into 11 sectors according to the Global Industrial Classification Standard (GICS).  We consider a 30-year period between January 1987 and December 2016. Additionally, we consider the 5-, 10-, 12-, and 17-sector datasets from the Fama-French data library. These datasets include monthly returns, for which we consider a 30-year period between March 1994 and February 2024, and daily returns, for which we consider a 10-year period between March 2014 and February 2024.

Fama-French Data Library: https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html
