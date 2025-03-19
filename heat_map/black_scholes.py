import math
import numpy as np
from scipy.stats import norm

N = norm(0, 1)

def black_scholes_prices(
    s: float, 
    k: float, 
    r: float, 
    q: float, 
    v: float, 
    t: float
) -> tuple[float, float]:
    """
    Calculate the Black-Scholes call and put option prices.

    Parameters:
    -----------
    s : float
        Underlying price
    k : float
        Strike price
    r : float
        Continuous risk-free rate
    q : float
        Continuous dividend yield
    v : float
        Volatility (annualized)
    t : float
        Time to expiry (in years)

    Returns:
    --------
    (call, put) : tuple of floats
        Call and put option prices under Black-Scholes.
    """
    d1_val = (np.log(s / k) + (r - q + 0.5 * v**2) * t) / (v * np.sqrt(t))
    d2_val = d1_val - v * np.sqrt(t)

    call = (s * np.exp(-q * t) * N.cdf(d1_val)) - (k * np.exp(-r * t) * N.cdf(d2_val))
    put  = (k * np.exp(-r * t) * N.cdf(-d2_val)) - (s * np.exp(-q * t) * N.cdf(-d1_val))

    return call, put

if __name__ == "__main__":
    # Example usage:
    s_input = 100.0   # Underlying price
    k_input = 100.0   # Strike
    r_input = 0.05    # Risk-free rate
    q_input = 0.00    # Dividend yield
    v_input = 0.20    # Volatility
    t_input = 1.0     # Time to maturity (1 year)

    call_price, put_price = black_scholes_prices(s_input, k_input, r_input, q_input, v_input, t_input)

    print(f"Call Price: {call_price:.4f}")
    print(f"Put Price:  {put_price:.4f}")