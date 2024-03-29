from sqlalchemy import Column, String, Integer
from data_collection.db.models.base import Base

'''
Table of all game links
@TODO add game_id to this table (last n digits minus .htm from link)
'''
class Game_Link(Base):
    # target table
    __tablename__ = 'game_links'
    season = Column("season", Integer)
    week = Column("week", Integer)
    link = Column("game_link", String, primary_key=True)
    game_id = Column("game_id", String)

    def __init__(self, game_link: tuple):
        self.season = game_link.season
        self.week = game_link.week
        self.link = game_link.link
        self.game_id = game_link.game_id

    def __repr__(self):
        return f"{self.season}, {self.week}, {self.link}, {self.game_id}"