import streamlit as st
import time
import matplotlib.pyplot as plt

from grab import fetch_stock_data
from parse import parse_stock_data

st.title("Stock Data Analysis")

# User inputs
symbol = st.text_input("Stock Symbol", "AAPL")
start_date = st.date_input("Start Date")
end_date = st.date_input("End Date")

if st.button("Fetch Data"):
    try:
        start_time = int(time.mktime(start_date.timetuple()))
        end_time = int(time.mktime(end_date.timetuple()))
        json_data = fetch_stock_data(symbol, start_time, end_time)
        df = parse_stock_data(json_data)

        # Plot the data
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 15))

        # Close Price
        ax1.plot(df['Date'], df['Close'], label='Close Price')
        ax1.set_title(f"Close Prices for {symbol}")
        ax1.set_xlabel("Date")
        ax1.set_ylabel("Close Price")
        ax1.legend()

        # High Price
        ax2.plot(df['Date'], df['High'], label='High Price', color='green')
        ax2.set_title(f"High Prices for {symbol}")
        ax2.set_xlabel("Date")
        ax2.set_ylabel("High Price")
        ax2.legend()

        # Low Price
        ax3.plot(df['Date'], df['Low'], label='Low Price', color='red')
        ax3.set_title(f"Low Prices for {symbol}")
        ax3.set_xlabel("Date")
        ax3.set_ylabel("Low Price")
        ax3.legend()

        st.pyplot(fig)

        # Display data table
        st.write("Stock Data Table", df)

    except Exception as e:
        st.error(e)