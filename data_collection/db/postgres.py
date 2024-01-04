import psycopg2
from sqlalchemy import create_engine
from config import config
import sys
sys.path.append('/Users/rchayward/demo-sports-app/data_collection')


import scripts.generic_game_log as game_log

params = config()

print(params)

conn_string = 'postgresql://%s:%s@%s/%s' % (params['user'], params['password'], params['host'], params['database'])

db = create_engine(conn_string)

df = game_log.get_player_game_log("Josh Allen", "QB", 2022)

df.to_sql('player_data', con=db, if_exists='replace', index=False) 

conn = psycopg2.connect(conn_string) 
conn.autocommit = True
cursor = conn.cursor() 
  
sql1 = '''select * from player_data;'''

cursor.execute(sql1) 

for i in cursor.fetchall(): 
    print(i) 
  
# conn.commit() 
conn.close() 


'''
def connect():
    # attempt to establish a connection
    try:
        params = config()
        print('Connencting to PostgreSQL db...')
        con = pg2.connect(**params)

        print(params)

        #create a cursor
        curs = con.cursor()

        print('PostgreSQL db version: ')
        curs.execute('Select version()')
        db_version = curs.fetchone()
        print(db_version)

    except(Exception, pg2.DatabaseError) as error:
        print(error)
    
    finally:
        if con:
            # close cursor and connection
            curs.close()
            con.close()
        print('Database connection terminated')
'''
'''
if __name__ == '__main__':
    connect()
'''

