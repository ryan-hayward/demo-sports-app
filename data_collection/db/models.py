from sqlalchemy import ForeignKey, Column, String, Integer, Float, Date, DateTime, Boolean, Time
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
    playerID = Column("playerID", String, primary_key=True)
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
        return f"{self.seasonID}, {self.playerID}, {self.name}"
    


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



'''
@TODO evaluate if the game information is necessary to include in this table or if it can just be
included in the Game table
'''
class Game_Log(Base):
    # target table
    __tablename__ = 'player_game_logs'

    # create columns (use composite pkey)
    playerID = Column(String, primary_key=True)
    gameID = Column(String, primary_key=True)
    date = Column('date', Date)
    game = Column('game', Integer)
    week = Column('week', Integer)
    team = Column('team', String)
    game_location = Column('game_location', String)
    opp = Column('opp', String)
    result = Column('result', String)
    team_pts = Column('team_pts', Integer)
    opp_pts = Column('opp_pts', Integer)
    start = Column('gs', Boolean) # @TODO change start to True/False at collection
    cmp = Column('cmp', Integer)
    att = Column('att', Integer)
    pass_yds = Column('pass_yds', Integer)
    pass_tds = Column('pass_tds', Integer)
    ints = Column('ints', Integer)
    qbr = Column('qbr', Float)
    sacked_qty = Column('sacked_qty', Integer)
    sacked_yds = Column('sacked_yds', Integer)
    rush_att = Column('rush_att', Integer)
    rush_yds = Column('rush_yds', Integer)
    rush_td = Column('rush_td', Integer)
    targets = Column('targets', Integer)
    receptions = Column('receptions', Integer)
    rec_yds = Column('rec_yds', Integer)
    rec_td = Column('rec_td', Integer)
    xp_made = Column('xp_made', Integer)
    xp_att = Column('xp_att', Integer)
    fg_made = Column('fg_made', Integer)
    fg_att = Column('fg_att', Integer)
    fumbles = Column('fumbles', Integer)
    fumbles_lost = Column('fumbles_lost', Integer)
    snap_count = Column('snap_count', Integer)
    snap_pct = Column('snap_pct', Float)
    total_td = Column('total_td', Integer)
    two_pt_cons = Column('two_pt_cons', Integer)

    def __init__(self, game_log: tuple):
        self.playerID = game_log.playerID
        self.gameID = game_log.gameID
        self.date = game_log.date
        self.game = game_log.game
        self.week = game_log.week
        self.team = game_log.team
        self.game_location = game_log.game_location
        self.opp = game_log.opp
        self.result = game_log.result
        self.team_pts = game_log.team_pts
        self.opp_pts = game_log.opp_pts
        self.start = game_log.start
        self.cmp = game_log.cmp
        self.att = game_log.att
        self.pass_yds = game_log.pass_yds
        self.pass_tds = game_log.pass_tds
        self.ints = game_log.ints 
        self.qbr = game_log.qbr
        self.sacked_qty = game_log.sacked_qty
        self.sacked_yds = game_log.sacked_yds
        self.rush_att = game_log.rush_att
        self.rush_yds = game_log.rush_yds
        self.rush_td = game_log.rush_td
        self.targets = game_log.targets
        self.receptions = game_log.receptions
        self.rec_yds = game_log.rec_yds
        self.rec_td = game_log.rec_td
        self.xp_made = game_log.xp_made
        self.xp_att = game_log.xp_att 
        self.fg_made = game_log.fg_made
        self.fg_att = game_log.fg_att
        self.fumbles = game_log.fumbles
        self.fumbles_lost = game_log.fumbles_lost
        self.snap_count = game_log.snap_count
        self.snap_pct = game_log.snap_pct
        self.total_td = game_log.total_td
        self.two_pt_cons = game_log.two_pt_cons

    def __repr__(self):
        return f"{self.playerID}, {self.gameID}"



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



'''
utility function to pass declarative base to functions.py
'''
def get_base():
    return Base
