import pandas as pd
import numpy as np

import os
import logging
import copy
from datetime import date

from data_collection import DataImport
from portfolio_aggregation import PortfolioConstructor

class PortfolioAnalysis:
    def __init__(self, portfolio_holdings_pathway: str):
        self._portfolio_holdings = self.import_portfolio_holdings(portfolio_holdings_pathway)
        self.split_holdings_stock_funds_df()
        self._list_of_funds = self.create_list_of_funds()
        self.define_todays_holdings_folder()
        
    @property
    def holdings_folder(self):
        return self._holdings_folder
    
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
    
    @property
    def aggregated_holdings(self):
        return self._aggregated_holdings
    
    def create_list_of_funds(self):
        df = copy.deepcopy(self.portfolio_fund_holdings_df)
        # correcting and left filling CIKs to be 10 digits long
        df['tuples'] = df.apply(lambda x: (x['ticker'], str(int(x['CIK'])).zfill(10), x['series']), axis=1)
        
        return df['tuples'].to_list()
    
    def import_portfolio_holdings(self, pathway: str) -> pd.DataFrame:
        """ returns a DataFrame of the portfolio holdings """

        holdings = None
        try:
            holdings = pd.read_csv(pathway, index_col=False)
            column_dtype_map = {"ticker": str, 
                                "investment_amt": float,
                                "holding_type": str,
                                "sector": str,
                                "country": str,
                                "series": str,
                                }
            holdings = holdings.astype(column_dtype_map)
        except:
            logging.critical(f"Unable to import holdings CSV file using pathway: {pathway}")

        return holdings
    
    def split_holdings_stock_funds_df(self):
        """ takes portfolio holdings and breaks them into fund and stock holdings """

        stocks = self.portfolio_holdings[self.portfolio_holdings['holding_type'] == 'stock']
        stocks.drop(['CIK', 'series'], axis=1)

        funds = self.portfolio_holdings[self.portfolio_holdings['holding_type'] == 'fund']
        funds = funds.drop(['sector','country'], axis=1)

        self._portfolio_fund_holdings_df = funds
        self._portfolio_stock_holdings_df = stocks
    
    def check_holdings_folder(self) -> None:
        try:
            os.mkdir("fund_holdings")
        except:
            pass # already exists so we don't need to create a new one
    
    def define_todays_holdings_folder(self) -> None:
        """ creates a new folder with today's date if it exists or 
        Returns:
            str: file path to today's folder
        """
        todays_date = date.today()
        self.check_holdings_folder()
        try:
            os.mkdir("fund_holdings/" + str(todays_date))
        except:
            pass # already exists so we don't need to create a new one
        
        self._holdings_folder = "fund_holdings/" + str(todays_date)
    
    
    def import_fund_data(self) -> None:
        """ Imports fund holdings using data_collection library """
        print("Beginning import of fund holdings")
        DI = DataImport(self.list_of_funds, self.holdings_folder)
        DI.generate_and_save_holdings()
        print("Finished importing fund holdings")
    
    def aggregate_portfolio(self) -> None:
        PC = PortfolioConstructor(self.portfolio_stock_holdings_df, self.portfolio_fund_holdings_df, self.holdings_folder)
        self._aggregated_holdings = PC.full_portfolio_holdings()
    
    
    
    
    