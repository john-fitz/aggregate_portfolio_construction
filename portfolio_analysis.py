import pandas as pd
import numpy as np

import os
import logging
import copy
from datetime import date
import time

from data_collection import DataImport
from portfolio_aggregation import PortfolioConstructor

import yfinance as yf

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
        """ aggregates all holdings into self.aggregaed_holdings """
        print("Starting to aggregate holdings")
        PC = PortfolioConstructor(self.portfolio_stock_holdings_df, self.portfolio_fund_holdings_df, self.holdings_folder)
        self._aggregated_holdings = PC.full_portfolio_holdings
        print("Finished aggregating holdings")
    
    def add_additional_information_to_stock_holdings(self) -> None:
        """ Uses the Yahoo Finance API to pull in additional information about the holdings """
        counter = 0
        full_stock_info = {'ticker': [], 'portfolio_holdings': [], 'country': [], 'sector': [], 'industry': [], "market_cap": []}
        for ticker, portfolio_holdings in zip(self.aggregated_holdings['ticker'], self.aggregated_holdings['portfolio_holdings']):
            addition_info = self.query_YF_API(ticker)
            full_stock_info['ticker'].append(ticker)
            full_stock_info['portfolio_holdings'].append(portfolio_holdings)
            full_stock_info['country'].append(addition_info[0])
            full_stock_info['sector'].append(addition_info[1])
            full_stock_info['industry'].append(addition_info[2])
            full_stock_info['market_cap'].append(addition_info[3])
            counter += 1
            print(f"gathering information on stock {counter}")
            if counter % 20 == 0:
                self._aggregated_holdings = pd.DataFrame.from_dict(full_stock_info)
                self.save_portfolio_holdings()
        self._aggregated_holdings = pd.DataFrame.from_dict(full_stock_info)
        
    def query_YF_API(self, ticker: str) -> tuple:
        """ query Yahoo Finance API to pull additional information on stock"""
        ans = (np.nan, np.nan, np.nan, np.nan)
        
        start_time = time.time()
        while time.time() - start_time <= 10: # timeout after 10 seconds of trying
            info = yf.Ticker(ticker).info
            if info['regularMarketPrice'] is not None:
                try:
                    country = info['country']
                    sector = info['sector']
                    industry = info['industry']
                    marketCap = info['marketCap']
                    ans = (country, sector, industry, marketCap)
                except:
                    pass
        if info['regularMarketPrice'] is None:
            logging.warning(f"Unable to find information on {ticker} on Yahoo Finance")
        elif ans[0] is None:
            logging.warning(f"Yahoo Finance query timed out after 10 seconds. Unable to pull information on {ticker}")
        
        return ans
    
    def save_portfolio_holdings(self, save_pathway: str="full_portfolio_holdings.csv") -> None:
        """ save portfolio_holdings """
        
        self.aggregated_holdings.to_csv(save_pathway, index=False)