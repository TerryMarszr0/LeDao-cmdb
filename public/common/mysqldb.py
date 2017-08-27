#-*- coding:utf-8 -*-
import MySQLdb

class DBOP():

    def __init__(self, host, user, password, dbname, port=3306):
        self.db = MySQLdb.connect(host, user, password, dbname, port)
        self.db.set_character_set('utf8')


    def getList(self, sql, *args):
        cursor = self.db.cursor()
        try:
            cursor.execute(sql, args)
            results = cursor.fetchall()
            cursor.close()
            return results
        except Exception as ex:
            print str(ex)
            cursor.close()
            return []

    def getOne(self, sql, *args):
        cursor = self.db.cursor()
        try:
            cursor.execute(sql, args)
            results = cursor.fetchall()
            cursor.close()
            if len(results) <= 0:
                return False
            return results[0]
        except Exception as ex:
            print str(ex)
            cursor.close()
            return False

    def add(self, sql, *args):
        cursor = self.db.cursor()
        try:
            cursor.execute(sql, args)
            lastid = cursor.lastrowid
            cursor.close()
            return lastid
        except Exception as ex:
            print str(ex)
            cursor.close()
            return False

    def update(self, sql, *args):
        cursor = self.db.cursor()
        try:
            res = cursor.execute(sql, args)
            cursor.close()
            return res
        except Exception as ex:
            print str(ex)
            cursor.close()
            return False

    def dbhealthcheck(self, sql, *args):
        cursor = self.db.cursor()
        try:
            cursor.execute(sql, args)
            cursor.close()
            return True
        except Exception as ex:
            print str(ex)
            cursor.close()
            return False

    def close(self):
        self.db.close()
