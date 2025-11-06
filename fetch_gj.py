import ee
import geemap
import geopandas as gpd

ee.Initialize(project='edge3-448100')

gdf = gpd.read_file(r'C:\Users\m.rahman\PythonProjects\dmz\gj\dmz.geojson')
region = geemap.geopandas_to_ee(gdf)

collection = (ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
              .filterBounds(region)
              .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 30))
              .sort('system:time_start', False))

size = collection.size().getInfo()

if size > 0:
    image = collection.first()

    if image and 'B8' in image.bandNames().getInfo() and 'B4' in image.bandNames().getInfo():
        ndvi = image.normalizedDifference(['B8', 'B4']).rename('NDVI')

        export_task = ee.batch.Export.image.toDrive(
            image=ndvi,
            description='last_ndvi',
            folder='gee_output',
            fileNamePrefix='last_ndvi2',
            scale=10,
            region=region.geometry()
        )

        export_task.start()
    else:
        print('Required bands (B8, B4) are not available.')
else:
    print('No images found in the collection.')
