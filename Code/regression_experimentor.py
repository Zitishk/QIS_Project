"""
A module for conducting regression analysis experiments and portfolio performance evaluation.

This module contains two main classes:
- regression: Handles individual regression analysis and portfolio construction
- experimentor: Manages multiple regression combinations and result aggregation

The module is designed for financial analysis, particularly for:
- Cross-sectional regression analysis
- Portfolio formation based on regression results
- Performance evaluation using various metrics including Carhart model
"""
import numpy as np
import pandas as pd
import statsmodels.api as sm
from tqdm import tqdm
from tabulate import tabulate
import statsmodels.formula.api as smf
from typing import List, Tuple, Dict
import gc
import subprocess
import sys

try:
    from linearmodels.panel import PanelOLS
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "linearmodels"])
    import linearmodels
    from linearmodels.panel import PanelOLS


class regression():
    """
    A class for performing regression analysis and portfolio construction.

    Attributes:
        data (pd.DataFrame): Input data with financial variables
        var (list): List of independent variables for regression
        yvar (str): Dependent variable name
        train_freq (str): Training frequency ('6m' or '12m')
        turnover (str): Portfolio rebalancing frequency
        ff (pd.DataFrame): Fama-French factors data
        coeffs (pd.DataFrame): Regression coefficients
        coefs (pd.DataFrame): Processed coefficient statistics
        sig_vars (list): Significant variables based on t-statistics
        ports (dict): Portfolio returns
        performance (dict): Performance metrics
        carhart (dict): Carhart model results
    """

    def __init__(self,combinations,ff):
        """
        Initialize regression analysis with given combinations and factors.

        Args:
            combinations (dict): Configuration dictionary containing data and parameters
            ff (pd.DataFrame): Fama-French factors data
        """
        self.data = combinations['data'].drop_duplicates(subset=['yyyymm','permno']).dropna(subset=[combinations['yvar']])
        self.var = combinations['vars']
        self.yvar = combinations['yvar']
        self.train_freq = combinations['train_freq']
        self.turnover  = combinations['turnover']
        self.ff = ff
        self.coeffs = pd.DataFrame()
        self.coefs = pd.DataFrame()
        self.sig_vars = None
        self.ports = {}
        self.performance = {}
        self.carhart = {}

    def eqw_mean(self, x: pd.Series) -> float:
        """
        Calculate equal-weighted returns mean with log transformation.

        Args:
            x (pd.Series): Series of returns in percentage

        Returns:
            float: Equal-weighted mean return
        """
        if len(x) == 0 or x.isna().all():return np.nan  # Added check for empty/all-NA series
        return np.log(np.nanmean(np.exp(x/100) - 1) + 1) * 100

    def crossreg(self,df: pd.DataFrame):
        """
        Perform Fama-MacBeth cross-sectional regression analysis.

        Args:
            df (pd.DataFrame): Input data for regression

        Updates:
            self.coeffs with regression results
        """
        if len(df) == 0:return  # Added check for empty DataFrame
        df.dropna(subset=[self.yvar] + self.var.to_list(),inplace=True)
        coefs = {}
        for i in sorted(df.yyyymm.unique()):
            X = df[df.yyyymm == i]
            try:
                model = PanelOLS(X[self.yvar], sm.add_constant(X[self.var]), entity_effects=False,time_effects=False,other_effects=X['ind'],drop_absorbed=True).fit()
                #model = sm.OLS(X[self.yvar], sm.add_constant(X[self.var])).fit()
                p = model.params
                p.loc['Rsq'] = model.rsquared
                coefs[i] = p
            except Exception as e:
              #print(f'Regression failed for',e)
              continue
        #self.coeffs = pd.DataFrame(coefs)
        self.coeffs = pd.concat(coefs, axis=1)
        #print(self.coeffs)
        return

    def coefsm(self):
        """
        Calculate coefficient statistics including factor premia and t-statistics.

        Updates:
            self.coefs with statistical measures
        """
        if self.coeffs.empty:return  # Added check for empty coeffs
        n = self.coeffs.shape[1]
        self.coefs['f_premia'] = self.coeffs.mean(axis=1)
        self.coefs['f_std'] = self.coeffs.std(axis=1)
        self.coefs['tstat'] = np.sqrt(n) * self.coefs['f_premia'] / self.coefs['f_std']
        return

    def scor_rank(self,df: pd.DataFrame):
        """
        Calculate composite scores and decile rankings for portfolio formation.

        Args:
            df (pd.DataFrame): Input data for scoring

        Returns:
            pd.DataFrame: Data with added score and rank columns
        """
        df['score'] = sum(df[i] * self.coefs.loc[i, 'tstat'] for i in self.sig_vars)
        if(self.turnover == 'year'):
            jan_mask = df.month == 1
            jan_rankings = df.loc[jan_mask,['year','permno','score']].copy()
            jan_rankings['rank'] = jan_rankings.groupby('year')['score'].transform(
                lambda x: pd.qcut(x.rank(method='first'), 10, labels=False))
            jan_rankings.drop('score',axis=1,inplace=True)
            df = pd.merge(df,jan_rankings,on=['year','permno'],how='left',validate='many_to_one')
        else:
            df['rank'] = df.groupby('yyyymm')['score'].transform(
            lambda x: pd.qcut(x.rank(method='first'), 10, labels=False))
        return df

    def portfolio(self,df: pd.DataFrame):
        """
        Construct long-short portfolio returns from decile rankings.

        Args:
            df (pd.DataFrame): Data with rankings

        Returns:
            pd.DataFrame: Long-short portfolio returns
        """
        df = df.loc[df['rank'].isin([0, 9])].copy()
        df.loc[df['rank'] == 9, 'longRet']  = df.loc[df['rank'] == 9, '1m.lret']
        df.loc[df['rank'] == 0, 'shortRet'] = df.loc[df['rank'] == 0, '1m.lret']
        portfolio = df.groupby('yyyymm')[['longRet', 'shortRet']].agg(self.eqw_mean)
        portfolio['LongShort'] = portfolio['longRet'] - portfolio['shortRet']
        return portfolio

    def performance_metrics(self):
        """
        Calculate portfolio performance metrics including returns and Sharpe ratios.

        Updates:
            self.performance with calculated metrics
        """
        for t,port in self.ports.items():
            ports_e = 100 * (np.exp(port / 100) - 1)
            perf = pd.DataFrame()
            perf['mean_returns'] = ports_e.mean()
            perf['std_dev'] = ports_e.std()
            perf['sharpe_ratio'] = perf['mean_returns'] / perf['std_dev']
            self.performance[t] = perf.T

    def carhart_metrics(self):
        """
        Calculate Carhart four-factor model metrics for portfolio returns.

        Updates:
            self.carhart with model results
        """
        ff = self.ff
        for t,port in self.ports.items():
            port['date'] =  pd.to_datetime(port.index,format='%Y%m')
            port = port.merge(ff, on='date', how='left')
            model = smf.ols(formula='LongShort ~ mkt_rf + SMB + HML + Mom', data=port).fit()
            self.carhart[t] = model

    def run(self):
        """
        Execute complete regression analysis pipeline.
        
        This method orchestrates the entire analysis process:
        1. Splits data into train and test sets
        2. Performs regression analysis
        3. Constructs portfolios
        4. Calculates performance metrics
        """
        df = self.data
        df['date'] = pd.to_datetime(df['yyyymm'],format='%Y%m')
        train = df.loc[df.s == 0].copy()
        train = train.set_index(['date','permno'])
        test  = df.loc[df.s == 1].copy()
        test = test.set_index(['date','permno'])
        del df, self.data
        gc.collect()
        if self.train_freq == '6m':
            train = train.loc[train['month'].isin([1, 7])]
        elif self.train_freq == '12m':
            train = train.loc[train['month'] == 1]
        self.calls(train,test)
        return

    def calls(self,train,test):
        """
        Execute sequence of analysis steps on train and test data.

        Args:
            train (pd.DataFrame): Training dataset
            test (pd.DataFrame): Testing dataset
        """
        self.crossreg(train)
        train = train.reset_index()
        test = test.reset_index()
        self.coefsm()
        coefs = self.coefs
        del self.coeffs
        gc.collect()
        self.sig_vars = [v for v in coefs[abs(coefs.tstat) > 1.5].index
                      if v not in ['const', 'Rsq']]

        train = self.scor_rank(train)
        test  = self.scor_rank(test)

        self.ports['train'] = self.portfolio(train)
        self.ports['test']  = self.portfolio(test)

        del train, test
        gc.collect()

        self.performance_metrics()
        self.carhart_metrics()

        del self.ports
        gc.collect()

        return
        
class experimentor():
    """
    A class for running multiple regression experiments and aggregating results.
    """
    
    def __init__(self):
        """Initialize experimentor instance."""
        print('initialized')

    def run_combinations(self,combinations,ff):
        """
        Run regression analysis for multiple parameter combinations.

        Args:
            combinations (list): List of parameter combinations to test
            ff (pd.DataFrame): Fama-French factors data

        Returns:
            pd.DataFrame: Summary results for all combinations
        """
        results = []
        for combo in combinations:
            R = regression(combo,ff)
            R.run()
            result = {
            'significant_vars': len(R.sig_vars),
            'train_m_L': R.performance['train'].loc['mean_returns','longRet'],
            'train_m_S': R.performance['train'].loc['mean_returns','shortRet'],
            'train_m_LS': R.performance['train'].loc['mean_returns','LongShort'],
            'valid_m_L': R.performance['test'].loc['mean_returns','longRet'],
            'valid_m_S': R.performance['test'].loc['mean_returns','shortRet'],
            'valid_m_LS': R.performance['test'].loc['mean_returns','LongShort'],
            'train_s_L': R.performance['train'].loc['sharpe_ratio','longRet'],
            'train_s_S': R.performance['train'].loc['sharpe_ratio','shortRet'],
            'train_s_LS': R.performance['train'].loc['sharpe_ratio','LongShort'],
            'valid_s_L': R.performance['test'].loc['sharpe_ratio','longRet'],
            'valid_s_S': R.performance['test'].loc['sharpe_ratio','shortRet'],
            'valid_s_LS': R.performance['test'].loc['sharpe_ratio','LongShort'],
            'train_rsq': R.carhart['train'].rsquared,
            'valid_rsq': R.carhart['test'].rsquared,
            'train_alpha': R.carhart['train'].params['Intercept'],
            'valid_alpha': R.carhart['test'].params['Intercept'],
            'train_pval': R.carhart['train'].pvalues['Intercept'],
            'valid_pval': R.carhart['test'].pvalues['Intercept']
            }
            results.append({'name': combo['name'],**result})
            del R
            gc.collect()
        return pd.DataFrame(results).round(4)

    def printres(self,results):
        """
        Print results in a formatted table.

        Args:
            results (pd.DataFrame): Results to display
        """
        print(tabulate(results, headers='keys', tablefmt='fancy_grid'))