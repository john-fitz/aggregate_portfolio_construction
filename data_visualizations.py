import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

class DataVisualizations:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.df['nation'] = self.df['country'].apply(lambda x: 'Domestic' if x == 'US' else 'International')
        
    def compareTotalCount(self) -> None:
        """ Compare total count by U.S. and other nations """
        sns.countplot(data = self.df, x = 'nation').set(title = 'International')
    
    def compareSumbyNation(self) -> None:
        """ Compare the sum of total investment by nations """
        a = self.df.groupby('nation')['investment_amt'].sum().reset_index()
        a.set_index('nation', inplace = True)
        a.plot(kind = 'bar')
        
    def CompareFiveUS(self) -> None:
        """ Compare the 5 most investment in U.S. """
        
        us5 = self.df[self.df['country'] == 'US'].sort_values('investment_amt', ascending = False).head()
        us5['investment_amt'].plot(kind = 'bar')
        plt.title('5 the most investment in US')

    def compareSectorUS(self) -> None:
        """ comparing by sector in the US """
        
        sns.countplot(data = self.df, x = 'sector').set(title = 'Sectors')
    
    def distribution(self) -> None:
        """ Distribution of Investment Amount """
        
        ax = sns.distplot(self.df['investment_amt'])
        sns.set(font_scale = 1.7)
        
        
    def compareHolding(self) -> None:
        """ Comparing holding types """
        
        sns.catplot(x = 'holding_type', kind = 'count', data = self.df).set(Title = '0 = fund, 1 = stock')
        plt.show()
        
        # pie chart
        categories = self.df['holding_type'].value_counts().keys()
        values = self.df['holding_type'].value_counts().values

        plt.pie(values, labels=categories)

        plt.axis('equal')
        plt.show()
    
    def compareCapsize(self) -> None:
        df['cap_size']=""

        df.loc[df['investment_amt'] <= 2000, 'cap_size'] = 'small'
        df.loc[(df['investment_amt'] > 2000) & (df['investment_amt'] <= 6000), 'cap_size'] = 'mid'
        df.loc[df['investment_amt'] > 6000, 'cap_size'] = 'large'
        
        sns.countplot(data = df, x = 'cap_size').set(title = 'Breakdown by Cap size')
    
    def map_graph(self) -> None:
        invst_sum = self.df.groupby("country")["investment_amt"].sum()

        fig = px.choropleth(self.df, locationmode='country names', locations = invst_sum.keys(), color = value)
        fig.update_layout(coloraxis_colorbar=dict(title="investment_amount"))
        fig.show()
        
