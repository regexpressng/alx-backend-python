#!/usr/bin/python3
import mysql.connector

class DatabaseConnection:
    def __init__(self, host, user, password, database):
        self.conn = mysql.connector.connect(
            host = host,
            user = user,
            password = password,
            database= database
        )


    def __enter__(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM users")
            result = cursor.fetchall()
            return result
        except Exception as e:
            self.exc_type = e

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            print(exc_type)
        print("connection closing")
        self.conn.close()
        
with DatabaseConnection('localhost', 'alx_user', 'asdffdsa', 'ALX_prodev') as resource:
    print(resource)