

from rio_tiler.utils import render
from rio_tiler import reader
from rio_color.utils import to_math_type
from rio_color.operations import gamma, sigmoidal
from flask import Blueprint, abort, request, send_file
import rasterio
import numpy as np
import mercantile
import io
import json
import datetime

import sys
sys.path.append("D:\\projects\\landsat8\\explorer\\landsat8_explorer")

from db.Util import rowsToObject,objectsToJson
from db.Postgresql import getConnect, putconn


x = 849
y = 419
z = 10

bounds = mercantile.bounds(int(x), int(y), int(z))

querySql = "select product_id,cloud_cover,acquisition_date,path,row  from landsat8 where path=122 and row =35"

conn, cursor = getConnect()

cursor.execute(querySql)
rows = cursor.fetchall() 

result = rowsToObject(cursor,rows)
list2 = objectsToJson(result)


print(result)

putconn(conn)

print(querySql)
