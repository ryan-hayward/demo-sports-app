from sqlalchemy import create_engine, inspect, text, ForeignKey, Column, String, Integer, Float
from sqlalchemy.ext.declarative import declarative_base
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
import scripts.eligible_players as eligible_players

# Set up a base class
Base = declarative_base()

# Set up a sessionmaker orm queries and inserts
Session = sessionmaker(bind=engine)


'''
Constructor for eligible player objects to be inserted into the eligible_players database

    Attributes are identical to those in the pandas dataframe returned by eligible_players.get_eligible_players
    season ID (str), playerID (str), name (str), position (str), age (int), season (int)
'''
class Eligible_Player(Base):
    # specify target table name
    __tablename__ = 'eligible_players'
    
    # create columns
    seasonID = Column("seasonID", String, primary_key=True)
    playerID = Column("playerID", String)
    name = Column("name", String)
    position = Column("position", String)
    age = Column("age", Integer)
    season = Column("season", Integer)

    def __init__(self, player: tuple):
        # set object attribute names to be the same as the dataframe columns
        self.seasonID = player.seasonID
        self.playerID = player.playerID
        self.name = player.name
        self.position = player.position
        self.age = player.age
        self.season = player.season
    
    def __repr__(self):
        return f"{self.seasonID}, {self.name}, {self.position}, {self.age}, {self.season}"



'''
Method to update OR insert eligible players into the eligible players table.

@TODO currently this is only insert; add insert/update functionality
'''
def upsert_eligible_players(data: pd.DataFrame):
    session = Session()

    for player in data.itertuples():
        eligible_player = Eligible_Player(player)
        session.add(eligible_player)

    session.commit()
    session.close_all()



'''
Drop contents of a table based on the model
'''
def drop_table(model):
    session = Session()
    session.query(model).delete()
    session.commit()
    session.close_all()



'''
Main Method

@TODO add functionality for upsert to eligible players. Build out the game log class. Add functionality to delete
specific lines of data from each table
'''
def main():
    df = eligible_players.get_eligible_players("passing", 2012)[0]
    upsert_eligible_players(df)
    # drop_table(Eligible_Player)



if __name__ == '__main__':
    main()