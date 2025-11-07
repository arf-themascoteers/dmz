import ee
import geemap
import geopandas as gpd
from datetime import datetime

ee.Initialize(project='edge3-448100')

gdf = gpd.read_file(r'C:\Users\m.rahman\PythonProjects\dmz\gj\dmz.geojson')
region = geemap.geopandas_to_ee(gdf)

start_year = 2019
end_year = 2025

for year in range(start_year, end_year + 1):
    for month in range(1, 13):
        if year == 2025 and month > 10:
            break  # Stop at October 2025

        start_date = f'{year}-{month:02d}-01'
        end_date = f'{year}-{month:02d}-{30 if month != 2 else 28}'

        collection = (ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
                      .filterBounds(region)
                      .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 30))
                      .filterDate(start_date, end_date)
                      .sort('system:time_start', False))

        size = collection.size().getInfo()

        if size > 0:
            mean_image = collection.reduce(ee.Reducer.mean())
            ndvi = mean_image.normalizedDifference(['B8_mean', 'B4_mean']).rename('NDVI')

            export_task = ee.batch.Export.image.toDrive(
                image=ndvi,
                description=f'ndvi_{year}_{month:02d}',
                folder='gee_output',
                fileNamePrefix=f'ndvi_{year}_{month:02d}',
                scale=10,
                region=region.geometry()
            )

            export_task.start()
        else:
            print(f'No images found for {start_date} to {end_date}.')
