from flask import Blueprint, request, Response

from db.Postgresql import getConnect,  putconn
from db.Util import rowsToObject, objectsToJson

searchApp = Blueprint('search', __name__)


@searchApp.route('/search')
def search():

    path = request.args.get('path')
    row = request.args.get('row')

    conn, cursor = getConnect()

    sql = "select product_id,cloud_cover,acquisition_date,path,row  from landsat8 where path={} and row ={}".format(
        path, row)
    cursor.execute(sql)
    rows = cursor.fetchall()

    result = rowsToObject(cursor, rows)
    jsonData = objectsToJson(result)

    putconn(conn)

    return Response(jsonData, mimetype='application/json')
