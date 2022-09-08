
# Raw Package
import numpy as np
import pandas as pd
from datetime import date
from numpy.polynomial import Chebyshev
import os 
import yfinance as yf
import pickle
import math

# Creating an object to store all the important informations.
class inventory:
    cash = 100000
    capital_gain = 0
    capital_loss = 0
    holdings = pd.DataFrame(columns=['Ticker', 'Price', 'Amount'])



# Buy a stock, provide the ticker name and the number of stock to buy
def buy_stock(wallet, ticker, amount):
    
    data = yf.download(tickers=ticker, period='1d', interval='1d')

    closing_price = data["Close"].item()
    closing_price = round(closing_price, 2)

    if wallet.cash < closing_price*amount:
        raise Exception("Sorry not enough money. buy less.")

    purchase = {'Ticker': ticker, 'Price': closing_price, 'Amount': amount}

    #update balance
    wallet.holdings = wallet.holdings.append(purchase, ignore_index=True)
    wallet.cash = wallet.cash - closing_price*amount #current cash amount - purchased amount

    print("Holdings:")
    print(wallet.holdings)
    print("Cash on hand:", wallet.cash)



# given a specific ticker, buy as much as you can. No partical stock. 
def buy_max(wallet, ticker):
    data = yf.download(tickers=ticker, period='1d', interval='1d')

    closing_price = data["Close"].item()
    closing_price = round(closing_price, 2)

    amount = wallet.cash/closing_price
    amount = math.floor(amount)

    buy_stock(wallet, ticker, amount)



# Sell a stock. Provide the index (check the dataframe in wallet.holding) and the number of shares to sell
def sell_stock(wallet, sell_index, sell_amount):

    #wallet info: what you have
    ticker = wallet.holdings.at[sell_index, 'Ticker']
    amount = wallet.holdings.at[sell_index, 'Amount']
    price = wallet.holdings.at[sell_index, 'Price']


    #error check: enough stocks to sell
    if sell_amount > amount:
        raise Exception("Not enough to sell. sell less.")

    #current prices
    data = yf.download(tickers=ticker, period='1d', interval='1d')
    closing_price = data["Close"].item()
    closing_price = round(closing_price, 2)

    print(f"You have {amount} of {ticker} bought at ${price}, you're selling {sell_amount} for ${closing_price}")

    #Transaction - remove sold, convert to cash

    #update the amount you've sold 
    wallet.holdings.at[sell_index, 'Amount'] = amount - sell_amount 
    #update cash
    wallet.cash = wallet.cash + (sell_amount*closing_price)

    #capital gain and capital loss calculation
    #gain - if you sell more than you bought for
    if  closing_price * sell_amount > price * sell_amount:
        wallet.capital_gain = price * sell_amount - closing_price * sell_amount
    #loss - if you sell for less than you bought for 
    elif closing_price * sell_amount < price * sell_amount :
        wallet.capital_loss =  closing_price * sell_amount - price * sell_amount

    print(f"Updated cash balance: {wallet.cash}")
    print(f"Updated holdings: \n {wallet.holdings}")


def panic_sell(wallet):
    #print(wallet.holdings)
    print("Panic!")
    #loop through each one and sell it: 
    for index, row in wallet.holdings.iterrows():
        if row['Amount'] > 0:
            print(f"Selling {row['Amount']} shares of {row['Ticker']}; index of {index}")
            sell_stock(wallet, index, row["Amount"])



#saving or loading previous wallet
def load(name):
    pickle_in = open(f'{name}.pickle', 'rb')
    wallet = pickle.load(pickle_in)
    print("loaded")
    return(wallet)

def save(wallet, name):
    pickle_out = open(f'{name}.pickle', 'wb')
    pickle.dump(wallet, pickle_out)
    pickle_out.close()
    print("saved. you may close.")