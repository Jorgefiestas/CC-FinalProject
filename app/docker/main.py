from flask import Flask
from fetch_data import AlphaVantageRequest
from predict_data import forecast
from threading import Thread

app = Flask(__name__)

@app.route("/fetch/<stock>/<bucket>")
def fetch(stock, bucket):
	fetcher = AlphaVantageRequest()
	fetcher.request(stock, bucket)

	return 'Finished'

@app.route("/prediction/<stock>/<field>/<bucket1>/<bucket2>")
def prediction(stock, field, bucket1, bucket2):
	forecast(stock, field, bucket1, bucket2)
	return 'Finished'

if __name__ == "__main__":
	print("HERE")
	app.run(host='0.0.0.0')
