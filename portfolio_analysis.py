import pandas as pd
import numpy as np

import logging
import copy

from data_collection import DataImport
from portfolio_aggregation import PortfolioConstructor

class PortfolioAnalysis:
    def __init__(self, portfolio_holdings_pathway: str):
        self._portfolio_holdings = self.import_portfolio_holdings(portfolio_holdings_pathway)
        self._list_of_funds = self.create_list_of_funds()
        self.split_holdings_stock_funds_df()
        
    @property
    def list_of_funds(self):
        return self._list_of_funds

    @property
    def portfolio_holdings(self):
        return self._portfolio_holdings
    
    @property
    def portfolio_fund_holdings_df(self):
        return self._portfolio_fund_holdings_df
    
    @property
    def portfolio_stock_holdings_df(self):
        return self._portfolio_stock_holdings_df
    
    @property 
    def portfolio_fund_holdings_dict(self):
        return self._portfolio_fund_holdings_dict
    
    def create_list_of_funds(self):
        df = copy.deepcopy(self.portfolio_fund_holdings_df)
        df['tuples'] = df.apply(lambda x: (x['ticker'], x['CIK'], x['series']))
        
        return df['tuples'].to_list()
            
    
    
    
    
    
    