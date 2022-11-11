import numpy as np
import pandas as pd
import os

class DataImport:
    def init(self, fund_holdings_file: str):
        self._fund_holdings_file = fund_holdings_file
        self._API_TOKEN = os.environ['SEC-API-TOKEN']
        
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
    
    def CUSIP_to_ticker(self, CUSIP: str) -> str:
        """ looks up the CUSIP string and returns a ticker for the company that issued that security

        Args:
            CUSIP (str): CUSIP of security in fund holdings

        Returns:
            str: ticker of the company that issued that security
        """
    
    