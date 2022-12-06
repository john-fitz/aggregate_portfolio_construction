# aggregate_portfolio_construction

To Run:
1) Import modules for data analysis using:
from portfolio_analysis import PortfolioAnalysis

2) Instantiate portfolio analysis object using: 
PA = PortfolioAnalysis(portfolio_holdings_pathway='example_holdings.csv')

3) Import the fund data and then aggregate holdings:
PA.import_fund_data()
PA.aggregate_portfolio()

4) Add additional information about the individual holdings:
PA.add_additional_information_to_stock_holdings()

5) Save the total holdings information:
PA.save_portfolio_holdings()

We can then pass in this information into our visualizations module and view some outputs:
from data_visualizations import DataVisualizations

You can either re-use the outputs of the portfolio analysis module or read in examples/new ones
- using outputs:
DV = DataVisualizations(PA.portfolio_holdings, PA.aggregated_holdings)

- else reading in new examples:
DV = DataVisualizations(pd.read_csv('example_holdings.csv', index_col=None), pd.read_csv('partial_holdings_for_testing.csv', index_col=None))

And then call methods to create graphs