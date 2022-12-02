import numpy as np
import pandas as pd

import logging
from typing import Dict

class PortfolioConstructor:
    def __init__(self, portfolio_holdings_file: str, fund_holdings_folder_name: str):
        self._portfolio_holdings_file = portfolio_holdings_file
        self._fund_holdings_folder_name = fund_holdings_folder_name 

    @property
    def portfolio_fund_holdings(self):
        return self._portfolio_fund_holdings
    
    @property
    def portfolio_stock_holdings_dict(self):
        return self._portfolio_stock_holdings_dict
    
    @property
    def portfolio_stock_holdings_df(self):
        return self._portfolio_stock_holdings_df
        
        
    def import_fund_holdings(self) -> Dict[str, pd.DataFrame]:
        """read in all of the fund holdings into a dictionary
        
        Returns:
            dict: key: fund name, value: DataFrame of holdings
        """
        
        
    def import_portfolio_holdings(pathway: str) -> pd.DataFrame:
        """ returns a DataFrame of the portfolio holdings """
        
        holdings = None
        try:
            holdings = pd.read_csv(pathway, index_col=False)
        except:
            logging.critical(f"Cannot find holdings CSV file using pathway: {pathway}")
        
        return holdings
    
    def split_holdings_stock_funds_df(self):
        """ takes portfolio holdings and breaks them into fund and stock holdings """
        
        stocks = self.portfolio_holdings[self.portfolio_holdings['holding_type'] == 'stock']
        stocks.drop(['CIK', 'series'], axis=1)
        
        funds = self.portfolio_holdings[self.portfolio_holdings['holding_type'] == 'fund']
        funds = funds.drop(['sector','country'], axis=1)
        
        self._portfolio_fund_holdings_df = funds
        self._portfolio_stock_holdings_df = stocks

    def holdings_amt_dict(self, holding_type: str = "stocks") -> dict:
        """ creates dictionary of holdings and the investment amounts """
        
        val = None
        
        if holding_type == "funds":
            val = dict(zip(self.portfolio_fund_holdings_df['holding'], self.portfolio_fund_holdings_df['investment_amt'].astype(float)))
        elif holding_type == "stocks":
            val = dict(zip(self.portfolio_stock_holdings_df['holding'], self.portfolio_stock_holdings_df['investment_amt'].astype(float)))
        else:
            val = dict(zip(self.portfolio_fund_holdings_df['holding'], self.portfolio_fund_holdings_df['investment_amt'].astype(float)))
            logging.error("Invalid holding type request, returning dictionary of stock values as default")
            
        return val
        
    
    def add_investment_amounts(self, fund_holdings: dict, portfolio_fund_holdings: dict) -> dict:
        """adds column in each dataframe for the dollar amount invested in that holding for that fund
    
        Returns:
            dict: dict of holding_name as keys and DataFrames of their holdings as values
        """
    
    
    
    
    
    
    
    
    
    
    def define_combined_fund_portfolio(self, fund_holdings: dict, portfolio_fund_holdings: dict) -> None:
        """Combines portfolio values into one larger portfolio based on ticker
    
        Args:
            fund_holdings (dict, optional): dict of fund names and DataFrames of their holdings. Defaults to self.fund_holdings.
            portfolio_fund_holdings (dict, optional): dict of fund names and how much is invested in each. Defaults to self.portfolio_fund_holdings.
    
        Returns:
            None: sets self._combined_fund_portfolio as the combined amounts of stocks held in portfolio
        """
    
    def define_combined_full_portfolio(self) -> None:
        """Combines fund holdings and individual stock holdings"""
        
    
    