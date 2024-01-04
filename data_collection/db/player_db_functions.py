from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pandas as pd

# Set up the engine, which provides access to the DB
from db_config import config
params = config()
connection_url = 'postgresql://%s:%s@%s/%s' % (params['user'], params['password'], params['host'], params['database'])
engine = create_engine(connection_url, echo=True)

# add parent directory to sys.path and import package from sibling module
import sys
sys.path.append('./data_collection')
import scripts.generic_game_log as game_log

# Set up a sessionmaker orm queries and inserts
Session = sessionmaker(bind=engine)

'''
Function accepts a player's game log for a given season and inserts/updates (upserts) the log into the database
that is specified in the db_config.py file

    Args:
        game_log (Pandas Dataframe): a log of player games for a given season

    Returns:
        0 for successful upsert, -1 for failure
'''
def upsert_player_game_log(data: pd.DataFrame):
    # establish a new connection to the database
    with engine.connect() as conn:
        data.to_sql('player_data', con=conn, if_exists='append', index=False)
        conn.commit()
    conn.close()


def main():
    df = game_log.get_player_game_log("Josh Allen", "QB", 2018)
    upsert_player_game_log(df)


if __name__ == '__main__':
    main()