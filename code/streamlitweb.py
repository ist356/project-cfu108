import streamlit as st
import time
import matplotlib.pyplot as plt
from datetime import timedelta
import pandas as pd

from grab import fetch_stock_data
from parse import parse_stock_data

st.title("Stock Data Analysis")

# User inputs
symbol = st.text_input("Stock Symbol", "AAPL")
start_date = st.date_input("Start Date")
end_date = st.date_input("End Date")
ma_periods = st.text_input("Moving Averages (comma separated)", "3,5,7,10")

if st.button("Fetch Data"):
    try:
        # Calculate the maximum moving average period
        ma_periods_list = [int(x) for x in ma_periods.split(',')]
        max_ma_period = max(ma_periods_list)

        # Adjust start_date to include extra days for moving averages
        adjusted_start_date = start_date - timedelta(days=max_ma_period * 2)  # Rough estimate

        start_time = int(time.mktime(adjusted_start_date.timetuple()))
        end_time = int(time.mktime(end_date.timetuple()))
        json_data = fetch_stock_data(symbol, start_time, end_time)
        df = parse_stock_data(json_data)

        # Ensure we have enough data for the moving averages
        if len(df) < max_ma_period:
            st.error("Not enough data to calculate the moving averages.")
        else:
            # Calculate moving averages
            for period in ma_periods_list:
                df[f'MA_{period}'] = df['Close'].rolling(window=period).mean()

            # Filter data to the original date range
            df = df[df['Date'] >= pd.to_datetime(start_date)]

            # Plot the data
            fig, ax1 = plt.subplots(figsize=(10, 5))

            # Close Price
            ax1.plot(df['Date'], df['Close'], label='Close Price', color='blue')
            for period in ma_periods_list:
                ax1.plot(df['Date'], df[f'MA_{period}'], label=f'MA {period}', linestyle='--', alpha=0.7)

            marker_size = 10 if len(df) < 100 else 1000 / len(df)
            # High Price as scatter plot
            ax1.scatter(df['Date'], df['High'], label='High Price', color='green', marker='^', s=marker_size)

            # Low Price as scatter plot
            ax1.scatter(df['Date'], df['Low'], label='Low Price', color='red', marker='v', s=marker_size)

            ax1.set_title(f"Stock Prices for {symbol}")
            ax1.set_xlabel("Date")
            ax1.set_ylabel("Price")
            ax1.legend()

            st.pyplot(fig)

            # Display data table
            st.write("Stock Data Table", df)

            # Display data table
            st.write("Stock Data Table", df)

            # Display data table
            st.write("Stock Data Table", df)

    except Exception as e:
        st.error(e)