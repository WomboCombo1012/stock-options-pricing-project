import math
from scipy.stats import norm

def black_scholes(S, K, T, sigma, r, option_type):
    """
     Parameters:
     S : float : current stock price
     K : float : strike price
     T : float : time to maturity (in years)
     r : float : risk-free interest rate (annualized)
     sigma : float : volatility of the underlying stock (annualized)
     option_type : str : 'call' or 'put'

     Returns:
     float : option price
     """
    d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)

    if option_type == 'call':
        price = S * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)
    elif option_type == 'put':
        price = K * math.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    else:
        raise ValueError("option_type must be 'call' or 'put'")

    return price

print(black_scholes(100, 100, 1, .05, .2, 'put'))