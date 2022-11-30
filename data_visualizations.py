import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

class DataVisualizations:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.df['nation'] = self.df['country'].apply(lambda x: 'Domestic' if x == 'US' else 'International')
        
     # Compare total count by U.S. and other nations
    def compareTotalCount(self) -> None:
        sns.countplot(data = self.df, x = 'nation').set(title = 'International')
    
    def compareSumbyNation(self):
        """ Compare the sum of total investment by nations """
        a = self.df.groupby('nation')['investment_amt'].sum().reset_index()
        a.set_index('nation', inplace = True)
        a.plot(kind = 'bar')
        
    
    def CompareFiveUS(self):
        """ Compare the 5 most investment in U.S. """
        us5 = self.df[self.df['country'] == 'US'].sort_values('investment_amt', ascending = False).head()
        us5['investment_amt'].plot(kind = 'bar')
        plt.title('5 the most investment in US')

    def compareSectorUS(self):
        """ comparing by sector in the US """
        sns.countplot(data = self.df, x = 'sector').set(title = 'Sectors')
    
    def distribution(self):
        """ Distribution of Investment Amount """
        ax = sns.distplot(self.df['investment_amt'])
        sns.set(font_scale = 1.7)
        
        
    def compareHolding(self):
        """ Comparing holding types """
        sns.catplot(x = 'holding_type', kind = 'count', data = self.df).set(Title = '0 = fund, 1 = stock')
        plt.show()
        
    def makePie(self):
        """ Pie Charts """
        y = np.array([35, 25, 25, 15])
        
        # if this is the investement amount of four companies
        mylabels = ["Apples", "Bananas", "Cherries", "Dates"]
        myexplode = [0.2, 0, 0, 0]

        # if this is name of companies

        plt.pie(y, labels = mylabels, explode = myexplode)
        plt.show()
