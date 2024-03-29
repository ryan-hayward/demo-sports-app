from sqlalchemy import Column, String, Integer, Boolean, Float, Date
from data_collection.db.models.base import Base

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