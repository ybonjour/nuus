import MySQLdb
import sys

class Database:
    def __this__(self):
        self.connection = None

    def connect(self):
        try:
            self.connection = MySQLdb.connect(host='localhost',
                                 user='nuus',
                                 passwd='nuus',
                                 db='nuus',
                                 charset='utf8')
        except MySQLdb.Error, e:
            print "Error " + str(e.args[0]) + ": " + str(e.args[1])
            sys.exit(1)

    def isConnected(self):
        return self.connection is not None
    
    def close(self):
        if self.isConnected():
            self.connection.close()

    def countQuery(self, query, parameters=None):
        if not self.isConnected():
            raise Exception
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, parameters)
            return cursor.rowcount
        finally:
            cursor.close()
    
    def uniqueQuery(self, query, parameters=None):
        if not self.isConnected():
            raise Exception
        
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, parameters)
            if cursor.rowcount != 1: raise Exception("Not exactly one entry selected, by this query")
            row = cursor.fetchone()
            return row
        finally:
            cursor.close()
    
    def uniqueScalarOrZero(self, query, parameters=None):
        if not self.isConnected():
            raise Exception
        
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, parameters)
            if cursor.rowcount != 1: return 0
            row = cursor.fetchone()
            return row[0]
        finally:
            cursor.close()
    
    
    def iterQuery(self, query, parameters=None):
        if not self.isConnected():
            raise Exception
        cursor = self.connection.cursor()
        cursor.execute(query, parameters)
        row = cursor.fetchone()
        try:
            while row!=None:
                yield row
                row = cursor.fetchone()
        finally:
            cursor.close()
        
    def manipulationQuery(self, query, parameters=None):
        if not self.isConnected():
            raise Exception
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, parameters)
        finally:
            cursor.close()
        
    def insertQuery(self, query, parameters=None):
        if not self.isConnected():
            raise Exception
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, parameters)
            return cursor.lastrowid
        finally:
            cursor.close()
    
    def commit(self):
        if not self.isConnected():
            raise Exception
        self.connection.commit()