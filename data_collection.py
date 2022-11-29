import numpy as np
import pandas as pd

from datetime import date
import logging
import os

from sec_api import FormNportApi
from sec_api import MappingApi


class DataImport:
    def init(self, fund_holdings: dict):
        self.fund_holdings = fund_holdings

    @property
    def API_TOKEN(self):
        token = None
        try: 
            token = os.environ['SEC_API_TOKEN']
        except:
            logging.error("Cannot find API Token in environment variables")
        
        return token

    @property
    def nportAPI(self):
        return FormNportApi(self.API_TOKEN)

    @property
    def mappingAPI(self):
        return MappingApi(self.API_TOKEN)


    def import_API_token(self) -> str:
        """ tests if API token exists and returns value if it does """

        token_value = None

        try:
            token_value = os.environ['SEC_API_TOKEN'] 
        except KeyError:
            logging.error("Unable to find sec-api token in environment variables")
            
        return token_value

    def query_10_filings(self, CIK: str, start: int) -> None:
        """ queries API to pull latest fund holdings and saves as a CSV """
        
        nportAPI = self.nportAPI
        
        response = nportAPI.get_data(
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
    
    def import_holdings_df(self, CIK: str, series: str) -> pd.DataFrame:
        """ locates latest filing and returns holdings as a DataFrame

        Args:
            CIK (str): CIK of filing institution
            series (str): Series corresponding to the specific being held

        Returns:
            pd.DataFrame: DataFrame of holdings information
        """
        data = {'company_name': [], 'CUSIP': [], 'num_holdings': [], 'invested_amt_usd': [], 'percent_of_portfolio': [], 'country': []}

        holdings = self.query_holdings(CIK, series)
        
        if holdings is not None:
            for holding in holdings['invstOrSecs']:
                data['company_name'].append(holding['name'])
                data['CUSIP'].append(holding['cusip'])
                data['num_holdings'].append(holding['balance'])
                data['invested_amt_usd'].append(holding['valUSD'])
                data['percent_of_portfolio'].append(holding['pctVal'])
                data['country'].append(holding['invCountry'])

        return pd.DataFrame.from_dict(data)
    
    def CUSIP_to_ticker(self, CUSIP: str) -> str:
        """ looks up the CUSIP string and returns a ticker for the company that issued that security

        Args:
            CUSIP (str): CUSIP of security in fund holdings

        Returns:
            str: ticker of the company that issued that security
        """
        mappingAPI = self.mappingAPI
        
        try:
            result = mappingAPI.resolve("cusip", CUSIP)[0].ticker
        except:
            result = ""
            logging.error(f"Unable to find ticker symbol for CUSIP: {CUSIP}")
        
        return result

    def generate_and_save_holdings(self, list_of_funds: list, save_folder_pathway: str) -> None:
        """ goes through list of funds, pulls their holdings, and saves holdings as CSV

        Args:
            list_of_funds (list): list of tuples of strings of (CIK, series) per fund
            save_folder_pathway (str): pathway to today's folder to save outputs
        """
        for CIK, series in list_of_funds:
            fund_holdings = self.import_holdings_df(CIK, series)
            fund_holdings['ticker'] = fund_holdings['CUSIP'].apply(lambda x: self.CUSIP_to_ticker(x))
            self.save_fund_holdings(fund_holdings=fund_holdings, CIK=CIK, series=series, save_folder_pathway=save_folder_pathway)

    def save_fund_holdings(self, fund_holdings: pd.DataFrame, CIK: str, series: str, save_folder_pathway: str) -> None:
        """ saves fund holdings in the current folder

        Args:
            fund_holdings (pd.DataFrame): DataFrame of fund holdings pulled from SEC API
            CIK (str): CIK corresponding to the fund's parent co.
            series (str): series corresponding to the fund
            save_folder_pathway (str): folder for the day in which to save information
        """
        todays_date = date.today()
        file_pathway = f"{save_folder_pathway}/{CIK}_{series}_{todays_date}"
        fund_holdings.to_csv(file_pathway)
        
        

