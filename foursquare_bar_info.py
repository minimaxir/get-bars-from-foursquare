import urllib2
import json
import datetime
import pandas as pd
import math
import time
from math import cos
from pandas import DataFrame
from pandas import read_csv

client_id = "INSERT CLIENT ID TOKEN HERE"
client_secret = "INSERT CLIENT SECRET TOKEN HERE"

bar_df = []
rating_df = []
category = "bar"
df = read_csv("foursquare_%s_nyc.csv" % category)

for venue in df["id"]:
	url = "https://api.foursquare.com/v2/venues/%s?client_id=%s&client_secret=%s&v=%s" % (venue, client_id, client_secret, time.strftime("%Y%m%d"))		
	try:
		req = urllib2.Request(url)
		
		success = False
		while success is False: # avoid getting HTTP Errors
			try: 	
				time.sleep(1) 	# stay within API limits
				response = urllib2.urlopen(req)
				if response.getcode() == 200:
					success = True
			except Exception, e:
				print e
	
		data = json.loads(response.read())
		response.close()
	
		bar_df.append(DataFrame(data["response"]).transpose()['attributes']['venue'])
		rating_df.append(data["response"]["venue"])

		print venue

	except Exception, e:
			print e

### WARNING: Lazy function coding ahead.

def getPrice(x):
	string = str(x)
	if '$$$$' in string:
		return '$$$$'
	elif '$$$' in string:
		return '$$$'
	elif '$$' in string:
		return '$$'
	elif '$' in string:
		return '$'
	return ''

def isHappyHour(x):
	return "Happy Hour" in str(x)
	
def getRating(x):
	try:
		return x["rating"]
	except:
		return ""

def getnumRatings(x):
	try:
		return x["ratingSignals"]
	except:
		return ""
		
def getUrl(x):
	try:
		return x["url"]
	except:
		return ""


df["price"] = map(getPrice, bar_df)
df["happyHour"] = map(isHappyHour, bar_df)
df["rating"] = map(getRating, rating_df)
df["numRatings"] = map(getnumRatings, rating_df)
df["url"] = map(getUrl, rating_df)
df["fs_url"] = map(lambda x: x["canonicalUrl"], rating_df) 	# always exists


ordered_df = df[["name","price","happyHour","rating","numRatings","categories","lat","long","checkins","url","fs_url"]]
ordered_df.to_csv("foursquare_%s_nyc_full.csv" % category,encoding='utf-8', index=False)