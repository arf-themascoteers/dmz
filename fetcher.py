import ee
import geemap
import os
import geopandas as gpd

ee.Initialize(project='edge3-448100')

gdf = gpd.read_file('shp/DMS_Owned_Parcel.shp')
region = geemap.geopandas_to_ee(gdf)

region = region.geometry().transform('EPSG:3857', True)

collection = (ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
              .filterBounds(region)
              .sort('system:time_start', False))

image = collection.first()
ndvi = image.normalizedDifference(['B8', 'B4']).rename('NDVI')

print("NDVI image processed successfully.", ndvi)
