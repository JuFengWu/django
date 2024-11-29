from yahoo_fin import stock_info as si

# get Apple's live quote price
si.get_live_price("AAPL")

# or Amazon's
si.get_live_price("AMZN")