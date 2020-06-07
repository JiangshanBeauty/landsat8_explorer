
import numpy as np
import rasterio
from rio_tiler import reader
from rio_tiler.utils import render
from rio_color.operations import gamma, sigmoidal
from rio_color.utils import to_math_type



tifPath1 = "d:\\data\\3010\\1_1.tif"

dataset = rasterio.open(tifPath1)

band = rasterio.band(dataset, 1)


print(band)

tile, mask = reader.tile(dataset, 852, 418, 10, tilesize=1024)

min = 0
max = 405


tile1 = (tile[0]-min)/max*255
tile2 = (tile[1]-min)/max*255
tile3 = (tile[2]-min)/max*255

tileList = np.array([tile[0], tile[1], tile[2]])

renderData = np.where(tileList > 255, 255, tileList)
renderData = np.where(renderData < 0, 0, renderData)

renderData = renderData.astype(np.uint8)
mtdata = to_math_type(renderData)
data = gamma(mtdata, 1.7)

data = sigmoidal(mtdata, 10, 0)*255

buffer = render(data.astype(np.uint8), mask=mask)
with open("reraster2.png", "wb") as f:
    f.write(buffer)
