import io

import mercantile
import numpy as np
import rasterio
from flask import Blueprint, abort, request, send_file
from rio_color.operations import gamma, sigmoidal
from rio_color.utils import to_math_type

from db.Postgresql import getConnect, putconn
from rio_tiler import reader
from rio_tiler.utils import render

tileApp = Blueprint('tifTile', __name__)


@tileApp.route('/tiftile')
def tiftile():
    x = request.args.get('x')
    y = request.args.get('y')
    z = request.args.get('z')
    tifName = request.args.get('tname')

    tifPath1 = "d:\\data\\3010\\{}.tif".format(tifName)

    try:
        dataset = rasterio.open(tifPath1)
        tile, mask = reader.tile(dataset, int(x), int(y), int(z), tilesize=256)
        dataset.close()
        min = 0
        max = 60

        renderData = np.array([tile[0], tile[1]+tile[2]*0.3, tile[2]])

        renderData = renderData.astype(np.uint8)
        mtdata = to_math_type(renderData)
        data = sigmoidal(mtdata, 10, 0.15)*255

        buffer = render(data.astype(np.uint8), mask=mask)
        return send_file(io.BytesIO(buffer), mimetype="image/png", attachment_filename="{}_{}_{}.jpg".format(x, y, z))
    except Exception as a:
        print(a)
        return abort(404)
    finally:
        pass


@tileApp.route('/tile/landsat8Vector')
def landsat8VectorTile():
    x = request.args.get('x')
    y = request.args.get('y')
    z = request.args.get('z')

    bounds = mercantile.bounds(int(x), int(y), int(z))

    envelope = "ST_MakeEnvelope({},{},{},{})".format(
        bounds.west, bounds.south, bounds.east, bounds.north)
    querySql = '''WITH mvtgeom AS
                (
                SELECT ST_AsMVTGeom(geom, {}) AS geom,gid as id,path,row
                FROM wrs2_descending
                WHERE ST_Intersects(geom, {})
                )
                SELECT ST_AsMVT(mvtgeom.*,'contour',4096,'geom','id')
                FROM mvtgeom;'''.format(envelope, envelope)

    conn, cursor = getConnect()

    cursor.execute(querySql)
    blob = cursor.fetchone()

    result = blob[0]
    putconn(conn)

    return send_file(io.BytesIO(result), mimetype="application/x-protobuf", attachment_filename="{}_{}_{}.mvt".format(x, y, z))
