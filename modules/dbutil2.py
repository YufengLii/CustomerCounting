import time
import json
import re
from PyMysqlPool.db_util.mysql_pool import get_pool_connection
from PyMysqlPool.mysql.connector.dpooling import PooledMySQLConnection
from PyMysqlPool.mysql.connector.errors import ProgrammingError, InterfaceError, OperationalError, DatabaseError
from modules.mlogger import get_caller_info_total, get_caller_function
try:
    from modules.mlogger import mlogger as logging
except ImportError as e:
    import logging

import MySQLdb


db_config = {
        '184': {
            'host': "192.168.31.184", 'port': 3306,
            'user': "root", 'passwd': "root@1234",
            'db': "cvtest1", 'charset': "utf8",
            'isolation_level': 'READ COMMITTED',
            'pool': {
                "use":1,
                "size": 0,
                "name":"184",
            }
        },
        '33': {
            'host': "192.168.31.33", 'port': 3306,
            'user': "cv", 'passwd': "cv@aisland#17",
            'db': "cvtest1", 'charset': "utf8",
            'pool': {
                #use = 0 no pool else use pool
                "use":1,
                # size is >=0,  0 is dynamic pool
                "size":0,
                #pool name
                "name":"33",
            }
        },
        '243': {
            'host': "192.168.31.243", 'port': 3306,
            'user': "cv", 'passwd': "cv@aisland#17",
            'db': "cvtest1", 'charset': "utf8",
            'pool': {
                # use = 0 no pool else use pool
                "use": 1,
                # size is >=0,  0 is dynamic pool
                "size": 0,
                # pool name
                "name": "243",
            }
        },
    }


class DBPool(object):

    def __init__(self, config=db_config['33']):
        super(DBPool, self).__init__()
        self._db_config = config

    def __query(self, sql, args=()):

        def unpack(record):
            if isinstance(record, dict):
                for k in record.keys():
                    if isinstance(record[k], bytearray):
                        record[k] = record[k].decode('utf-8')
            elif isinstance(record, list):
                for i in range(len(record)):
                    if isinstance(record[i], dict) or isinstance(record[i], list):
                        record[i] = unpack(record[i])
                    elif isinstance(record[i], bytearray):
                        record[i] = record[i].decode('utf-8')
            return record

        code = 0
        result = ()
        try:

            conn = get_pool_connection(self._db_config)
            if not isinstance(conn, PooledMySQLConnection):
                cursor = conn.cursor(MySQLdb.cursors.DictCursor)
                if args == (): args = None
            else:
                cursor = conn.cursor(dictionary=True)

            cursor.execute(sql, args)
            result = cursor.fetchall()
            # print(result)

            result = unpack(result)
            # print(result)
        except (ProgrammingError, InterfaceError, OperationalError, DatabaseError) as e:
            logging.error("[Pool] query DatabaseError sql is %s ,_args is %s", sql, args)
            logging.error("[Pool] query DatabaseError message: %s", e)
            # conn.rollback()
            result = e.errno
        except (MySQLdb.ProgrammingError, MySQLdb.InterfaceError,
                MySQLdb.OperationalError, MySQLdb.DatabaseError) as e:
            logging.error("[Pool] query MySQLdb.DatabaseError sql is \"%s\" ,_args is \"%s\"", sql, args)
            logging.exception("[Pool] query MySQLdb.DatabaseError message: %s", e)
            try:
                code = int(str(e).split(',', 1)[0].replace('(', ''))
            except Exception:
                code = -2
        except Exception as e:
            logging.error("[Pool] query exception sql is %s ,_args is %s \n\tstacks is %s",
                      sql, args, "")
            logging.error("[Pool] query Exception message: %s", e)
            code = -1
        finally:
            try:
                cursor.close()
                conn.close()
            except Exception as e:
                pass
        return code, result

    def __execute(self, sql, args=()):
        code = 0
        result = 0
        # conn.autocommit(True) #replace False -> True
        try:
            conn = get_pool_connection(self._db_config)
            if not isinstance(conn, PooledMySQLConnection):
                cursor = conn.cursor(MySQLdb.cursors.DictCursor)
            else:
                cursor = conn.cursor(dictionary=True, buffered=True)

            if type(args) == list and len(args) > 1:
                cursor.executemany(sql, args)
            else:
                cursor.execute(sql, args)
            conn.commit()
            result = cursor.rowcount
        except (ProgrammingError, InterfaceError, OperationalError, DatabaseError,
                MySQLdb.OperationalError) as e:
            logging.error("[Pool] commit ProgrammingError sql is %s ,_args is %s", sql, args)
            logging.error("ProgrammingError message: %s", e)

            code = e.errno
        except (MySQLdb.ProgrammingError, MySQLdb.InterfaceError,
                    MySQLdb.OperationalError, MySQLdb.DatabaseError) as e:
            logging.error("[Pool] query DatabaseError sql is \"%s\" ,_args is \"%s\"", sql, args)
            logging.error("[Pool] query DatabaseError message: %s", e)
            try:
                code = int(str(e).split(',', 1)[0].replace('(', ''))
            except Exception:
                code = -2
        except Exception as e:
            logging.error("[Pool] commit exception sql is %s ,_args is %s. \n\tstacks is %s",
                          sql, args, get_caller_function())
            logging.error("Exception message: %s", e)
            code = -1
        finally:
            # print(sql)
            try:
                # print("affected rows = {}".format(cursor.rowcount))
                conn.rollback()
                cursor.close()
                conn.close()
            except Exception as e:
                pass
        return code, result

    def test_connection(self):
        code, rt = self.__query("show databases;")
        return code == 0

    def add_user(self, user_id, name, group_id, app_id=None):
        sql = "INSERT INTO Member (memberID, name, faceDB, faceGroup, faceID) VALUES ( %(user_id)s, %(name)s, " \
              "%(app_id)s, %(group_id)s, %(user_id)s);"
        return self.__execute(sql, dict(user_id=user_id, name=name, group_id=group_id, app_id=app_id))[0]

    def del_user(self, user_id):
        sql = "DELETE FROM Member WHERE memberID=%s;"
        params = (user_id,)
        return self.__execute(sql, params)[0]

    def add_stranger(self, user_id, name, property, group_id, app_id=None):
        sql = "INSERT INTO Stranger (strangerID, name, faceDB, faceGroup, faceID, property) VALUES "\
                "( %(user_id)s, %(name)s, %(db)s, %(group)s, %(user_id)s, %(property)s );"
        # print(23423, dict(user_id=user_id, db=app_id, group=group_id, property=property))
        return self.__execute(sql, dict(user_id=user_id, name=name, db=app_id, group=group_id, property=property))[0]

    def delete_stranger(self, user_id):
        sql = "DELETE FROM Stranger WHERE strangerID=%s;"
        params = (user_id,)
        return self.__execute(sql, params)

    def query_user(self, memberID=None, name=None):
        sql = "SELECT * FROM Member;"
        if memberID is not None:
            sql = sql[:-1] + ' WHERE memberID="{}";'.format(memberID)
        elif name is not None:
            sql = sql[:-1] + ' WHERE name="{}";'.format(name)
        c, r = self.__query(sql)
        if c == 0: return r
        else: return []

    def query_camera(self, cameraID=None):
        sql = "SELECT cameraID, name, stream as url, spot, resolution, " \
              "frame_rate, calibration_body, calibration_keypoint FROM Camera;"

        if cameraID is not None:
            sql = sql[:-1] + ' WHERE cameraID="{};"'.format(cameraID)

        c, r = self.__query(sql)
        if c != 0: return []
        for item in r:
            if item.get('calibration'):
                item['calibration'] = json.loads(item['calibration'])
        return r

    def query_customer(self, customerID=None):
        sql = 'SELECT * FROM Customer;'
        if customerID is not None:
            sql = sql[:-1] + ' WHERE customerID="{}";'.format(customerID)
        c, r =  self.__query(sql)
        if c == 0: return r
        else: return []

    def query_customer_within_memberinfo(self, customerID=None, memberID=None):
        sql = 'SELECT Customer.*, Member.* FROM Customer join Member on Customer.faceID=Member.faceID;'
        if customerID is not None:
            sql = sql[:-1] + ' WHERE customerID="{}";'.format(customerID)
        elif memberID is not None:
            sql = sql[:-1] + ' WHERE memberID="{}";'.format(memberID)
        c, r = self.__query(sql)
        if c == 0: return r[0]
        else: return None

    def update_headcount(self, targetID, headcount, timestamp):
        sql = "INSERT INTO AllTargetOccupancy (targetID, timestamp, headcount) " \
              "VALUE ( %(targetID)s, %(timestamp)s, %(headcount)s )" \
              "ON DUPLICATE KEY UPDATE timestamp={timestamp}, headcount={headcount}"\
            .format(timestamp=timestamp, headcount=headcount)
        self.__execute(sql, dict(targetID=targetID, timestamp=timestamp, headcount=headcount))

        sql = 'INSERT INTO {table} (timestamp, headcount) VALUES ( %(timestamp)s, %(headcount)s )'\
            .format(table="TargetArea{}Occupancy".format(targetID))
        e = self.__execute(sql, dict(timestamp=timestamp, headcount=headcount))

        if e and e == 1146 or e == '1146':
            self.__execute("CREATE TABLE IF NOT EXISTS {} LIKE TargetAreaXOccupancy;"\
                           .format("TargetArea{}Occupancy".format(targetID)))
            self.__execute(sql, dict(timestamp=timestamp, headcount=headcount))

    def query_track_tbl(self, cameraID=None, trackID=None):
        sql = 'SHOW tables;'
        if cameraID is not None and trackID is not None:
            sql = sql[:-1] + " LIKE 'Camera{cid}_Track{tid}';".format(cid=cameraID, tid=trackID)
        elif cameraID is not None:
            sql = sql[:-1] + " LIKE 'Camera{cid}_Track%';".format(cid=cameraID)
        elif trackID is not None:
            sql = sql[:-1] + " LIKE 'Camera%_Track{tid}';".format(tid=trackID)
        else:
            sql = sql[:-1] + " LIKE 'Camera%_Track%';"
            # sql = sql[:-1] + " LIKE 'TargetArea%';"

        c, r = self.__query(sql)
        if c == 0:
            return [list(d.values())[0] for d in r]
        else:
            return []

    def get_camera_tracks(self, cameraID=None):
        l = self.query_track_tbl(cameraID=cameraID)
        patt = r'Camera([\w\d]+)_Track([\w\d]+)'
        tracklist = {}
        for item in l:
            r = re.match(patt, item)
            if r:
                cid, tid = r.groups()
                if cid not in tracklist:
                    tracklist[cid] = [tid]
                else:
                    tracklist[cid].append(tid)

        if cameraID: return {cameraID: tracklist.get(cameraID,[])}

        return tracklist

    def get_trajectory(self, cameraID, trackID, trange=None):
        sql = 'SELECT timestamp, st_astext(coordinates), st_astext(rect), area FROM Camera{cid}_Track{tid};'\
            .format(cid=cameraID, tid=trackID)
        if trange is not None:
            sql = sql[:-1] + ' WHERE timestamp BETWEEN {t1} and {t2}'.format(t1=trange[0], t2=trange[1])
        c, rt = self.__query(sql)
        if c != 0: return None
        for item in rt:
            if item.get('st_astext(coordinates)'):
                try:
                    r = re.match(r'POINT\(([\d\s,\.]+)\)', item['st_astext(coordinates)'])
                    p = re.split(r',|\s', r.group(1))
                    item['coordinates'] = [float(p[0]), float(p[1])]
                    del item['st_astext(coordinates)']
                except Exception as e:
                    print(item['astext(coordinates)'])
                    print('[Exception] get_trajectory POINT parse error', e)
            if item.get('st_astext(rect)'):
                try:
                    r = re.match(r'POLYGON\(\(([\d\s,\.]+)\)\)', item['st_astext(rect)'])
                    p = re.split(r',|\s', r.group(1))
                    # item['rect'] = list(map(lambda x: float(x), [p[0], p[1], p[4], p[5]]))
                    item['rect'] = [float(p[0]), float(p[1]), float(p[4]), float(p[5])]
                    del item['st_astext(rect)']
                except Exception as e:
                    print('[Exception] get_trajectory POLYGON parse error', e)
        return rt


if __name__ == "__main__":


    import multiprocessing as mp
    from pprint import pprint
    db_config = {
        '184': {
            'host': "192.168.31.184", 'port': 3306,
            'user': "root", 'passwd': "root@1234",
            'db': "cvtest1", 'charset': "utf8",
            'isolation_level': 'READ COMMITTED',
            'pool': {
                "use":1,
                "size": 0,
                "name":"184",
            }
        },
        '33': {
            'host': "192.168.31.33", 'port': 3306,
            'user': "cv", 'passwd': "cv@aisland#17",
            'db': "cvtest1", 'charset': "utf8",
            'pool': {
                #use = 0 no pool else use pool
                "use":1,
                # size is >=0,  0 is dynamic pool
                "size":0,
                #pool name
                "name":"33",
            }
        },
    }

    pool1 = DBPool(db_config['33'])
    db = pool1

    print(2222222, pool1.test_connection())

    print("="*50)

    r = pool1.query_camera()
    pprint(r)

    r = pool1.query_user()
    pprint(r)

    print("OK!")


    # db.update_headcount('table1', 2, int(time.time()*1000))

    # r = db.query_customer_within_memberinfo()
    # pprint(r)


    # r = db.query_track_tbl()
    # print(r)
    #
    # r = db.get_camera_tracks()
    # pprint(r)
    #
    # r = db.get_trajectory('channel1', '1', [time.time()*1000-60*60*24*30*1000, time.time()*1000])
    # pprint(r)

