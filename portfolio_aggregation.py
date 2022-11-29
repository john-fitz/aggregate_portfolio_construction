import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

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
        
        fund_holdings = fund_holdings.merge(portfolio_fund_holdings, left_on = 'name', right_on = 'holding')
        fund_holding.drop(columns = ['holding_type', 'country', 'sector'], axis = 0)
        self._portfolio_fund_holdings = dict(zip(fund_holding['holding'], fund_holding['investment_amt'].astype(float)))
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
df = pd.read_csv('holdings.csv')
df['nation'] = df['country'].apply(lambda x: 'Domestic' if x == 'US' else 'International')

# Compare total count by U.S. and other nations
sns.countplot(data = df, x = 'nation').set(title = 'International')

# Compare the sum of total investment by nations
a = df.groupby('nation')['investment_amt'].sum().reset_index()
a.set_index('nation', inplace = True)
a.plot(kind = 'bar')

# Compare the 5 most investment in U.S.
us5 = df[df['country'] == 'US'].sort_values('investment_amt', ascending = False).head()
us5['investment_amt'].plot(kind = 'bar')
plt.title('5 the most investment in US')

# Compare the 5 most investment in the world
world5 = df.sort_values('investment_amt', ascending = False).head()
world5['investment_amt'].plot(kind = 'bar')
plt.title('5 the most investment in the world')

# Comapring by sector in US
sns.countplot(data = df, x = 'sector').set(title = 'Sectors')

# Distribution of Investment Amount
ax = sns.distplot(df['investment_amt'])
sns.set(font_scale = 1.7)

# Compare holding types
sns.catplot(x = 'holding_type', kind = 'count', data = df).set(Title = '0 = fund, 1 = stock')
plt.show()

# pie charts()
y = np.array([35, 25, 25, 15])
# if this is the investement amount of four companies
mylabels = ["Apples", "Bananas", "Cherries", "Dates"]
myexplode = [0.2, 0, 0, 0]
# if this is name of companies
plt.pie(y, labels = mylabels, explode = myexplode)
plt.show() 
