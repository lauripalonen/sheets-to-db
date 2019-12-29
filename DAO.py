import sqlite3
from sqlite3 import Error

class Dao:
    def __init__(self, db_filename):
        self.db_filename = db_filename
    
    def create_connection(self):
        conn = None
        try:
            conn = sqlite3.connect(self.db_filename)
        except Error as e:
            print(e)

        return conn

    def create_table(self, table_name):
        stmt = "CREATE TABLE IF NOT EXISTS {} (id integer PRIMARY KEY AUTOINCREMENT);".format(table_name)        

        conn = self.create_connection()

        try:
            cursor = conn.cursor()
            cursor.execute(stmt)
        except Error as e:
            print(e)
    
        if (conn):
          conn.close

    def create_column(self, table, header):
        stmt = "ALTER TABLE {} ADD {} VARCHAR;".format(table, header)

        conn = self.create_connection()

        try:
            cursor = conn.cursor()
            cursor.execute(stmt)
        except Error as e:
            print(e)
        
        conn.close()

    def insert_values(self, table, columns, values):
        stmt = "INSERT INTO {} ({}) VALUES {};".format(table, columns, values)
        
        conn = self.create_connection()

        try:
          cursor = conn.cursor()
          cursor.execute(stmt)
          conn.commit()
        except Error as e:
          print(e)

        conn.close()
        

