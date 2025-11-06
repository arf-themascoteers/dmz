import ee
import geemap
import geopandas as gpd

ee.Initialize(project='edge3-448100')

gdf = gpd.read_file(r'C:\Users\m.rahman\PythonProjects\dmz\gj\dmz.geojson')
region = geemap.geopandas_to_ee(gdf)

start_date = '2025-09-01'
end_date = '2025-09-30'

collection = (ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
              .filterBounds(region)
              .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 30))
              .filterDate(start_date, end_date)
              .sort('system:time_start', False))

size = collection.size().getInfo()

if size > 0:
    mean_image = collection.mean()
    ndvi = mean_image.normalizedDifference(['B8', 'B4']).rename('NDVI')

    export_task = ee.batch.Export.image.toDrive(
        image=ndvi,
        description='ndvi_09_2025',
        folder='gee_output',
        fileNamePrefix='ndvi_09_2025',
        scale=10,
        region=region.geometry()
    )

    export_task.start()
else:
    print('No images found for September 2025.')
