import urllib2
import json
import datetime
import pandas as pd
import math
import time
from math import cos
from pandas import DataFrame

### Helper function for converting meters to lat/long

def distcust(p, d, lat_m, long_m):
	lat = p['lat']
	long = p['long']
	
	lat1 = lat + lat_m * (d / (11100.0/90*1000) * cos(lat))
	long1 = long + long_m * (d / (11100.0/90*1000))
	
	return {'lat': lat1, 'long': long1}

client_id = "INSERT CLIENT ID TOKEN HERE"
client_secret = "INSERT CLIENT SECRET TOKEN HERE"
#p = {'lat': 37.7833, 'long': -122.4167} 	# central San Francisco, at Van Ness and Market
p = {'lat': 40.783011, 'long': -73.965368}	# central NYC, at Central Park
distance = 5000
limit = 50
gridSize = 10
df = DataFrame()
requested_keys = ["categories","id","location","name","stats"]
category = "bar"
category_id = "4d4b7105d754a06376d81259"

for x in [x1 / 10.0 for x1 in range(-3*gridSize, 3*gridSize)]:
	for y in [y1 / 10.0 for y1 in range(-3*gridSize, 3*gridSize)]:
		center = distcust(p,distance,x,y)
		url = "https://api.foursquare.com/v2/venues/search?ll=%s,%s&intent=browse&radius=%s&categoryId=%s&client_id=%s&client_secret=%s&v=%s" % (center["lat"], center["long"], distance, category_id, client_id, client_secret, time.strftime("%Y%m%d"))
		try:
			req = urllib2.Request(url)
			response = urllib2.urlopen(req)
			data = json.loads(response.read())
			response.close()
	
			data = DataFrame(data["response"]['venues'])[requested_keys]
	
			df = df.append(data,ignore_index=True)
			print center
			time.sleep(1) # stay within API limits
		except Exception, e:
			print e

df = df.drop_duplicates(cols='id',take_last=True)

df["categories"] = df["categories"].apply(lambda x: dict(x[0])['name'])
df["lat"] = df["location"].apply(lambda x: dict(x)["lat"])
df["long"] = df["location"].apply(lambda x: dict(x)["lng"])
df["checkins"] = df["stats"].apply(lambda x: dict(x)["checkinsCount"])

ordered_df = df[["name","id","categories","lat","long","checkins"]]
ordered_df.to_csv("foursquare_%s_nyc.csv" % category,encoding='utf-8', index=False)