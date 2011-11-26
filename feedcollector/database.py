import MySQLdb

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
            print "Error " + e.args[0] + ": " + e.args[1]
            sys.exit(1)

    def isConnected(self):
        return self.connection != None
    
    def close(self):
        if self.isConnected():
            self.connection.close()

    def countQuery(self, query, parameters=None):
        if not self.isConnected():
            raise Exception
        cursor = self.connection.cursor()
        cursor.execute(query, parameters)
        count = cursor.rowcount
        cursor.close()
        return count
    
    def iterQuery(self, query, parameters=None):
        if not self.isConnected():
            raise Exception()
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
        cursor.execute(query, parameters)
        cursor.close()

    def commit(self):
        if not self.isConnected():
            raise Exception
        self.connection.commit()
