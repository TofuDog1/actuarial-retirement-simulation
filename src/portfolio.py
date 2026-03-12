import numpy
from config import stock_returns, bond_returns, stock_volatility, bond_volatility

stock_sigma = stock_volatility / 100
bond_sigma = bond_volatility / 100

stock_mu = numpy.log(1 + (stock_returns/100)) - (stock_sigma**2)/2
bond_mu = numpy.log(1 + (bond_returns/100)) - (bond_sigma**2)/2

def sample_portfolio_return(stock_share, bond_share):
    stock_log_returns = numpy.random.normal(stock_mu, stock_sigma)
    bond_log_returns = numpy.random.normal(bond_mu, bond_sigma)
    total_returns = (numpy.exp(stock_log_returns) * stock_share + 
                     numpy.exp(bond_log_returns) * bond_share)
    # Log returns instead of simple returns

    return total_returns