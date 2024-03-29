from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean
from data_collection.db.models.base import Base

class Game(Base):
    # target table
    __tablename__ = 'games'

    # general information
    gameID = Column(String, primary_key=True)
    datetime = Column('datetime', DateTime)
    playoff = Column('playoff', Boolean)
    week = Column('week', Integer)
    home_team = Column('home_team', String)
    home_team_code = Column('home_team_code', String)
    away_team = Column('away_team', String)
    away_team_code = Column('away_team_code', String)
    home_coach = Column('home_coach', String)
    away_coach = Column('away_coach', String)
    stadium = Column('stadium', String)
    attendance = Column('attendance', Integer)
    # point scoring information
    h1q_pts = Column('h1q_pts', Integer)
    h2q_pts = Column('h2q_pts', Integer)
    h3q_pts = Column('h3q_pts', Integer)
    h4q_pts = Column('h4q_pts', Integer)
    h_ot_pts = Column('h_ot_pts', Integer)
    hfinal_pts = Column('hfinal_pts', Integer)
    a1q_pts = Column('a1q_pts', Integer)
    a2q_pts = Column('a2q_pts', Integer)
    a3q_pts = Column('a3q_pts', Integer)
    a4q_pts = Column('a4q_pts', Integer)
    a_ot_pts = Column('a_ot_pts', Integer)
    afinal_pts = Column('afinal_pts', Integer)
    # gambling information
    toss_winner = Column('toss_winner', String)
    toss_deferred = Column('toss_deferred', Boolean)
    favored_team = Column('favored_team', String)
    favored_by = Column('favored_by', Float)
    over_under = Column('over_under', Float)
    head_ref = Column('head_ref', String)
    total_game_time = Column('total_game_time', String)
    day_of_week = Column('day_of_week', String)
    # home statistical information
    home_yds = Column('home_yards', Integer)
    home_pass_att = Column('home_pass_att', Integer)
    home_pass_yds = Column('home_pass_yds', Integer)
    home_rush_att = Column('home_rush_att', Integer)
    home_rush_yds = Column('home_rush_yds', Integer)
    home_fds = Column('home_fds', Integer)
    home_int = Column('home_int', Integer)
    home_fum = Column('home_fum', Integer)
    home_fum_lost = Column('home_fum_lost', Integer)
    home_penalties = Column('home_penalties', Integer)
    home_penalty_yds = Column('home_penalty_yds', Integer)
    home_third_down_conv = Column('home_third_down_conv', Integer)
    home_third_down_att = Column('home_third_down_att', Integer)
    home_fourth_down_conv = Column('home_fourth_down_conv', Integer)
    home_fourth_down_att = Column('home_fourth_down_att', Integer)
    home_top = Column('home_top', String)
    # away statistical information
    away_yds = Column('away_yards', Integer)
    away_pass_att = Column('away_pass_att', Integer)
    away_pass_yds = Column('away_pass_yds', Integer)
    away_rush_att = Column('away_rush_att', Integer)
    away_rush_yds = Column('away_rush_yds', Integer)
    away_fds = Column('away_fds', Integer)
    away_int = Column('away_int', Integer)
    away_fum = Column('away_fum', Integer)
    away_fum_lost = Column('away_fum_lost', Integer)
    away_penalties = Column('away_penalties', Integer)
    away_penalty_yds = Column('away_penalty_yds', Integer)
    away_third_down_conv = Column('away_third_down_conv', Integer)
    away_third_down_att = Column('away_third_down_att', Integer)
    away_fourth_down_conv = Column('away_fourth_down_conv', Integer)
    away_fourth_down_att = Column('away_fourth_down_att', Integer)
    away_top = Column('away_top', String)
    # forgot this one
    season = Column('season', Integer)

    def __init__(self, game: dict):
        self.gameID = game["gameID"]
        self.datetime = game["datetime_et"]
        self.playoff = game["playoff"]
        self.week = game["week"]
        self.home_team = game["home_team"]
        self.home_team_code = game["home_team_code"]
        self.away_team = game["away_team"]
        self.away_team_code = game["away_team_code"]
        self.home_coach = game["home_coach"]
        self.away_coach = game["away_coach"]
        self.stadium = game["stadium"]
        self.attendance = game["attendance"]
        # scoring information
        self.h1q_pts = game["h1q_pts"]
        self.h2q_pts = game["h2q_pts"]
        self.h3q_pts = game["h3q_pts"]
        self.h4q_pts = game["h4q_pts"]
        self.h_ot_pts = game["h_ot_pts"]
        self.hfinal_pts = game["hfinal_pts"]
        self.a1q_pts = game["a1q_pts"]
        self.a2q_pts = game["a2q_pts"]
        self.a3q_pts = game["a3q_pts"]
        self.a4q_pts = game["a4q_pts"]
        self.a_ot_pts = game["a_ot_pts"]
        self.afinal_pts = game["afinal_pts"]
        # gambling information
        self.toss_winner = game["toss_winner"]
        self.toss_deferred = game["toss_deferred"]
        self.favored_team = game["favored_team"]
        self.favored_by = game["favored_by"]
        self.over_under = game["over_under"]
        self.head_ref = game["head_ref"]
        self.total_game_time = game["total_game_time"]
        self.day_of_week = game["day_of_week"]
        # home statistical information
        self.home_yds = game["home_yds"]
        self.home_pass_att = game["home_pass_att"]
        self.home_pass_yds = game["home_pass_yds"]
        self.home_rush_att = game["home_rush_att"]
        self.home_rush_yds = game["home_rush_yds"]
        self.home_fds = game["home_fds"]
        self.home_int = game["home_int"]
        self.home_fum = game["home_fum"]
        self.home_fum_lost = game["home_fum_lost"]
        self.home_penalties = game["home_penalties"]
        self.home_penalty_yds = game["home_penalty_yds"]
        self.home_third_down_conv = game["home_third_down_conv"]
        self.home_third_down_att = game["home_third_down_att"]
        self.home_fourth_down_conv = game["home_fourth_down_conv"]
        self.home_fourth_down_att = game["home_fourth_down_att"]
        self.home_top = game["home_top"]
        # away statistical information
        self.away_yds = game["away_yds"]
        self.away_pass_att = game["away_pass_att"]
        self.away_pass_yds = game["away_pass_yds"]
        self.away_rush_att = game["away_rush_att"]
        self.away_rush_yds = game["away_rush_yds"]
        self.away_fds = game["away_fds"]
        self.away_int = game["away_int"]
        self.away_fum = game["away_fum"]
        self.away_fum_lost = game["away_fum_lost"]
        self.away_penalties = game["away_penalties"]
        self.away_penalty_yds = game["away_penalty_yds"]
        self.away_third_down_conv = game["away_third_down_conv"]
        self.away_third_down_att = game["away_third_down_att"]
        self.away_fourth_down_conv = game["away_fourth_down_conv"]
        self.away_fourth_down_att = game["away_fourth_down_att"]
        self.away_top = game["away_top"]
        # forgot this one because I'm an idiot
        self.season = game["season"]

    def __repr__(self):
        return f"{self.gameID}, {self.week}"