from sqlite3 import Error
import sqlite3

connection = sqlite3.connect('./myDictionary')

def sql_connection():
    try:
        cursor = connection.cursor()
        print("Connection is established: Database is created in memory")
    except Error:
        print(Error.__str__())
    try:
        cursor.execute(
            'CREATE TABLE myDictionary('
            'ID identity primary key ,'
            '词条 varchar, '
            '分类 varchar,'
            '词性 varchar, '
            '词频 integer )'
        )
        print('Create table myDictionary successfully!')
    except Error:
        print(Error.__str__())
    finally:
        connection.close()

sql_connection()
