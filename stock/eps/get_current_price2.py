import serpapi 

client = serpapi.Client(api_key="752b35dcc6e9b337ebcf540de04a3e717161c7253d6dabcede04961f505192c8")
results = client.search({
    'engine': 'google',
    'q': 'TPE: 2454',
})

current_stock_price = results['answer_box']['price']
print(current_stock_price)
