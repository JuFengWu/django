import serpapi 

def get_current_price(stockNumber):

    client = serpapi.Client(api_key="752b35dcc6e9b337ebcf540de04a3e717161c7253d6dabcede04961f505192c8")
    results = client.search({
        'engine': 'google',
        'q': 'TPE: ' + stockNumber,
    })

    current_stock_price = results['answer_box']['price']
    return current_stock_price
if __name__ == "__main__":
    stockNumber = "2454"
    current_stock_price = get_current_price(stockNumber)
    print(current_stock_price)
