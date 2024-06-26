import twstock
import yfinance as yf
from datetime import datetime, timedelta

def check_stock_exist(symbol):
    stock = yf.Ticker(symbol)
    return 'symbol' in stock.info

def get_stock_info_by_id(stock_id):
    stock = twstock.realtime.get(stock_id)
    
    if not stock['success']:
        return None
    
    data = get_stock_data_by_id(stock_id, '1D')

    info = {
        'stock_name': stock['info']['fullname'],
        'stock_id': stock['info']['code'],
        'current_price': round(data[list(data)[-1]]['Close'], 2)
    }

    return info

def get_stock_data_by_id(stock_id, timescale):
    # interval
    # 1 2 5 15 30 60 90m
    # 1h
    # 1d 5d
    # 1wk
    # 1 3mo
    found_stock = False
    for suffix in ['.TW', '.TWO']:
        symbol = stock_id + suffix
        if check_stock_exist(symbol):
            stock = yf.Ticker(symbol)
            found_stock = True
            break
    if not found_stock:
        return None

    current_time = datetime.now()

    if timescale == '1D':
        if current_time.weekday() == 5: # Saturday
            start_time = (current_time - timedelta(days=1)).replace(hour=9, minute=0, second=0)
        elif current_time.weekday() == 6: # Sunday
            start_time = (current_time - timedelta(days=2)).replace(hour=9, minute=0, second=0)
        elif current_time.time() < datetime.strptime('09:00:00', '%H:%M:%S').time():
            start_time = (current_time - timedelta(days=1)).replace(hour=9, minute=0, second=0)
        else:
            start_time = current_time

        data = stock.history(start=start_time.strftime('%Y-%m-%d'), interval='5m')
        data = data.to_dict(orient='index')
        data = {
            timestamp.to_pydatetime().strftime('%Y-%m-%d %H:%M'): values for timestamp, values in data.items()
        }
    elif timescale == '1W':
        start_time = current_time - timedelta(weeks=1)
        data = stock.history(start=start_time.strftime('%Y-%m-%d'), end=(current_time + timedelta(weeks=1)).strftime('%Y-%m-%d'), interval='1h')    
        data = data.to_dict(orient='index')
        data = {
            timestamp.to_pydatetime().strftime('%Y-%m-%d %H:%M'): values for timestamp, values in data.items()
        }
    elif timescale == '1M':
        start_time = current_time - timedelta(days=30)
        data = stock.history(start=start_time.strftime('%Y-%m-%d'), end=(current_time + timedelta(weeks=1)).strftime('%Y-%m-%d'), interval='1d')    
        data = data.to_dict(orient='index')
        data = {
            timestamp.to_pydatetime().strftime('%Y-%m-%d'): values for timestamp, values in data.items()
        }
    elif timescale == '1Y':
        start_time = current_time - timedelta(days=365)
        data = stock.history(start=start_time.strftime('%Y-%m-%d'), end=(current_time + timedelta(weeks=1)).strftime('%Y-%m-%d'), interval='5d')
        data = data.to_dict(orient='index')
        data = {
            timestamp.to_pydatetime().strftime('%Y-%m-%d'): values for timestamp, values in data.items()
        }
    else:
        raise ValueError("Invalid timescale")
  
    return data