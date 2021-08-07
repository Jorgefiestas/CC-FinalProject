from flask import Flask
from fetch_data import AlphaVantageRequest
from threading import Thread

app = Flask(__name__)

@app.route("/fetch/<stock>/<bucket>")
def query(stock, bucket):
	fetcher = AlphaVantageRequest()

	fetcher.request(stock, bucket)

	return 'started'


if __name__ == "__main__":
	app.run(host='0.0.0.0')
