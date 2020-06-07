import rasterio
import numpy as np
import mercantile
from rasterio import warp
from rio_tiler.io import landsat8
from rio_tiler.mercator import get_zooms
from rio_tiler.profiles import img_profiles
from rio_tiler.utils import expression
from rio_tiler.io import cogeo
from rio_tiler.utils import render
tiles = mercantile.tiles(
    112.21818, 33.93807, 112.68424, 35.66072, 10)

for tile in tiles:
    print(tile)

datapth = "http://8.210.87.140:802/c1/L8/124/036/LC08_L1TP_124036_20200522_20200527_01_T1/LC08_L1TP_124036_20200522_20200527_01_T1_B1.TIF"
tile, mask = cogeo.tile(
    datapth,
    833,  # "http://127.0.0.1:5500/mosaic_3band/013022223133.tif",
    405,
    10,
    tilesize=256
)
min = 0
max = 34952


tile = (tile-min)/max*255
buffer = render(tile.astype(np.uint8), mask=mask)

with open("my.png", "wb") as f:
    f.write(buffer)


print(tiles)
