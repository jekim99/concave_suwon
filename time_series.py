import pandas as pd
import numpy as np
from math import radians, cos, sin, asin, sqrt
import random
import alphashape
import geopandas as gpd
from shapely.geometry import Point
import matplotlib
import pyproj
import folium

fire = (37.261672, 127.030887) # 300m radius
fire_center = Point(fire[1], fire[0])

def get_geom_point(geom):
	return (geom.y, geom.x)

def haversine_distance(point, center, xy):
	if xy == True:
		# latitude, longitude
		lat1, lon1, lat2, lon2 = map(radians, [point[0], point[1], center[0], center[1]])
	else:
		# shapely point : longitude, latitude
		p = get_geom_point(point)
		c = get_geom_point(center)
		lat1, lon1, lat2, lon2 = map(radians, [p[0], p[1], c[0], c[1]])
		
	del_lat = lat1 - lat2
	del_lon = lon1 - lon2

	a = sin(del_lat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(del_lon / 2) **2
	c = 2 * asin(sqrt(a))
	r = 6371 # radius of earth in km
	return c * r * 1000 #return m

def get_data():
	d_list = []
	for i in range(0, 5):
		filename = "./data/time_random" + str(i) + ".csv"
		d = pd.read_csv(filename, usecols=['latitude', 'longitude']).values.tolist()
		if i > 0:
			for point in d:
				if haversine_distance(point, fire, xy=True) <= i * 100:
					# if random.random() < 0.9:
					d.remove(point)
		# print(len(d))
		d_list.append(d)

	return d_list

def timewise_hull(gdf):
	# print(gdf.crs)
	# '+proj=aea +lat_1=29.5 +lat_2=42.5'
	# proj_gdf = gdf.to_crs('epsg:5179')
	# print(proj_gdf.iat[2, 0].distance(proj_gdf.iat[3, 0]))

	inside_points = [p for p in gdf['geometry'] if haversine_distance(p, fire_center, xy=False) <= 300]
	inside_gdf = gpd.GeoDataFrame({'geometry':inside_points}, crs=4326).to_crs('+proj=aea +lat_1=29.5 +lat_2=42.5')
	hull = alphashape.alphashape(inside_gdf)
	hull = hull.to_crs('epsg:4326')
	print(hull)
	hull.plot()
	return


def main():
	d_list = get_data()
	
	for j in d_list:
		p = [Point(j[i][1], j[i][0]) for i in range(0, len(j))]
		gdf = gpd.GeoDataFrame({'geometry':p}, crs=4326)
		# print(haversine_distance(j[2], j[3], xy=True))

		timewise_hull(gdf)

	# a = Point(d_list[0][1][1], d_list[0][1][0], crs=4326) #.to_crs("epsg:5179")

	# fire_point
	# print(fire_point.distance(a))

	return

if __name__ == "__main__":
	main()