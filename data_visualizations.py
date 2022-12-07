import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

class DataVisualizations:
    def __init__(self, portfolio_holdings_df: pd.DataFrame, aggregate_holdings_df: pd.DataFrame):
        self._portfolio_holdings_df = portfolio_holdings_df
        self._aggregate_holdings_df = aggregate_holdings_df
        self._aggregate_holdings_df['nation'] = self._aggregate_holdings_df['country'].apply(lambda x: 'Domestic' if x == 'United States' else 'International')
    
    @property
    def aggregate_holdings_df(self):
        return self._aggregate_holdings_df
    
    @property
    def portfolio_holdings_df(self):
        return self._portfolio_holdings_df
    
    def compareTotalCount(self) -> None:
        """ Compare total count by U.S. and other nations """
        sns.countplot(data = self.aggregate_holdings_df, x = 'nation').set(title = 'International')
    
    def compareSumbyNation(self) -> None:
        """ Compare the sum of total investment by nations """
        a = self.aggregate_holdings_df.groupby('nation')['portfolio_holdings'].sum().reset_index()
        a.set_index('nation', inplace = True)
        a.plot(kind = 'bar')
        
    def CompareFiveUS(self) -> None:
        """ Compare the 5 most investment in U.S. """
        
        us5 = self.aggregate_holdings_df[self.aggregate_holdings_df['country'] == 'United States'].sort_values('portfolio_holdings', ascending = False).head()
        
        us5['portfolio_holdings'].plot(kind = 'bar')
        plt.title('5 the most investment in US')

    def compareSectorUS(self) -> None:
        """ comparing by sector in the US """
        
        sns.countplot(data = self.aggregate_holdings_df, x = 'sector').set(title = 'Sectors')
    
    def distribution(self) -> None:
        """ Distribution of Investment Amount """
        
        ax = sns.distplot(self.aggregate_holdings_df['portfolio_holdings'])
        sns.set(font_scale = 1.7)
        
        
    def compareHolding(self) -> None:
        """ Comparing holding types """
        
        sns.catplot(x = 'holding_type', kind = 'count', data = self.portfolio_holdings_df).set(Title = '0 = fund, 1 = stock')
        plt.show()
        
        # pie chart
        categories = self.portfolio_holdings_df['holding_type'].value_counts().keys()
        values = self.portfolio_holdings_df['holding_type'].value_counts().values

        plt.pie(values, labels=categories)

        plt.axis('equal')
        plt.show()
    
    def compareCapsize(self) -> None:
        self.aggregate_holdings_df['cap_size']=""

        self.aggregate_holdings_df["cap_size"] = self.aggregate_holdings_df['market_cap'].apply(self.market_cap_categorization)
        
        sns.countplot(data = self.aggregate_holdings_df, x = 'cap_size').set(title = 'Breakdown by Cap size')
    
    def map_graph(self) -> None:
        invst_sum = self.aggregate_holdings_df.groupby("country")["portfolio_holdings"].sum()

        fig = px.choropleth(self.aggregate_holdings_df, locationmode='country names', locations = invst_sum.keys(), color = invst_sum.values)
        fig.update_layout(coloraxis_colorbar=dict(title="portfolio_holdings"))
        fig.show()
        
    def market_cap_categorization(self, market_cap: float) -> str:
        category = ""
        
        if market_cap >= 10_000_000_000:
            category = 'large'
        elif market_cap >= 2_000_000_000:
            category = 'mid'
        else:
            category = 'small'
        
        return category
