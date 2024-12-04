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
        fig, ax = plt.subplots()
        ax.plot(df['Date'], df['Close'], label='Close Price')
        ax.set_title(f"Stock Prices for {symbol}")
        ax.set_xlabel("Date")
        ax.set_ylabel("Close Price")
        ax.legend()

        st.pyplot(fig)

        # Display data table
        st.write("Stock Data Table", df)

    except Exception as e:
        st.error(f"Error: {e}")
