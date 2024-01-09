from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from player_db_models import Eligible_Player
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

# Set up a sessionmaker orm queries and inserts
Session = sessionmaker(bind=engine)
# Set up a counter to keep track of requests to web pages
REQUEST_COUNTER = 0


##### ELIGIBLE PLAYER TABLE MODIFICATIONS #####

'''
Function to insert a set of new eligible players into thee eligible_players table

    Params:
        data (pd.df): dataframe of eligible stat accumulators for a given season as defined in
        scripts/eligible_players.py

    Returns:
        N/A; function inserts players into the appropriate db table using a session
        @TODO add error handling and tracking as a return
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
Function that inserts all eligible QBs, RBs, FBs, WRs, TEs, and Ks into the eligible_players database over
a defined stretch of time

    Params:
        start_year (int): year to start looking for stat accumulators
        end_year (int): year to end looking for stat accumulators
    
    Returns:
        N/A; function uses insert_eligible_players to insert passers, scrimmage yard accumulators, and kickers
        into the database on a yearly basis.
        @TODO add error handling/tracking as the return
'''
def insert_all_eligible_players(start_year: int, end_year: int):
    # set request tracking file to zero
    prepare_request_file()
    
    # get all player data between start and end year (end year inclusive)
    for i in range (start_year, end_year + 1):
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



##### REQUEST TRACKING HELPER FUNCTIONS #####

'''
Function to increment the request counter (stored in a text file) by the amount of requests as received from
any script. Necessary to prevent sending too many requests to a given host, which could result in suspension.
'''
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


'''
Function wipes any pre-existing value out of the request tracking file, setting the file equal to zero.
Called prior to running any insert_all() type script to ensure that the base request amount is set to zero.
'''
def prepare_request_file():
    file = open('data_collection/utils/request_counter.txt', 'w')
    file.write("0")
    file.close()



##### DATABASE UTILITY FUNCTIONS #####
    
'''
Drop contents of a given table

    Params:
        model: name of model (as specified in player_db_models). Models correspond 1-to-1 with
        db tables, so equivalent of passing a db name, essentially.
    
    Returns:
        N/A; simply opens a session, drops the appropriate table, and closes the session
        @TODO add error tracking/handling in return
'''
def drop_table(model):
    session = Session()
    session.query(model).delete()
    session.commit()
    session.close_all()



##### MAIN #####

'''
Main Method

@TODO add functionality for upsert to eligible players. Build out the game log class. Add functionality to delete
specific lines of data from each table
'''
def main():
    # insert_all_eligible_players()
    print("Do testing here")



if __name__ == '__main__':
    main()