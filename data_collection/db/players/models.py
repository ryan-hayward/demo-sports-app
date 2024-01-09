from sqlalchemy import ForeignKey, Column, String, Integer, Float
from sqlalchemy.ext.declarative import declarative_base

# Set up a base class
Base = declarative_base()

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
    playerID = Column(String, ForeignKey("player_bios.playerID"))
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
Store player biographical information. Get this information by getting unique values from the player_id column of the
Eligible Player table
'''
class Player(Base):
    # specify target table name
    __tablename__ = 'player_bios'

    # create columns
    playerID = Column("playerID", String, unique=True, primary_key=True)
    birth_year = Column("birth_year", Integer)
    first_name = Column("first_name", String)
    last_name = Column("last_name", String)

    def __init__(self, playerID: str, birth_year: int, first_name: str, last_name: str):
        self.playerID = playerID
        self.birth_year = birth_year
        self.first_name = first_name
        self.last_name = last_name

    def __repr__(self):
        return f"{self.playerID}, {self.birth_year}, {self.first_name}, {self.last_namee}"
    

'''
pass declarative base to functions
'''

def get_base():
    return Base
'''
class Game_Log(Base):
    # specify target table name
    __tablename__ = 'player_game_log'

    # create columns (from field_player_mapping.csv in metadata)
'''


