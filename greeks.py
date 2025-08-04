import math
from scipy.stats import norm
from binomial_tree import binomial_tree_price
def compute_european_greeks(S, K, T, r, sigma, option_type='call'):
    d1 = (math.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)

    delta = norm.cdf(d1) if option_type == 'call' else norm.cdf(d1) - 1
    gamma = norm.pdf(d1) / (S * sigma * math.sqrt(T))
    vega = S * norm.pdf(d1) * math.sqrt(T) / 100  # per 1% change in volatility
    theta = None
    rho = None

    if option_type == 'call':
        theta = (-S * norm.pdf(d1) * sigma / (2 * math.sqrt(T))
                 - r * K * math.exp(-r * T) * norm.cdf(d2)) / 365
        rho = K * T * math.exp(-r * T) * norm.cdf(d2) / 100
    elif option_type == 'put':
        theta = (-S * norm.pdf(d1) * sigma / (2 * math.sqrt(T))
                 + r * K * math.exp(-r * T) * norm.cdf(-d2)) / 365
        rho = -K * T * math.exp(-r * T) * norm.cdf(-d2) / 100

    return {
        'Delta': delta,
        'Gamma': gamma,
        'Theta': theta,
        'Vega': vega,
        'Rho': rho
    }

def compute_american_greeks(S, K, T, r, sigma, N, option_type, epsilonS, epsilonSigma, epsilonT, epsilonr):
    #Greeks approximated using the standard central difference approximation
    P1 = binomial_tree_price(S + epsilonS, K, T, r, sigma, N, option_type)
    P2 = binomial_tree_price(S - epsilonS, K, T, r, sigma, N, option_type)
    P = binomial_tree_price(S, K, T, r, sigma, N, option_type)

    delta = (P1-P2) / (2 * epsilonS)
    gamma = (P1 - 2*P + P2) / epsilonS ** 2

    P3 = binomial_tree_price(S, K, T - epsilonT, r, sigma, N, option_type)

    theta = (P3 - P) / epsilonT

    P4 = binomial_tree_price(S, K, T, r, sigma + epsilonSigma, N, option_type)
    P5 = binomial_tree_price(S, K, T, r, sigma - epsilonSigma, N, option_type)

    vega = (P4 - P5) / (2 * epsilonSigma)

    P6 = binomial_tree_price(S, K, T, r + epsilonr, sigma, N, option_type)
    P7 = binomial_tree_price(S, K, T, r - epsilonr, sigma, N, option_type)

    rho = (P6 - P7) / (2 * epsilonr)

    return {
        'Delta': delta,
        'Gamma': gamma,
        'Theta (Daily)': theta,
        'Vega': vega,
        'Rho': rho
    }

