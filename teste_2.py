import requests
import pandas as pd
from bs4 import BeautifulSoup

# Extrair dados do sítio

url = 'https://finance.yahoo.com/quote/AAPL/history?p=AAPL'

response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')

table = soup.find("table", {"data-test": "historical-prices"})

# Extrair dados de uma tabela

data = []

table_body = table.find("tbody")

rows = table_body.find_all("tr")

for row in rows:
    cols = row.find_all("td")
    cols = [ele.text.strip() for ele in cols]
    data.append([ele for ele in cols if ele])
    
# Converter o dado para o pandas dataframe

df = pd.DataFrame(data, columns = ["Date", "Open", "High", "Low", "Close", "Adj Close", "Volume"])

# Limpar e transformar o dado

df["Date"] = pd.to_datetime(df["Date"])

df = df.set_index("Date")

df = df.astype({"Open": float, "High": float, "Low": float, "Close": float, "Adj Close": float, "Volume": int})

# Analizando o dado e gerando relatório

average_daily_return = df["Adj Close"].pct_change().mean()

maximum_daily_return = df["Adj Close"].pct_change().max()

minimum_daily_return = df["Adj Close"].pct_change(). min()

print("Average Daily Return", average_daily_return)

print("Maximum Daily Return", maximum_daily_return)

Print("Minimum Daily Return", minimum_daily_return)

# Salvando o relatório em CSV

df.to_csv("daily_stock_prices.csv", index = True)