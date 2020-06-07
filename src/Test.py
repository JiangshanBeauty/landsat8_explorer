from rio_tiler.io import cogeo
from rio_tiler.utils import render
from rio_tiler import reader
from rio_tiler.colormap import get_colormap
import rasterio
import mercantile
from matplotlib import pyplot
import numpy as np

tifPath = "d:\\data\\spacenet\\mosaic_3band\\013022223133.tif"
tifPath1 = "d:\\data\\3010\\1_1.tif"

tifPath2 = "https://landsat-pds.s3.amazonaws.com/c1/L8/122/034/LC08_L1TP_122034_20200422_20200508_01_T1/LC08_L1TP_122034_20200422_20200508_01_T1_B1.TIF"
with rasterio.open(tifPath2) as src:
    print(src.bounds)
    tiles = mercantile.tiles(
        src.bounds.left, src.bounds.bottom, src.bounds.right, src.bounds.top, 10)
    for tile in tiles:
        print(tile)

"""
tile, mask = cogeo.tile(
    'http://oin-hotosm.s3.amazonaws.com/5a95f32c2553e6000ce5ad2e/0/10edab38-1bdd-4c06-b83d-6e10ac532b7d.tif',
    691559,
    956905,
    21,
    tilesize=256
)
"""

tile, mask = cogeo.tile(
    tifPath2,  # "http://127.0.0.1:5500/mosaic_3band/013022223133.tif",
    1023,
    107,
    10,
    tilesize=256
)

buffer = render(tile, mask=mask)

with open("my.png", "wb") as f:
    f.write(buffer)

print(tile)
"""

dataset = rasterio.open(tifPath1)

tile, mask = reader.tile(dataset, 426, 209, 9, tilesize=256)


colormap = get_colormap('viridis')
# print(colormap)

options = {}

options["colormap"] = colormap

arr2 = np.array([tile[3], tile[2], tile[1]])


print(tile[0])

maskarr2 = np.array([mask[0], mask[1], mask[2]])

buffer = render(tile[3], mask=mask, colormap=colormap)
with open("my.png", "wb") as f:
    f.write(buffer)
print(type(tile), arr2.shape)

#pyplot.imshow(tile[1], cmap='viridis')

# pyplot.show()
print(mask.shape)
"""
print("hello world")
