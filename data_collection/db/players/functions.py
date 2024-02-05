from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import exists
from models import Eligible_Player, Player, Game_Link, get_base
import pandas as pd

# add parent directory to sys.path and import packages from sibling modules
import sys
sys.path.append('./data_collection')
from db.db_config import config
import scripts.get_game_logs as game_log
import scripts.get_eligible_players as get_eligible_players
import scripts.get_game_urls as get_game_urls

# Set up the engine, which provides access to the DB
params = config()
connection_url = 'postgresql://%s:%s@%s/%s' % (params['user'], params['password'], params['host'], params['database'])
engine = create_engine(connection_url, echo=True)

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
'''
def upsert_eligible_players(data: pd.DataFrame):
    # ensure that target table exists
    create_all_tables()

    # set request tracking file to zero
    prepare_request_file()

    # open session
    session = Session()

    # iterate through eligible player df
    for player in data.itertuples():
        # get unique id (seasonID)
        season_id = player.seasonID
        # check if record exists
        exists = session.query(Eligible_Player).filter_by(seasonID=season_id).first() is not None
        # if it does, update
        if exists:
            session.query(Eligible_Player).filter_by(seasonID=season_id).update({
                'playerID': player.playerID,
                'name': player.name,
                'position': player.position,
                'age': player.age,
                'season': player.season
            })
        # if not, add playerr
        else:
            new_player = Eligible_Player(player)
            session.add(new_player)

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
def upsert_all_eligible_players(start_year: int, end_year: int):
    # ensure that target table exists
    create_all_tables()

    # set request tracking file to zero
    prepare_request_file()
    
    # get all player data between start and end year (end year inclusive)
    for i in range (start_year, end_year + 1):
        # get eligible QBs
        passers = get_eligible_players.get_eligible_players("passing", i, REQUEST_COUNTER)
        upsert_eligible_players(passers[0]) # pass data frame to be inserted into database
        increment_request_counter(passers[1]) # increment request counter
        # get eligible FLEXs
        field_players = get_eligible_players.get_eligible_players("scrimmage", i, REQUEST_COUNTER)
        upsert_eligible_players(field_players[0]) # pass data frame to be inserted into database
        increment_request_counter(field_players[1]) # increment request counter
        # get eligible Ks
        kickers = get_eligible_players.get_eligible_players("kicking", i, REQUEST_COUNTER)
        upsert_eligible_players(kickers[0]) # pass data frame to be inserted into database
        increment_request_counter(kickers[1])  # increment request counter



'''
Deletes a specified player's records in a given time frame
'''
def delete_eligible_player(playerID: str, start_year: int, end_year: int):
    session = Session()
    # drop all records related to a certain player given the start and end year
    for i in range(start_year, end_year + 1):
        session.query(Eligible_Player).filter(
            Eligible_Player.playerID==playerID).filter(
            Eligible_Player.season==i).delete()
        print("Deleted record " + str(playerID) + ' ' + str(i))
    
    session.commit()
    session.close()



'''
Deletes all player records within a given time frame
'''
def delete_all_eligible_players(start_year: int, end_year: int):
    session = Session()
    # drop all records given the start and end year
    for i in range(start_year, end_year + 1):
        session.query(Eligible_Player).where(Eligible_Player.season==i).delete()

    session.commit()
    session.close()



##### PLAYER BIO TABLE MODIFICATIONS
'''
Upserts unique player biographical information into the player_bios table based on the appearance
of unique playerIDs in the Eligible Players table
'''
def upsert_player_bios():
    # ensure that target table exists
    create_all_tables()

    # no need to prepare request file since this is done internally, just open session
    session = Session()

    for player in session.query(Eligible_Player.playerID).distinct():
        # get player unique id
        player_id = player._mapping['playerID']
        # find player for each player ID
        player_record = session.query(Eligible_Player).filter_by(playerID=player_id).first()
        # get birth year
        birth_year = player_id[-2:]
        # get first and last name
        name = player_record.name.split(' ')
        first_name = name[0]
        last_name = name[1]
        # create player object
        player = Player(player_id, birth_year, first_name, last_name)
        # if player already exists in player bios, update. Else, add
        if session.query(Player).filter_by(playerID=player_id):
            session.query(Player).filter_by(playerID=player_id).update({
                'birth_year': birth_year,
                'first_name': first_name,
                'last_name': last_name
            })
        else:
            session.add(player)

    session.commit()
    session.close()



'''
Given a list of player ids, delete records in the player bios database
'''
def delete_player_bios(player_list: list):
    session = Session()

    for player in list:
        session.query(Player).filter_by(playerID=player).delete()
    
    print('player removal complete.')



##### GAME URL TABLE MODIFICATIONS
def upsert_game_urls(data: pd.DataFrame):
    # ensure that target table exists
    create_all_tables()
    # set request tracking file to zero
    prepare_request_file()
    # create session
    session = Session()

    # iterate through game link df
    for game_link in data.itertuples():
        # check if record exists
        exists = session.query(Game_Link).filter_by(link=game_link.link).first() is not None
        # if it does, update
        if exists:
            session.query(Game_Link).filter_by(link=game_link.link).update({
                'season': game_link.season,
                'week': game_link.week,
                'link': game_link.link
            })
        # if not, add playerr
        else:
            new_game_link = Game_Link(game_link)
            session.add(new_game_link)

    # commit changes & close session
    session.commit()
    session.close_all()



def upsert_all_game_urls(start_year: int, end_year: int):
    # ensure that target table exists
    create_all_tables()

    # set request tracking file to zero
    prepare_request_file()
    
    # get all player data between start and end year (end year inclusive)
    for i in range (start_year, end_year + 1):
        # get eligible QBs
        game_urls = get_game_urls.get_games(i, REQUEST_COUNTER)
        upsert_game_urls(game_urls[0]) # pass data frame to be inserted into database
        increment_request_counter(game_urls[1]) # increment request counter



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
Ensure all tables have been set up
'''
def create_all_tables():
    get_base().metadata.create_all(bind=engine)



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


'''
Not currently used but may be used by the drop model method in the future
'''
def table_exists(table):
    # check for the existence of the table
    inspector = inspect(engine)
    if table in inspector.get_table_names():
        return True
    else:
        return False
    


##### MAIN #####

'''
Main Method

@TODO add functionality for upsert to eligible players. Build out the game log class. Add functionality to delete
specific lines of data from each table
'''
def main():
    # upsert_all_eligible_players(2020, 2023)
    # df = get_eligible_players.get_eligible_players("passing", 2023, REQUEST_COUNTER)[0]
    # upsert_eligible_players(df)
    # df = get_game_urls.get_games(2023)[0]
    upsert_all_game_urls(1981, 1990)


if __name__ == '__main__':
    main()