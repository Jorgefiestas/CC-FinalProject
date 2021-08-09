from datetime import datetime
from time import sleep

import requests
import pytz
import csv

import influxdb_client
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

class BatchPush:
	def __init__(self, bucket, batch_size=5000):
		self.DBURL = "http://influxdb-service:8086"
		self.TOKEN = "vnghrD2mQGTT77pWJoOIKDjnjPpgBHqSIYPBXznsnZGKicNpnDD6cRsHJtnIGRFPkHXaSS6wjbHYLNmBPCZkKw=="
		self.ORG = "UTEC"

		self.bucket = bucket
		self.batch_size = batch_size

		self.client = InfluxDBClient(url=self.DBURL, token=self.TOKEN, org=self.ORG)
		self.batch_values = []

	def add(self, val):
		self.batch_values.append(val) 
		if (len(self.batch_values) == self.batch_size):
			self.push()

	def push(self):
		if (len(self.batch_values) > 0):
			with self.client.write_api(write_options=SYNCHRONOUS) as write_api:
				write_api.write(self.bucket, self.ORG, self.batch_values)
			self.batch_values = []


class AlphaVantageRequest():
	def __init__(self):
		self.URL = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY_EXTENDED&interval=5min&slice=year{}month{}&symbol={}&apikey=HV01ONZPAKODE9RT'
		return

	def request(self, equity, bucket):
		bp = BatchPush(bucket)

		for year in range(1,3):
			for month in range(1,13):
				download = self.__request__(year, month, equity)
				download = download.content.decode('utf-8')

				rows = list(csv.reader(download.splitlines(), delimiter=','))

				for row in rows[1:]:
					p = Point('stock').tag('stock', equity).time(row[0])
					for name, val in zip(rows[0][1:], row[1:]):
						p = p.field(name, float(val))
						bp.add(p.to_line_protocol())
		bp.push()


	def __request__(self, year, month, equity):
		with requests.Session() as s:
			while True:
				query_url = self.URL.format(year, month, equity);
				download = s.get(query_url)
				if 'Thank you' in download.text:
					sleep(60)
				else:
					break

		return download
