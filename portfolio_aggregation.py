import numpy as np
import pandas as pd

from typing import Dict

class PortfolioConstructor:
    def __init__(self, portfolio_holdings_file: str, fund_holdings_folder_name: str):
        self._portfolio_holdings_file = portfolio_holdings_file
        self._fund_holdings_folder_name = fund_holdings_folder_name 

    def import_portfolio_holdings(self) -> tuple[Dict[str, pd.DataFrame], Dict[str, pd.DataFrame]]:
        """builds dictionaries for the portfolio holdings and the amount held in them
        
        Returns:
            tuple[dict, dict]: dicts with fund/stock names, amounts for funds and stocks
        """        
        
        
    def import_fund_holdings(self) -> Dict[str, pd.DataFrame]:
        """read in all of the fund holdings into a dictionary
        
        Returns:
            dict: key: fund name, value: DataFrame of holdings
        """
        
        
        
        
    
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
        
        
        
##Data Visualization
class Visual:
    df['nation'] = df['country'].apply(lambda x: 'Domestic' if x == 'US' else 'International')
     # Compare total count by U.S. and other nations
    def compareTotalCount():
        sns.countplot(data = df, x = 'nation').set(title = 'International')
        # Compare the sum of total investment by nations
    def compareSumbyNation():
        a = df.groupby('nation')['investment_amt'].sum().reset_index()
        a.set_index('nation', inplace = True)
        a.plot(kind = 'bar')
    # Compare the 5 most investment in U.S.
    def CompareFiveUS():
        us5 = df[df['country'] == 'US'].sort_values('investment_amt', ascending = False).head()
        us5['investment_amt'].plot(kind = 'bar')
        plt.title('5 the most investment in US')

    # also can do this to the world
    # Comapring by sector in US
    def compareSectorUS():
        sns.countplot(data = df, x = 'sector').set(title = 'Sectors')
        # Distribution of Investment Amount
    def distribution():
        ax = sns.distplot(df['investment_amt'])
        sns.set(font_scale = 1.7)
        # Comparing holding types
    def compareHolding():
        sns.catplot(x = 'holding_type', kind = 'count', data = df).set(Title = '0 = fund, 1 = stock')
        plt.show()
        # pie charts()
    def makePie():
        y = np.array([35, 25, 25, 15])
        # if this is the investement amount of four companies
        mylabels = ["Apples", "Bananas", "Cherries", "Dates"]
        myexplode = [0.2, 0, 0, 0]

        # if this is name of companies

        plt.pie(y, labels = mylabels, explode = myexplode)
        plt.show()
