from sqlalchemy import ForeignKey, Column, String, Integer
from data_collection.db.models.base import Base

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
        return f"{self.seasonID}, {self.playerID}, {self.name}"