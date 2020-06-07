
import json
import psycopg2

import ogr


def getLeftLong(lon):
    if lon > 0:
        return -360+lon
    return lon


def getRightLong(lon):
    if lon < 0:
        return 360+lon
    return lon


worldgeom = ogr.CreateGeometryFromWkt(
    "POLYGON((-180 -90,180 -90,180 90,-180 90,-180 -90))")

dataPath = "C:\\Users\\zffp\\Desktop\\landsat\\LANDSAT_8_C1.csv"

conn = psycopg2.connect(database="landsat8", user="postgres",
                        password="postgresql", host="127.0.0.1", port="5432")


dataList = []

headCloumn = []
with open(dataPath, "r") as newFile:
    lineString = newFile.readline()
    lineString = lineString.replace("\n", "")
    headCloumn = lineString.split(",")

    cursor = conn.cursor()

    count = 0

    for lineString in newFile:
        lineString = lineString.replace("\n", "")
        data = lineString.split(",")
        # print(lineString, data)
        dataDict = {}
        num = 0

        for cloumn in headCloumn:
            dataDict[cloumn] = data[num]
            num += 1

        upperLeftCornerLongitude = float(dataDict["upperLeftCornerLongitude"])
        upperLeftCornerLatitude = float(dataDict["upperLeftCornerLatitude"])

        upperRightCornerLongitude = float(
            dataDict["upperRightCornerLongitude"])
        upperRightCornerLatitude = float(dataDict["upperRightCornerLatitude"])

        lowerLeftCornerLongitude = float(dataDict["lowerLeftCornerLongitude"])
        lowerLeftCornerLatitude = float(dataDict["lowerLeftCornerLatitude"])

        lowerRightCornerLongitude = float(
            dataDict["lowerRightCornerLongitude"])
        lowerRightCornerLatitude = float(dataDict["lowerRightCornerLatitude"])

        jsonData = json.dumps(dataDict)

        cloudCover = float(dataDict["cloudCover"])
        product_id = dataDict["LANDSAT_PRODUCT_ID"]
        acquisition_date = dataDict["acquisitionDate"]
        path = int(dataDict["path"])
        row = int(dataDict["row"])

        collection_category = dataDict["COLLECTION_CATEGORY"]
        minLong = min([upperLeftCornerLongitude, lowerLeftCornerLongitude,
                       upperRightCornerLongitude, lowerRightCornerLongitude])
        maxlong = max([upperLeftCornerLongitude, lowerLeftCornerLongitude,
                       upperRightCornerLongitude, lowerRightCornerLongitude])

        geomString = "POLYGON(({} {},{} {},{} {},{} {},{} {}))".format(upperLeftCornerLongitude, upperLeftCornerLatitude,
                                                                       upperRightCornerLongitude, upperRightCornerLatitude,
                                                                       lowerRightCornerLongitude, lowerRightCornerLatitude,
                                                                       lowerLeftCornerLongitude, lowerLeftCornerLatitude,
                                                                       upperLeftCornerLongitude, upperLeftCornerLatitude)
        if (maxlong-minLong) > 50:
            # print(geomString)
            geomString1 = "POLYGON(({} {},{} {},{} {},{} {},{} {}))".format(getLeftLong(upperLeftCornerLongitude), upperLeftCornerLatitude,
                                                                            getLeftLong(
                                                                                upperRightCornerLongitude), upperRightCornerLatitude,
                                                                            getLeftLong(
                                                                                lowerRightCornerLongitude), lowerRightCornerLatitude,
                                                                            getLeftLong(
                                                                                lowerLeftCornerLongitude), lowerLeftCornerLatitude,
                                                                            getLeftLong(upperLeftCornerLongitude), upperLeftCornerLatitude)

            geomString2 = "POLYGON(({} {},{} {},{} {},{} {},{} {}))".format(getRightLong(upperLeftCornerLongitude), upperLeftCornerLatitude,
                                                                            getRightLong(
                                                                                upperRightCornerLongitude), upperRightCornerLatitude,
                                                                            getRightLong(
                                                                                lowerRightCornerLongitude), lowerRightCornerLatitude,
                                                                            getRightLong(
                                                                                lowerLeftCornerLongitude), lowerLeftCornerLatitude,
                                                                            getRightLong(upperLeftCornerLongitude), upperLeftCornerLatitude)
            geom1 = ogr.CreateGeometryFromWkt(geomString1)
            geom1 = geom1.Intersection(worldgeom)

            geom2 = ogr.CreateGeometryFromWkt(geomString2)
            geom2 = geom2.Intersection(worldgeom)

            geom = geom1.Union(geom2)
            geomString = geom.ExportToWkt()

        sql = "insert into landsat8(id,geom,content,cloud_cover,product_id,acquisition_date,path,row,collection_category) values({},ST_GeomFromText('{}',4326),'{}',{},'{}','{}',{},{},'{}')".format(
            "nextval('meta_id')", geomString, jsonData, cloudCover, product_id, acquisition_date, path, row, collection_category)
        cursor.execute(sql)
        # print(sql)
        count += 1

        if count % 5000 == 0:
            print(count)
            conn.commit()  # 事物提交

conn.commit()  # 事物提交
# 关闭数据库连接
conn.close()
