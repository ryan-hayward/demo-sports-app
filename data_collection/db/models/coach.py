from sqlalchemy import Column, String, Integer, Float
from data_collection.db.models.base import Base

class Coach(Base):
    # specify target table name
    __tablename__ = 'coaches'

    # create columns
    coachID = Column("coachID", String, primary_key=True)
    name = Column("name", String)
    start_year = Column("start_year", Integer)
    end_year = Column("end_year", Integer)
    exp = Column("exp", Integer)
    games = Column("games", Integer)
    wins = Column("wins", Integer)
    losses = Column("losses", Integer)
    ties = Column("ties", Integer)
    win_pct = Column("win_pct", Float)
    playoff_exp = Column("playoff_exp", Integer)
    playoff_games = Column("playoff_games", Integer)
    playoff_wins = Column("playoff_wins", Integer)
    playoff_losses = Column("playoff_losses", Integer)
    playoff_win_pct = Column("playoff_win_pct", Float)
    avg_division_finish = Column("avg_division_finish", Float)
    best_division_finish = Column("best_division_finish", Integer)
    conference_champs = Column("conference_champs", Integer)
    world_champs = Column("world_champs", Integer)
    super_bowls = Column("super_bowls", Integer)

    def __init__(self, coach: tuple):
        # set object attribute names to be the same as the dataframe columns
        self.coachID = coach.coachID
        self.name = coach.name
        self.start_year = coach.start_year
        self.end_year = coach.end_year
        self.exp = coach.exp
        self.wins = coach.wins
        self.losses = coach.losses
        self.ties = coach.ties
        self.win_pct = coach.win_pct
        self.playoff_exp = coach.playoff_exp
        self.playoff_games = coach.playoff_games
        self.playoff_wins = coach.playoff_wins
        self.playoff_losses = coach.playoff_losses
        self.playoff_win_pct = coach.playoff_win_pct
        self.avg_division_finish = coach.avg_division_finish
        self.best_division_finish = coach.best_division_finish 
        self.conference_champs = coach.conference_champs
        self.world_champs = coach.world_champs
        self.super_bowls = coach.super_bowls
    
    def __repr__(self):
        return f"{self.coachID}, {self.name}"