import psycopg2 as pg2
from config import config

def connect():
    con = None
    # attempt to establish a connection
    try:
        params = config()
        print('Connencting to PostgreSQL db...')
        con = pg2.connect(**params)

        #create a cursor
        curs = con.cursor()
        print('PostgreSQL db version: ')
        curs.execute('Select version()')
        db_version = curs.fetchone()
        print(db_version)
        curs.close()

    except(Exception, pg2.DatabaseError) as error:
        print(error)
    
    finally:
        if con is not None:
            con.close()
        print('Database connection terminated')


if __name__ == '__main__':
    connect()

