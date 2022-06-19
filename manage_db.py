from sqlite3 import Error
import sqlite3

def sql_connection(connection):
    try:
        cursor = connection.cursor()
        print("Connection is established: Database is created in memory")
    except Error:
        print('Connection fail.')
    try:
        cursor.execute(
            'CREATE TABLE myDictionary('
            'ID Integer PRIMARY KEY,'
            '词条 varchar, '
            '分类 varchar,'
            '词性 varchar, '
            '词频 integer )'
        )
        print('Create table myDictionary successfully!')
    except Error:
        print('Table myDictionary existed.')
    finally:
        cursor.close()

def sql_insert(con, entries):
    sql = 'INSERT INTO myDictionary(词条, 分类, 词性, 词频) VALUES(?, ?, ?, ?)'
    cursor = con.cursor()
    cursor.execute(sql, entries)
    con.commit()
    print('Insert successfully!')
    cursor.close()

def sql_delete(con, entries):
    sql = 'DELETE FROM myDictionary where 词条 = ?'
    cursor = con.cursor()
    cursor.execute(sql, entries)
    con.commit()
    print('Delete successfully!')
    cursor.close()


def sql_update(con, update_list, entries_list):
    for i in range(len(update_list)):
        sql = 'UPDATE myDictionary set %s=? where 词条=?' % (update_list[i])
        cursor = con.cursor()
        cursor.execute(sql, entries_list[i])
        con.commit()
    print('Update successfully!')
    cursor.close()

def sql_select(con, condition_key, condition_value):
    sql = 'SELECT * FROM myDictionary where %s = ?' % (condition_key)
    cursor = con.cursor()
    cursor.execute(sql, condition_value)
    print(cursor.fetchall())
    cursor.close()


if __name__ == '__main__':
    connection = sqlite3.connect('./myDictionary.sqlite3')
    sql_connection(connection)
    # 测试增加条目
    # entry = ('中国', 'diming', 'N', 123)
    # entry2 = ('雪糕', 'food', 'N', 64)
    # sql_insert(connection, entry)
    # # 测试删除条目
    # entry3 = ('中国',)
    # entry4 = ('雪糕',)
    # sql_delete(connection, entry3)
    # sql_delete(connection, entry4)
    # # 测试修改条目
    # update_list = ['词性', '词频']
    # entry5_list = [('N', '雪糕'), (63, '雪糕')]
    # sql_update(connection, update_list, entry5_list)
    # # 测试查找条目
    # sql_select(connection, '词条', ('中国',))
    connection.close()
