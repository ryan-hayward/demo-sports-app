from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, Float
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
# Set up a counter to keep track of requests to web pages
REQUEST_COUNTER = 0


'''
Constructor for eligible player objects to be inserted into the eligible_players database

    Attributes are identical to those in the pandas dataframe returned by eligible_players.get_eligible_players
    season ID (str), playerID (str), name (str), position (str), age (int), season (int)
'''
class Eligible_Player(Base):
    # specify target table name
    __tablename__ = 'eligible_players'
    
    # create columns
    seasonID = Column("seasonID", String, unique=True, primary_key=True)
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
Method to insert new eligible players into the eligible players table.
'''
def insert_eligible_players(data: pd.DataFrame):
    # open session
    session = Session()

    # iterate through eligible player df
    for player in data.itertuples():
        # check if primary key exists already in db
        pk = player.seasonID
        existing_player = session.query(Eligible_Player).filter_by(seasonID=pk).first()
        # if new primary key, insert into table
        if not existing_player:
            eligible_player = Eligible_Player(player)
            session.add(eligible_player)

    # commit changes & close session
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
Method to insert all eligible players
'''
def insert_all_eligible_players():
    prepare_request_file()
    
    # get all player data between 2000-2023
    for i in range (2000, 2024):
        # get eligible QBs
        passers = eligible_players.get_eligible_players("passing", i, REQUEST_COUNTER)
        insert_eligible_players(passers[0]) # pass data frame to be inserted into database
        increment_request_counter(passers[1]) # increment request counter
        # get eligible FLEXs
        field_players = eligible_players.get_eligible_players("scrimmage", i, REQUEST_COUNTER)
        insert_eligible_players(field_players[0]) # pass data frame to be inserted into database
        increment_request_counter(field_players[1]) # increment request counter
        # get eligible Ks
        kickers = eligible_players.get_eligible_players("kicking", i, REQUEST_COUNTER)
        insert_eligible_players(kickers[0]) # pass data frame to be inserted into database
        increment_request_counter(kickers[1])  # increment request counter



def increment_request_counter(request_count: int):
    # load in the global request counter
    global REQUEST_COUNTER 
    # get the previous value
    read_file = open('data_collection/utils/request_counter.txt', 'r')
    prev_value = int(read_file.read())
    read_file.close()
    # generate new value and assign to global counting variable
    REQUEST_COUNTER = prev_value + request_count
    # write new value to file
    write_file = open('data_collection/utils/request_counter.txt', 'w')
    write_file.write(str(REQUEST_COUNTER))
    write_file.close()



def prepare_request_file():
    file = open('data_collection/utils/request_counter.txt', 'w')
    file.write("0")
    file.close()

'''
Main Method

@TODO add functionality for upsert to eligible players. Build out the game log class. Add functionality to delete
specific lines of data from each table
'''
def main():
    # df = eligible_players.get_eligible_players("passing", 2012)[0]
    # insert_eligible_players(df)
    # drop_table(Eligible_Player)
    insert_all_eligible_players()



if __name__ == '__main__':
    main()