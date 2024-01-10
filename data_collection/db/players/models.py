from sqlalchemy import ForeignKey, Column, String, Integer, Float, Date, Boolean, Time
from sqlalchemy.ext.declarative import declarative_base

# Set up a base class
Base = declarative_base()



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
        return f"{self.playerID}, {self.birth_year}, {self.first_name}, {self.last_name}"
    


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
    


class Game(Base):
    # target table
    __tablename__ = 'games'

    # general information
    gameID = Column('gameID', String, primary_key=True)
    date = Column('date', Date)
    playoff = Column('playoff', Boolean)
    home_team = Column('home_team', String)
    away_team = Column('away_team', String)
    home_coach = Column('home_coach', String)
    away_coach = Column('away_coach', String)
    home_score = Column('home_score', Integer)
    away_team = Column('away_score', Integer)
    stadium = Column('stadium', String)
    attendance = Column('attendance', Integer)
    # gambling information
    toss_winner = Column('toss_winner', String)
    favored_team = Column('favored_team', String)
    favored_by = Column('favored_by', Float)
    over_under = Column('over_under', Float)
    head_ref = Column('head_ref', String)
    scorigami = Column('scorigami', Boolean)
    # logistical information
    start_time_et = Column('start_time_et', Time)
    week = Column('week', Integer)
    day_of_week = Column('day_of_week', String)
    rest_days = Column('rest_days', Integer)
    miles_traveled = Column('miles_traveled', Float)
    # home statistical information
    home_yds = Column('home_yards', Integer)
    home_pass_yds = Column('home_pass_yds', Integer)
    home_rush_yds = Column('home_rush_yds', Integer)
    home_fds = Column('home_fds', Integer)
    home_tos = Column('home_tos', Integer)
    home_penalties = Column('home_penalties', Integer)
    home_penalty_yds = Column('home_penalty_yds', Integer)
    home_third_down_conv = Column('home_third_down_conv', Integer)
    home_third_down_att = Column('home_third_down_att', Integer)
    home_fourth_down_conv = Column('home_fourth_down_conv', Integer)
    home_fourth_down_att = Column('home_fourth_down_att', Integer)
    home_top = Column('home_top', Time)
    # away statistical information
    away_yds = Column('away_yards', Integer)
    away_pass_yds = Column('away_pass_yds', Integer)
    away_rush_yds = Column('away_rush_yds', Integer)
    away_fds = Column('away_fds', Integer)
    away_tos = Column('away_tos', Integer)
    away_penalties = Column('away_penalties', Integer)
    away_penalty_yds = Column('away_penalty_yds', Integer)
    away_third_down_conv = Column('away_third_down_conv', Integer)
    away_third_down_att = Column('away_third_down_att', Integer)
    away_fourth_down_conv = Column('away_fourth_down_conv', Integer)
    away_fourth_down_att = Column('away_fourth_down_att', Integer)
    away_top = Column('away_top', Time)



class Game_Log(Base):
    # target table
    __tablename__ = 'player_game_logs'

    # create columns (use composite pkey)
    playerID = Column(String, ForeignKey("player_bios.playerID"), primary_key=True)
    gameID = Column(String, ForeignKey("games.gameID"), primary_key=True)
    date = Column('date', Date)
    game = Column('game', Integer)
    # @TODO continue this



'''
utility function to pass declarative base to functions.py
'''
def get_base():
    return Base
'''
class Game_Log(Base):
    # specify target table name
    __tablename__ = 'player_game_log'

    # create columns (from field_player_mapping.csv in metadata)
'''


