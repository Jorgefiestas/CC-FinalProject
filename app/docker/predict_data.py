from prophet import Prophet
from influxdb_client import InfluxDBClient, Point, Dialect
from influxdb_client.client.write_api import SYNCHRONOUS

from fetch_data import BatchPush
from datetime import date

import pandas as pd

TOKEN = "_RlEoApP3EV-1axfl7kTqa-gWsUn5CFSkZ61kFs0YZy2jwfwQTWyHKNRuMMsUtIOsBm71pQ7a0-U65rQyGoaxg=="
client = InfluxDBClient(url="http://influxdb-service:8086", token=TOKEN, org="UTEC")

def query_idb(stock, field, bucket):
	query_api = client.query_api()

	query = """from(bucket:"Prueba") 
				|> range(start: -20d)
				|> filter(fn : (r) =>
					r.stock == "AAPL" and
					r._field == "high"
				)""".format(bucket, stock, field)

	return query_api.query_data_frame(query)


def forecast(stock, field, bucket_in, bucket_out):
	df = query_idb(stock, field, bucket_in)

	df = df[['_time', '_field', 'stock', '_value']]
	df = df[df['stock'] == stock]
	df = df[df['_field'] == field]

	df = df.drop(['stock', '_field'], axis=1)
	df['_time'] = df['_time'].dt.tz_localize(None)

	df.columns = ['ds', 'y']

	model = Prophet(
			interval_width=0.95,
			growth='linear',
			daily_seasonality=True,
			weekly_seasonality=True,
			yearly_seasonality=True,
			seasonality_mode='multiplicative'
		)
	model.fit(df)

	future_pd = model.make_future_dataframe(
		periods=180,
		freq='d',
		include_history=True
	)

	forecast_df = model.predict(future_pd)
	forecast_df = forecast_df[['ds', 'yhat']]

	bp = BatchPush(bucket_out)
	for idx, row in forecast_df.iterrows():
		p = Point('stock').tag('stock', stock).time(row[0])
		p = p.field(field, float(row[1]))
		bp.add(p.to_line_protocol())
	bp.push()
		

	return

