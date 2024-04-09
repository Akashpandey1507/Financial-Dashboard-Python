# Importing the libraries
import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import datetime as dt
# -------------------------------------------------------------------------------------------

#---------------------------------------Fetch the data---------------------------------------
# Function to fetch stock data
def get_stock_data(ticker, start_date, end_date, frequency):
    data = yf.download(ticker, start=start_date, end=end_date, interval=frequency) # Download the datasets from yahoo finance
    data['Retrun'] = data['Adj Close'].pct_change()  # Calculate returns
    data['Retrun'] = data['Retrun'].fillna(0)        # Fill missing
    data.reset_index(inplace=True)
    data['Date'] = data['Date'].dt.strftime('%d-%m-%Y')
    #data = data.drop(columns='index',axis=1)
    #data = data.drop('index')                   # Remove
    return data


#--------------------------------------Dashboard---------------------------------------------
# Function to create financial dashboard
def create_dashboard():
    st.title('Financial Dashboard - Sensex')

    # Sidebar for user input
    st.sidebar.title('Dashboard Settings')
    ticker = st.sidebar.text_input('Enter Ticker Symbol', '^NSEI')
    current_datetime = dt.datetime.now()
    new_datetime = current_datetime - dt.timedelta(days=365.25 * 50)
    start_date = st.sidebar.date_input('Start Date', new_datetime)
    end_date = st.sidebar.date_input('End Date', current_datetime)
    Daily = '1d'
    Weekly = '1wk'
    Monthly = '1mo'
    frequency = st.sidebar.selectbox('Frequency', [Daily, Weekly, Monthly])
    refresh_button = st.sidebar.button('Refresh Data')

    # Fetch stock data if refresh button is clicked
    if refresh_button:
        st.sidebar.write("Refreshing data...")
        stock_data = get_stock_data(ticker, start_date, end_date, frequency)
        stock_data.reset_index(inplace=True)
        # Display data table
        st.write('## Stock Data')
        st.write(stock_data)

        # Plotting
        st.write('## Stock Price Chart for ', ticker)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data['Close'], mode='lines', name='Adj Close'))
        fig.update_layout(title=f'{ticker} Stock Price',
                          xaxis_title='Date',
                          yaxis_title='Price')
        st.plotly_chart(fig)

        # Additional information
        st.write('## Additional Information')
        st.write(f'Ticker: {ticker}')
        st.write(f'Data Frequency: {frequency}')
        st.write(f'Date Range: {start_date} to {end_date}')

        
    else:
        # Fetch stock data
        stock_data = get_stock_data(ticker, start_date, end_date, frequency)
        stock_data.reset_index(inplace=True)
        # Display data table
        st.write('## Stock Data')
        st.write(stock_data)

        # Plotting
        st.write('## Stock Price Chart for ', ticker)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data['Close'], mode='lines', name='Close Price'))
        fig.update_layout(title=f'{ticker} Stock Price',
                          xaxis_title='Date',
                          yaxis_title='Price')
        st.plotly_chart(fig)

        # Additional information
        st.write('## Additional Information')
        st.write(f'Ticker: {ticker}')
        st.write(f'Data Frequency: {frequency}')
        st.write(f'Date Range: {start_date} to {end_date}')

if __name__ == "__main__":
    create_dashboard()
