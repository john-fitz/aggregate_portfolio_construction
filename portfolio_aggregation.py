import numpy as np
import pandas as pd

import logging
import os
from typing import Dict
import glob


class PortfolioConstructor:
    def __init__(self, portfolio_stock_holdings_df: pd.DataFrame, portfolio_fund_holdings_df: pd.DataFrame, fund_holdings_pathway: str):
        self._portfolio_stock_holdings_df = portfolio_stock_holdings_df
        self._portfolio_fund_holdings_df = portfolio_fund_holdings_df
        self._fund_holdings_pathway = fund_holdings_pathway
        
        self.import_fund_holdings()
        self.define_combined_fund_portfolio(self.portfolio_fund_holdings_df, self.fund_holdings_dict)
        self.define_combined_full_portfolio()

    @property
    def fund_holdings_dict(self):
        return self._fund_holdings_dict

    @property
    def stock_holdings(self):
        return self._stock_holdings
    
    @property
    def portfolio_total_holdings(self):
        return self._portfolio_total_holdings

    @property
    def fund_holdings_pathway(self):
        return self.__fund_holdings_pathway

    def import_fund_holdings(self) -> Dict[str, pd.DataFrame]:
        """read in all of the fund holdings from the folder into a dictionary

        Returns:
            dict: key: fund name, value: DataFrame of holdings
        """
        all_files = glob.glob(os.path.join(self._fund_holdings_folder_name + '/', "*.csv"))
        fund_holdings = {}

        for filename in all_files:
            fund_name = filename
            fund_name = fund_name.removeprefix(self._fund_holdings_folder_name + '/')
            fund_name = fund_name.removesuffix('_holdings.csv')
            try: 
                df = pd.read_csv(filename, index_col=None, header=0)
                
                # remap column types
                column_dtype_map = {"ticker": str, 
                                    "name": str,
                                    "weight": float,
                                    "country": str,
                                    "sector": str,
                                    }
                
                df = df.astype(column_dtype_map)
                fund_holdings[fund_name] = df
                
            except:
                logging.warning(f"Unable to import holdings for {fund_name} located in {filename}")
        
        self._fund_holdings_dict = fund_holdings

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
        dict = {}
        fund_holdings_dict = self.holdings_amt_dict(holding_type='funds')
        
        for key in fund_holdings_dict.keys():
            self._portfolio_fund_holdings_df[key] = fund_holdings_dict[key]['investment_amt']
            dict[key] = portfolio_funds[key]['investment_amt']

        for key in fund_holdings.keys():
            self._fund_holdings[key] = fund_holdings[key]

        return dict


    def define_combined_fund_portfolio(self, fund_holdings: dict, portfolio_fund_holdings: dict) -> None:
        """Combines portfolio values into one larger portfolio based on ticker

        Args:
            fund_holdings (dict, optional): dict of fund names and DataFrames of their holdings. Defaults to self.fund_holdings.
            portfolio_fund_holdings (dict, optional): dict of fund names and how much is invested in each. Defaults to self.portfolio_fund_holdings.

        Returns:
            None: sets self._combined_fund_portfolio as the combined amounts of stocks held in portfolio
        """

        funds_with_investment_amounts = self.add_investment_amounts(fund_holdings, portfolio_fund_holdings)
        df = pd.concat(funds_with_investment_amounts.values(), axis=0, join="inner")
        df = df.drop(['weight'], axis=1)
        aggregation_functions = {'name': 'first', 'country': 'first', 'sector': 'first', 'portfolio_holdings': 'sum'}
        df_new = df.groupby(df['ticker'], as_index=False).aggregate(aggregation_functions)

        self._combined_fund_portfolio = df_new



    def define_combined_full_portfolio(self) -> None:
        """Combines fund holdings and individual stock holdings"""
        
        fund_holdings = copy.deepcopy(self.combined_fund_portfolio)
        stock_holdings = self.portfolio_stock_holdings_df
        
        # rename column headings to be able to concatenate the DataFrames
        stock_holdings = stock_holdings.rename(columns={"holding": "ticker", "investment_amt": "portfolio_holdings"})
        # concat the DataFrames and sum holdings. Adds new ones from stock_holdings but sums ones that already exist
        df = pd.concat([fund_holdings, stock_holdings]).groupby(["ticker"], as_index=False)["portfolio_holdings"].sum()
        
        self._full_portfolio_holdings = df