import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import streamlit as st


class MarketMakerVisualizer:
    def __init__(self, gbm_prices, total_pnl):
        self.gbm_prices = gbm_prices
        # self.realized_pnl = realized_pnl
        # self.unrealized_pnl = unrealized_pnl
        self.total_pnl = total_pnl
        self.steps = len(gbm_prices)

        # Define figure and axis
        self.fig, self.axs = plt.subplots(2, 1, figsize=(10, 8), gridspec_kw={'hspace': 0.4})

        # Plot GBM price in the first subplot
        self.price_line, = self.axs[0].plot([], [], color='orange', lw=2, label='GBM Price')
        self.axs[0].set_title("GBM Underlying Price Over Time", fontsize=14, fontweight='bold')
        self.axs[0].set_xlabel("Time Step", fontsize=12)
        self.axs[0].set_ylabel("Price", fontsize=12)
        self.axs[0].grid(True, linestyle='--', alpha=0.6)
        self.axs[0].legend(fontsize=10)

        # Plot Market Maker PnL in the second subplot
        # self.realized_line, = self.axs[1].plot([], [], 'g', lw=2, label='Realized PnL')
        # self.unrealized_line, = self.axs[1].plot([], [], 'r', lw=2, label='Unrealized PnL')
        self.total_line, = self.axs[1].plot([], [], 'b', lw=2, label='Total PnL')
        self.axs[1].set_title("Market Maker PnL Over Time", fontsize=14, fontweight='bold')
        self.axs[1].set_xlabel("Time Step", fontsize=12)
        self.axs[1].set_ylabel("PnL", fontsize=12)
        self.axs[1].grid(True, linestyle='--', alpha=0.6)
        self.axs[1].legend(fontsize=10)

        # Define animation
        self.ani = animation.FuncAnimation(self.fig, self.update, frames=self.steps, interval=100, repeat=False)

    def update(self, i):
        self.price_line.set_data(range(i + 1), self.gbm_prices[:i + 1])
        
        # self.realized_line.set_data(range(i + 1), self.realized_pnl[:i + 1])
        # self.unrealized_line.set_data(range(i + 1), self.unrealized_pnl[:i + 1])
        self.total_line.set_data(range(i + 1), self.total_pnl[:i + 1])

        # Adjust axis limits dynamically
        self.axs[0].relim()
        self.axs[0].autoscale_view()
        self.axs[1].relim()
        self.axs[1].autoscale_view()

        return self.price_line, self.total_line
    
    def save_animation(self, filename="animation.mp4"):
        """Save animation to a file"""
        self.ani.save(filename, writer="ffmpeg")

    def save_animation2(self, filename="animation.gif"):
        """Save animation to a file"""
        self.ani.save(filename, writer="pillow", fps=100) 

    def show(self):
        plt.show()
