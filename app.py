from flask import Flask, request,  send_file, abort
import numpy as np
import rasterio
import io
from rio_tiler import reader
from rio_tiler.utils import render

from rio_color.operations import gamma, sigmoidal

from rio_color.utils import to_math_type

app = Flask(__name__)


@app.after_request
def cors(environ):
    environ.headers['Access-Control-Allow-Origin'] = '*'
    environ.headers['Access-Control-Allow-Method'] = '*'
    environ.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    environ.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    environ.headers["Pragma"] = "no-cache"
    environ.headers["Expires"] = "0"
    return environ


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/tiftile')
def tifTile():
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

    # return "tiftile{},{},{}".format(x, y, z)
