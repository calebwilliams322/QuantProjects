import numpy as np
from scipy.stats import norm
from scipy.optimize import brentq

def black_scholes_call(S, K, T, r, sigma, q=0.0):
    """
    Calculates the price of a call option using the Black–Scholes formula.

    Parameters:
        S (float): Current price of the underlying asset
        K (float): Option strike price
        T (float): Time to expiry (in years)
        r (float): Risk-free interest rate (annualized)
        sigma (float): Volatility of underlying asset (annualized)
        q (float): Dividend yield (annualized, default 0)

    Returns:
        float: Call option price
    """
    d1 = (np.log(S / K) + (r - q + sigma**2 / 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    call_price = (S * np.exp(-q * T) * norm.cdf(d1)) - (K * np.exp(-r * T) * norm.cdf(d2))

    return call_price


def implied_volatility_call(option_price, S, K, T, r, q=0.0, sigma_bounds=(0.01, 3.0)):
    """
    Computes implied volatility numerically for a call option using Black–Scholes.

    Parameters:
        option_price (float): Observed market price of the option
        S (float): Current price of the underlying asset
        K (float): Option strike price
        T (float): Time to expiry (in years)
        r (float): Risk-free interest rate
        q (float): Dividend yield (default 0)
        sigma_bounds (tuple): Bounds to search for volatility

    Returns:
        float: Implied volatility
    """
    objective_function = lambda sigma: black_scholes_call(S, K, T, r, sigma, q) - option_price
    
    try:
        implied_vol = brentq(objective_function, *sigma_bounds)
    except ValueError:
        implied_vol = np.nan  # In case no solution is found within bounds

    return implied_vol


