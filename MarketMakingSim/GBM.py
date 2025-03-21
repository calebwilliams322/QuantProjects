import numpy as np

class GBMSimulator:
    def __init__(self, S0, mu, sigma, dt=1.0):
        """
        Initialize the GBM model.
        
        Parameters:
        - S0: Initial price
        - mu: Drift (expected return)
        - sigma: Volatility
        - dt: Time step size (e.g., 1.0 for one time unit)
        """
        self.S = S0
        self.mu = mu
        self.sigma = sigma
        self.dt = dt
        self.history = [S0]

    def step(self):
        """
        Simulate one time step of GBM.
        """
        Z = np.random.normal()
        drift = (self.mu - 0.5 * self.sigma ** 2) * self.dt
        diffusion = self.sigma * np.sqrt(self.dt) * Z
        self.S = self.S * np.exp(drift + diffusion)
        self.history.append(self.S)
        return self.S

    def get_price(self):
        """
        Get the current price.
        """
        return self.S

    def get_history(self):
        """
        Get the full price history.
        """
        return self.history
