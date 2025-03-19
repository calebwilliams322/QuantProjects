import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from black_scholes import black_scholes_prices  # Your pricing function
from db_utils import (
    init_db,
    insert_black_scholes_input,
    insert_black_scholes_output,
    get_all_inputs
)

def compute_heatmap_data(s_range, v_range, k, r, q, t, purchase_call=None, purchase_put=None):
    """
    Computes call and put values over grids of underlying prices and volatilities.
    If purchase prices are provided, returns PnL (BS price minus purchase price).
    Otherwise, returns the raw Black-Scholes prices.
    """
    call_values = np.zeros((len(s_range), len(v_range)))
    put_values = np.zeros((len(s_range), len(v_range)))
    
    for i, s in enumerate(s_range):
        for j, v in enumerate(v_range):
            call, put = black_scholes_prices(s, k, r, q, v, t)
            if purchase_call is not None:
                call_values[i, j] = call - purchase_call
            else:
                call_values[i, j] = call
            if purchase_put is not None:
                put_values[i, j] = put - purchase_put
            else:
                put_values[i, j] = put
    return call_values, put_values

def plot_heatmap(data, x_range, y_range, title, cmap='RdYlGn'):
    """
    Plots a heatmap with larger fonts for titles and labels,
    with a mid-grey background and a slightly larger size.
    
    Parameters:
    -----------
    data : 2D array
        The option prices or PnL values.
    x_range : np.array
        Array for the x-axis values (volatility).
    y_range : np.array
        Array for the y-axis values (underlying price).
    title : str
        Title of the heatmap.
    cmap : str
        Colormap for the heatmap.
    
    Returns:
    --------
    fig : matplotlib Figure
        The heatmap figure.
    """
    # Increase the figure size (adjust as needed)
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Set both the figure and axis backgrounds to a mid-grey color
    fig.patch.set_facecolor('#4C4C4C')
    ax.set_facecolor('#4C4C4C')
    
    # Plot the heatmap data
    c = ax.imshow(
        data,
        extent=[x_range[0], x_range[-1], y_range[0], y_range[-1]],
        origin='lower',
        aspect='auto',
        cmap=cmap
    )
    
    # Set titles and labels with increased font size and white color for contrast
    ax.set_title(title, fontsize=16, color='white')
    ax.set_xlabel("Volatility (σ)", fontsize=14, color='white')
    ax.set_ylabel("Underlying Price (S)", fontsize=14, color='white')
    ax.tick_params(axis='both', which='major', labelsize=12, colors='white')
    
    # Add a colorbar and change its tick labels to white
    cbar = fig.colorbar(c, ax=ax)
    cbar.ax.tick_params(labelcolor='white')
    
    return fig


def main():
    st.title("Black-Scholes Price Sensitivity")

    # init_db()

    with st.expander("How to Use This Webpage"):
        st.markdown("""
    **Directions:**

    1. **Fixed Parameters:**  
       - Set the base underlying price, strike price, risk-free rate, dividend yield, time to expiry, and base volatility in the sidebar.
       - The sidebar will immediately compute and display the base call and put prices.

    2. **Sensitivity Grid Ranges:**  
       - Adjust the minimum and maximum underlying prices and volatilities along with the number of steps to define your grid.

    3. **Option Price Heatmaps:**  
       - The top row displays the original Black-Scholes option prices using a 'hot' color scheme.
       
    4. **PnL Heatmaps:**  
       - Check the "Compute PnL (use purchase prices)" option in the sidebar to reveal inputs for purchase prices.
       - Once entered, the PnL heatmaps (showing the difference between the market price and the Black-Scholes price) will display below the original heatmaps.
       
    5. **Interactivity:**  
       - Modify any of the inputs to see real-time updates to the heatmaps.
       
    Enjoy exploring the sensitivity analysis!
    """)

    
    # ----- FIXED PARAMETERS (Sidebar) -----
    st.sidebar.header("Fixed Parameters")
    base_s = st.sidebar.number_input("Base Underlying Price (S)", value=100.0)
    k = st.sidebar.number_input("Strike Price (K)", value=100.0)
    r = st.sidebar.number_input("Risk-Free Rate (r)", value=0.05, step=0.01)
    q = st.sidebar.number_input("Dividend Yield (q)", value=0.0, step=0.01)
    t = st.sidebar.number_input("Time to Expiry (years)", value=1.0, step=0.1)
    
    # Base Volatility input for the base price calculation
    base_vol = st.sidebar.number_input("Base Volatility (σ)", value=0.20, step=0.01)
    
    # Calculate and display base option prices in the sidebar
    from black_scholes import black_scholes_prices  # ensure your function is imported
    base_call, base_put = black_scholes_prices(base_s, k, r, q, base_vol, t)
    st.sidebar.markdown("**Base Option Prices:**")
    st.sidebar.write(f"Call Price: {base_call:.4f}")
    st.sidebar.write(f"Put Price:  {base_put:.4f}")
    
    # ----- SENSITIVITY GRID RANGES (Sidebar) -----
    st.sidebar.header("Sensitivity Grid Ranges")
    s_min = st.sidebar.number_input("Min Underlying Price", value=80.0)
    s_max = st.sidebar.number_input("Max Underlying Price", value=120.0)
    num_s = st.sidebar.number_input("Number of Underlying Price Steps", value=20, step=1)
    
    v_min = st.sidebar.number_input("Min Volatility (σ)", value=0.1, step=0.01)
    v_max = st.sidebar.number_input("Max Volatility (σ)", value=0.5, step=0.01)
    num_v = st.sidebar.number_input("Number of Volatility Steps", value=20, step=1)
    
    # Generate grid arrays
    s_range = np.linspace(s_min, s_max, int(num_s))
    v_range = np.linspace(v_min, v_max, int(num_v))
    
    # ---- BASE OPTION PRICE BUBBLES (Main Area) ----
    col_metric1, col_metric2 = st.columns(2)
    with col_metric1:
        st.markdown(
            f"""
            <div style="
                background-color: #4C4C4C;
                padding: 20px;
                border-radius: 10px;
                text-align: center;
                ">
                <h4 style="color: white; margin: 0;">Base Call Price</h4>
                <p style="color: white; font-size: 24px; margin: 0;">{base_call:.4f}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col_metric2:
        st.markdown(
            f"""
            <div style="
                background-color: #4C4C4C;
                padding: 20px;
                border-radius: 10px;
                text-align: center;
                ">
                <h4 style="color: white; margin: 0;">Base Put Price</h4>
                <p style="color: white; font-size: 24px; margin: 0;">{base_put:.4f}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    # ---- ORIGINAL HEATMAPS (First Row) ----
    original_call, original_put = compute_heatmap_data(s_range, v_range, k, r, q, t)
    
    st.write("## Option Price Heatmaps")
    col1, col2 = st.columns(2)
    with col1:
        st.write("### Call Price Heatmap")
        fig_call = plot_heatmap(original_call, v_range, s_range, "Call Price", cmap='hot')
        st.pyplot(fig_call)
    with col2:
        st.write("### Put Price Heatmap")
        fig_put = plot_heatmap(original_put, v_range, s_range, "Put Price", cmap='hot')
        st.pyplot(fig_put)

    # calc_id = insert_black_scholes_input(
    #     stock_price=base_s,
    #     strike_price=k,
    #     interest_rate=r,
    #     volatility=base_vol,
    #     time_to_expiry=t
    # )

    # for i, s_val in enumerate(s_range):
    #     for j, v_val in enumerate(v_range):
    #         # Insert call row
    #         insert_black_scholes_output(
    #             calculation_id=calc_id,
    #             volatility_shock=v_val,
    #             stock_price_shock=s_val,
    #             option_price=original_call[i, j],
    #             is_call=True
    #         )
    #         # Insert put row
    #         insert_black_scholes_output(
    #             calculation_id=calc_id,
    #             volatility_shock=v_val,
    #             stock_price_shock=s_val,
    #             option_price=original_put[i, j],
    #             is_call=False
    #         )

    # if st.button("Save BS Inputs to DB"):
    #     calc_id = insert_black_scholes_input(
    #     stock_price=base_s,
    #     strike_price=k,
    #     interest_rate=r,
    #     volatility=base_vol,
    #     time_to_expiry=t
    # )
        
    # with st.expander("Show All Input Calculations"):
    #     df_inputs = get_all_inputs()
    #     st.dataframe(df_inputs)
    
    # ---- PNL HEATMAPS (Second Row) ----
    compute_pnl = st.sidebar.checkbox("Compute PnL (use purchase prices)", value=False)
    if compute_pnl:
        st.sidebar.header("Purchase Prices for PnL Calculation")
        purchase_call = st.sidebar.number_input("Call Purchase Price", value=base_call, key="pnl_call")
        purchase_put = st.sidebar.number_input("Put Purchase Price", value=base_put, key="pnl_put")
        
        pnl_call, pnl_put = compute_heatmap_data(s_range, v_range, k, r, q, t, purchase_call, purchase_put)
        
        st.write("## PnL Heatmaps")
        col3, col4 = st.columns(2)
        with col3:
            st.write("### Call PnL Heatmap")
            fig_pnl_call = plot_heatmap(pnl_call, v_range, s_range, "Call PnL")
            st.pyplot(fig_pnl_call)
        with col4:
            st.write("### Put PnL Heatmap")
            fig_pnl_put = plot_heatmap(pnl_put, v_range, s_range, "Put PnL")
            st.pyplot(fig_pnl_put)

if __name__ == "__main__":
    main()




