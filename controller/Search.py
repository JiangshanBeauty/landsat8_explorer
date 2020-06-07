from flask import Blueprint, request, Response

from db.Postgresql import getConnect,  putconn
from db.Util import rowsToObject, objectsToJson
import urllib.request

searchApp = Blueprint('search', __name__)


@searchApp.route('/search')
def search():

    path = request.args.get('path')
    row = request.args.get('row')

    conn, cursor = getConnect()

    sql = "select product_id,cloud_cover,acquisition_date,path,row  from landsat8 where path={} and row ={} and collection_category!='T2' order by acquisition_date  DESC  limit 50".format(
        path, row)
    cursor.execute(sql)
    rows = cursor.fetchall()

    result = rowsToObject(cursor, rows)
    jsonData = objectsToJson(result)

    putconn(conn)

    return Response(jsonData, mimetype='application/json')


@searchApp.route('/getmeta')
def getMetaData():
    path = request.args.get('path')
    row = request.args.get('row')
    product_id = request.args.get('product_id')

    url = 'http://8.210.87.140:802/c1/L8/{}/{}/{}/{}_MTL.json'.format(
        path, row, product_id, product_id)

    print(url)
    resp = urllib.request.urlopen(url)
    result = resp.read()
    #print(result)

    #jsonData = objectsToJson({'a': "helloworld"})
    return Response(result, mimetype='application/json')
