
class inventory:
    cash = 100000
    capital_gain = 0
    capital_loss = 0
    holdings = pd.DataFrame(columns=['Ticker', 'Price', 'Amount'])





#Buy a stock, provide the ticker name and the # of stock to buy
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

    #capital gain and capital loss
    #gain - if you sell more than you bought for
    if  closing_price * sell_amount > price * sell_amount:
        wallet.capital_gain = price * sell_amount - closing_price * sell_amount
    #loss - if you sell for less than you bought for 
    elif closing_price * sell_amount < price * sell_amount :
        wallet.capital_loss =  closing_price * sell_amount - price * sell_amount

    #update cash
    wallet.cash = wallet.cash + (sell_amount*closing_price)

    print(f"Updated cash balance: {wallet.cash}")
    print(f"Updated holdings: \n {wallet.holdings}")



#saving or loading previous wallet
def load():
    pickle_in = open('data.pickle', 'rb')
    wallet = pickle.load(pickle_in)
    print("loaded")

def save(wallet):
    pickle_out = open('data.pickle', 'wb')
    pickle.dump(wallet, pickle_out)
    pickle_out.close()
    print("saved. you may close.")