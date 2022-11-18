import logging
import os

import numpy as np
import pandas as pd
from sec_api import FormNportApi


class DataImport:
    def init(self, fund_holdings: dict):
        self.fund_holdings = fund_holdings
        self._API_TOKEN = os.environ['SEC_API_TOKEN']
        self._nportApi = FormNportApi(self.API_TOKEN)

    @property
    def API_TOKEN(self):
        return self._API_TOKEN
    
    @property
    def nportApi(self):
        return self._nportApi
    
    
    def import_API_token(self) -> str:
        """ tests if API token exists and returns value if it does """

        token_value = None

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

    def query_10_filings(self, CIK: str, start: int) -> None:
        """ queries API to pull latest fund holdings and saves as a CSV """
        nportApi = FormNportApi(self.API_TOKEN)
        
        response = nportApi.get_data(
            {
                "query": {"query_string": {
                    "query": f"genInfo.regCik:{CIK}"
                    }
                },
                "from": str(start),
                "size": "10",
            }
        )

        return response
    
    def query_holdings(self, CIK: str, series: str) -> dict:
        """ goes through 10 filings at a time until it finds the correct holdings


        Args:
            CIK (str): CIK of filing institution
            series (str): Series corresponding to the specific being held
        """
        
        correct_filing = None
        
        # look through first 50 holdings
        for i in range(5):
            response = self.query_10_filings(CIK, start=i)
            
            for filing in response['filings']:
                if filing['genInfo']['seriesId'] == series:
                    correct_filing = filing
                    break
        
        if correct_filing is None:
            logging.error(f"Unable to locate filing for CIK: {CIK} and Series: {series}")
        else:
            return correct_filing    
    
    def CUSIP_to_ticker(self, CUSIP: str) -> str:
        """ looks up the CUSIP string and returns a ticker for the company that issued that security

        Args:
            CUSIP (str): CUSIP of security in fund holdings

        Returns:
            str: ticker of the company that issued that security
        """