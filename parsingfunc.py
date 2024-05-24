import pandas as pd
import requests
import schedule
import time
import analyzer
file_path = 'C:/Users/Marat/Desktop/APLHAVANTAGE/Russian_Stocks_on_MOEX.csv'
try:
    df = pd.read_csv(file_path, sep=';', on_bad_lines='skip')
except FileNotFoundError:
    print(f"Файл не найден по указанному пути: {file_path}")
    exit()
except pd.errors.ParserError as e:
    print(f"Ошибка парсинга: {e}")
    exit()
closing_prices = {}
company_names = {}
for index, row in df.iterrows():
    ticker = row['Ticker']
    closing_prices[ticker] = []
    company_names[ticker] = row['Company']
def get_stock_data(symbol, api_key):
    url = 'https://www.alphavantage.co/query'
    params = {'function': 'TIME_SERIES_INTRADAY','symbol': symbol,'interval': '5min','apikey': api_key,'outputsize': 'compact'}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        time_series = data.get('Time Series (5min)', {})
        if time_series:
            last_time = sorted(time_series.keys())[-1]
            last_data = time_series[last_time]
            close_price = float(last_data['4. close'])
            if symbol in closing_prices:
                closing_prices[symbol].append(close_price)
                if len(closing_prices[symbol]) > 2:
                    closing_prices[symbol].pop(0)
        else:
            print(f"Нет данных во временном ряде для {symbol}.")
    else:
        print(f"Ошибка {response.status_code} при запросе данных для {symbol}.")
def process_all_stocks():
    for index, row in df.iterrows():
        symbol = row['Ticker']
        api_key = row['key']
        get_stock_data(symbol, api_key)
    analysis_data = {company_names[ticker]: prices for ticker, prices in closing_prices.items()}
    analyzer.analyze_data(analysis_data)
schedule.every().hour.do(process_all_stocks)
while True:
    schedule.run_pending()
    time.sleep(1)
    
