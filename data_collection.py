import numpy as np
import pandas as pd
import os
import logging

from sec_api import FormNportApi
from sec_api import MappingApi

class DataImport:
    def init(self, fund_holdings_file: str):
        self._fund_holdings_file = fund_holdings_file
        self._API_TOKEN = os.environ['SEC_API_TOKEN']

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
            {
                "query": {"query_string": {
                    "query": f"genInfo.regCik:{CIK}"
                    }
                },
            }
        )



    def CUSIP_to_ticker(self, cusip: str) -> str:
        """ looks up the CUSIP string and returns a ticker for the company that issued that security

        Args:
            CUSIP (str): CUSIP of security in fund holdings

        Returns:
            str: ticker of the company that issued that security
        """
        mappingApi = MappingApi(api_key = self._API_TOKEN)
        result = mappingApi.resolve("cusip", CUSIP)
        return result[0]['ticker']
