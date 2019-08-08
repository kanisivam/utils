import pymysql

"""
to connect to db through pymysql
"""

DB_NAME= 'testdb'
TABLE_NAME="test_table"
TIMESTAMP = '%Y-%m-%d %H:%M:%S'

def connect_db(db_name):
    """ Opens and establishes the connection to the database testdb"""
    host, user, password = 'X.X.X.X','user','password'
    return pymysql.connect(host=host, port=3306, user=user, passwd=password, db=db_name, autocommit=True)


def execute_query(query,db_name,fetch=True,do_commit=False):
    """
    execute query in db.
    :param query:  str
    :param db_name:  dbname
    :param fetch: bool to indicate select query
    :param do_commit: bool to indicate commit
    :return:
    """
    try:
        cursor = connect_db(db_name).cursor()
        cursor.execute(query)
        if fetch:
            result = cursor.fetchall()
            cursor.close()
            return result
        elif do_commit:
                cursor.execute("COMMIT")
                cursor.close()
    except Exception as e:
        print(e)


if False and __name__ == '__main__':
    results = execute_query('select * from test_table','testdb',True,False)
