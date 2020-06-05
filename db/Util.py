import json
import datetime


class DateTimeEncoder(json.JSONEncoder):
    def default(self, z):
        if isinstance(z, datetime.date):
            return (str(z))
        else:
            return super().default(z)


def rowsToObject(cursor, rows):
    colnames = [desc[0] for desc in cursor.description]
    result = [dict(zip(colnames, l)) for l in (list(row) for row in rows)]
    return result


def objectsToJson(result):
    return json.dumps(result, cls=DateTimeEncoder)
