import numpy as np
import pandas as pd
import os
import logging

from sec_api import FormNportApi
from sec_api import MappingApi

class DataImport:
    def __init__(self, fund_holdings_file: str):
        self._fund_holdings_file = fund_holdings_file
        self._API_TOKEN = self.import_API_token()
        self._nportApi = FormNportApi(self._API_TOKEN)
        
    @property
    def nportApi(self):
        return self._nportApi

    def import_API_token(self) -> str:
        """ tests if API token exists and returns value if it does """
        
        token_value = ""

        try:
            token_value = os.environ['SEC_API_TOKEN']
        except KeyError:
            logging.error("Unable to find sec-api token in environment variables")

        return token_value

    def individual_fund_holdings_folder(self, CIK: str) -> str:
        """ creates folder for fund holdings if it doesn't exist or returns folder name if it does

        Args:
            CIK (str): fund CIK number used for SEC filings

        Returns:
            str: pathway to folder for holdings
        """

    def import_fund_holdings_csv_to_dict(self) -> None:
        """ converts CSV of fund holdings to a dictionary """

    def pull_and_save_fund_holdings(self, CIK: str) -> None:
        """ queries API to pull latest fund holdings and saves as a CSV """

        nportApi = FormNportApi("INPUT API TOKEN HERE")

        response = nportApi.get_data(

    def convert_holdings_list_to_df(self, holdings: list) -> pd.DataFrame:
        """ takes in a list of holdings from sec-api and converts it to a DataFrame

        Args:
            holdings (str): list of holdings output from the sec-api

        Returns:
            pd.DataFrame: holdings information with CUSIP, holding percentage
        """
        
        data = {'name': [], 'CUSIP': [], 'holding_amt': [], 'pct_holdings': []}
        
        for holding in holdings:
            data['name'].append(holding['name'])
            data['CUSIP'].append(holding['cusip'])
            data['holding_amt'].append(holding['balance'])
            data['pct_holdings'].append(holding['pctVal'])
        
        return pd.DataFrame.from_dict(data)

    
    def CUSIP_to_ticker(self, CUSIP: str) -> str:
        """ looks up the CUSIP string and returns a ticker for the company that issued that security

        Args:
            CUSIP (str): CUSIP of security in fund holdings

        Returns:
            str: ticker of the company that issued that security
        """
        mappingApi = MappingApi(api_key = self._API_TOKEN)
        result = mappingApi.resolve("cusip", CUSIP)
        return result[0]['ticker']
