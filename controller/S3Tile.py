import io
from rio_tiler.io import cogeo
import mercantile
import numpy as np
import rasterio
from flask import Blueprint, abort, request, send_file
from rio_color.operations import gamma, sigmoidal
from rio_color.utils import to_math_type

from db.Postgresql import getConnect, putconn
from rio_tiler import reader
from rio_tiler.utils import render

s3tileApp = Blueprint('s3Tile', __name__)


@s3tileApp.route('/tile/s3tile')
def tiftile():
    x = request.args.get('x')
    y = request.args.get('y')
    z = request.args.get('z')
    tifName = request.args.get('tname')

    try:
        print("开始",x, y, z)
        datapth = "http://8.210.87.140:802/c1/L8/124/036/LC08_L1TP_124036_20200522_20200527_01_T1/LC08_L1TP_124036_20200522_20200527_01_T1_B1.TIF"
        tile, mask = cogeo.tile(datapth, int(x), int(y), int(z), tilesize=256)

        min = 0
        max = 34952

        tile = (tile-min)/max*255
        buffer = render(tile.astype(np.uint8), mask=mask)

        #renderData = np.array([tile[0], tile[0], tile[0]])

        #renderData = renderData.astype(np.uint8)
        #mtdata = to_math_type(renderData)
        #data = sigmoidal(mtdata, 10, 0.15)*255

        
        print(x, y, z)
        return send_file(io.BytesIO(buffer), mimetype="image/png", attachment_filename="{}_{}_{}.jpg".format(x, y, z))
    except Exception as a:
        print(a)
        return abort(404)
    finally:
        pass
