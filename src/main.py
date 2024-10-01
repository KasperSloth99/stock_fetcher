import yfinance as yf
import os
import pandas as pd
import sys

def cleanup_directory():
    print("Cleaning up old files")
    current_directory = os.getcwd()
    for filename in os.listdir(current_directory):
        if filename.endswith('.xlsx') or filename.endswith('.csv'):
            file_path = os.path.join(current_directory, filename)
            os.remove(file_path)
            print(f'Deleted: {file_path}')

def get_tickers():
    with open('stocks_to_track.txt', 'r') as file:
        data = file.readlines()
        
    stock_names_single_string = ' '.join(name.strip() for name in data)
    stock_names_split = stock_names_single_string.split(' ')
    print("You are tracking these stocks:", stock_names_single_string)

    tickers = yf.Tickers(stock_names_single_string)
    return (stock_names_split, tickers)

[split_names, tickers] = get_tickers()

def get_history(name):
    history = tickers.tickers[name].history(period="1mo",actions=True)
    if history.index.tz is not None:
        history.index = history.index.tz_localize(None)
    adjusted_history = history[['Open', 'High', 'Low', 'Close', 'Volume']]
    adjusted_history.insert(0, 'Ticker', name)
    return adjusted_history

def fetch_stocks_to_excel():
    with pd.ExcelWriter('stocks.xlsx', engine='xlsxwriter') as writer:
        for stock_name in split_names:
            get_history(stock_name).to_excel(writer, sheet_name=stock_name, index=True)

def fetch_stocks_to_csv():
    all_data = [] 
    for stock_name in split_names:
        all_data.append(get_history(stock_name)) 
    final_data = pd.concat(all_data)
    final_data.to_csv('stocks.csv', index=True)

def main(user_input):
    cleanup_directory()
    if user_input == '0':
        print("Fetching stocks to csv")
        fetch_stocks_to_csv()
    elif user_input == '1':
        print("Fetching stocks to excel")
        fetch_stocks_to_excel()
    elif user_input == '2':
        print("Fetching stocks to both csv and excel")
        fetch_stocks_to_csv()
        fetch_stocks_to_excel()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print("No input provided, exitting.")