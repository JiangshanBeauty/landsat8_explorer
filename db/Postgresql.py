from db.Config import POSTGRE_HOST, POSTGRE_PORT, POSTGRE_USER, POSTGRE_PASSWORD, POSTGRE_DATABASE

from psycopg2.pool import SimpleConnectionPool
from psycopg2 import extensions, OperationalError

_pgpool = None


def getConnect():
    global _pgpool
    if not _pgpool:
        try:
            _pgpool = PostgresConnectionPool()
            print("创建")
        except Exception as exc:
            _pgpool = None
    return _pgpool.getConnect()




def putconn(conn):
    _pgpool.connectPool.putconn(conn)


class PostgresConnectionPool:
    def __init__(self):
        try:
            self.connectPool = SimpleConnectionPool(2, 20, host=POSTGRE_HOST, port=POSTGRE_PORT,
                                                    user=POSTGRE_USER, password=POSTGRE_PASSWORD,
                                                    database=POSTGRE_DATABASE, keepalives=1,
                                                    keepalives_idle=30, keepalives_interval=10,
                                                    keepalives_count=5)
        except Exception as e:
            print(e)

    def getConnect(self):
        conn = self.connectPool.getconn()
        cursor = conn.cursor()
        return conn, cursor
