# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Coaches(models.Model):
    coachid = models.CharField(db_column='coachID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(blank=True, null=True)
    start_year = models.IntegerField(blank=True, null=True)
    end_year = models.IntegerField(blank=True, null=True)
    exp = models.IntegerField(blank=True, null=True)
    games = models.IntegerField(blank=True, null=True)
    wins = models.IntegerField(blank=True, null=True)
    losses = models.IntegerField(blank=True, null=True)
    ties = models.IntegerField(blank=True, null=True)
    win_pct = models.FloatField(blank=True, null=True)
    playoff_exp = models.IntegerField(blank=True, null=True)
    playoff_games = models.IntegerField(blank=True, null=True)
    playoff_wins = models.IntegerField(blank=True, null=True)
    playoff_losses = models.IntegerField(blank=True, null=True)
    playoff_win_pct = models.FloatField(blank=True, null=True)
    avg_division_finish = models.FloatField(blank=True, null=True)
    best_division_finish = models.IntegerField(blank=True, null=True)
    conference_champs = models.IntegerField(blank=True, null=True)
    world_champs = models.IntegerField(blank=True, null=True)
    super_bowls = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'coaches'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class EligiblePlayers(models.Model):
    seasonid = models.CharField(db_column='seasonID', primary_key=True)  # Field name made lowercase.
    playerid = models.CharField(db_column='playerID', blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(blank=True, null=True)
    position = models.CharField(blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    season = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'eligible_players'


class GameLinks(models.Model):
    season = models.IntegerField(blank=True, null=True)
    week = models.IntegerField(blank=True, null=True)
    game_link = models.CharField(primary_key=True)
    game_id = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'game_links'


class Games(models.Model):
    gameid = models.CharField(db_column='gameID', primary_key=True)  # Field name made lowercase.
    datetime = models.DateTimeField(blank=True, null=True)
    playoff = models.BooleanField(blank=True, null=True)
    week = models.IntegerField(blank=True, null=True)
    home_team = models.CharField(blank=True, null=True)
    home_team_code = models.CharField(blank=True, null=True)
    away_team = models.CharField(blank=True, null=True)
    away_team_code = models.CharField(blank=True, null=True)
    home_coach = models.CharField(blank=True, null=True)
    away_coach = models.CharField(blank=True, null=True)
    stadium = models.CharField(blank=True, null=True)
    attendance = models.IntegerField(blank=True, null=True)
    h1q_pts = models.IntegerField(blank=True, null=True)
    h2q_pts = models.IntegerField(blank=True, null=True)
    h3q_pts = models.IntegerField(blank=True, null=True)
    h4q_pts = models.IntegerField(blank=True, null=True)
    h_ot_pts = models.IntegerField(blank=True, null=True)
    hfinal_pts = models.IntegerField(blank=True, null=True)
    a1q_pts = models.IntegerField(blank=True, null=True)
    a2q_pts = models.IntegerField(blank=True, null=True)
    a3q_pts = models.IntegerField(blank=True, null=True)
    a4q_pts = models.IntegerField(blank=True, null=True)
    a_ot_pts = models.IntegerField(blank=True, null=True)
    afinal_pts = models.IntegerField(blank=True, null=True)
    toss_winner = models.CharField(blank=True, null=True)
    toss_deferred = models.BooleanField(blank=True, null=True)
    favored_team = models.CharField(blank=True, null=True)
    favored_by = models.FloatField(blank=True, null=True)
    over_under = models.FloatField(blank=True, null=True)
    head_ref = models.CharField(blank=True, null=True)
    total_game_time = models.CharField(blank=True, null=True)
    day_of_week = models.CharField(blank=True, null=True)
    home_yards = models.IntegerField(blank=True, null=True)
    home_pass_att = models.IntegerField(blank=True, null=True)
    home_pass_yds = models.IntegerField(blank=True, null=True)
    home_rush_att = models.IntegerField(blank=True, null=True)
    home_rush_yds = models.IntegerField(blank=True, null=True)
    home_fds = models.IntegerField(blank=True, null=True)
    home_int = models.IntegerField(blank=True, null=True)
    home_fum = models.IntegerField(blank=True, null=True)
    home_fum_lost = models.IntegerField(blank=True, null=True)
    home_penalties = models.IntegerField(blank=True, null=True)
    home_penalty_yds = models.IntegerField(blank=True, null=True)
    home_third_down_conv = models.IntegerField(blank=True, null=True)
    home_third_down_att = models.IntegerField(blank=True, null=True)
    home_fourth_down_conv = models.IntegerField(blank=True, null=True)
    home_fourth_down_att = models.IntegerField(blank=True, null=True)
    home_top = models.CharField(blank=True, null=True)
    away_yards = models.IntegerField(blank=True, null=True)
    away_pass_att = models.IntegerField(blank=True, null=True)
    away_pass_yds = models.IntegerField(blank=True, null=True)
    away_rush_att = models.IntegerField(blank=True, null=True)
    away_rush_yds = models.IntegerField(blank=True, null=True)
    away_fds = models.IntegerField(blank=True, null=True)
    away_int = models.IntegerField(blank=True, null=True)
    away_fum = models.IntegerField(blank=True, null=True)
    away_fum_lost = models.IntegerField(blank=True, null=True)
    away_penalties = models.IntegerField(blank=True, null=True)
    away_penalty_yds = models.IntegerField(blank=True, null=True)
    away_third_down_conv = models.IntegerField(blank=True, null=True)
    away_third_down_att = models.IntegerField(blank=True, null=True)
    away_fourth_down_conv = models.IntegerField(blank=True, null=True)
    away_fourth_down_att = models.IntegerField(blank=True, null=True)
    away_top = models.CharField(blank=True, null=True)
    season = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'games'


class Player(models.Model):
    playerid = models.CharField(db_column='playerID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(blank=True, null=True)
    positions = models.TextField(blank=True, null=True)  # This field type is a guess.
    throws = models.CharField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    weight = models.IntegerField(blank=True, null=True)
    team = models.CharField(blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    birth_region = models.CharField(blank=True, null=True)
    college = models.CharField(blank=True, null=True)
    draft = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'player'


class PlayerGameLogs(models.Model):
    playerid = models.CharField(db_column='playerID', primary_key=True)  # Field name made lowercase. The composite primary key (playerID, gameID) found, that is not supported. The first column is selected.
    gameid = models.CharField(db_column='gameID')  # Field name made lowercase.
    date = models.DateField(blank=True, null=True)
    game = models.IntegerField(blank=True, null=True)
    week = models.IntegerField(blank=True, null=True)
    team = models.CharField(blank=True, null=True)
    game_location = models.CharField(blank=True, null=True)
    opp = models.CharField(blank=True, null=True)
    result = models.CharField(blank=True, null=True)
    team_pts = models.IntegerField(blank=True, null=True)
    opp_pts = models.IntegerField(blank=True, null=True)
    gs = models.BooleanField(blank=True, null=True)
    cmp = models.IntegerField(blank=True, null=True)
    att = models.IntegerField(blank=True, null=True)
    pass_yds = models.IntegerField(blank=True, null=True)
    pass_tds = models.IntegerField(blank=True, null=True)
    ints = models.IntegerField(blank=True, null=True)
    qbr = models.FloatField(blank=True, null=True)
    sacked_qty = models.IntegerField(blank=True, null=True)
    sacked_yds = models.IntegerField(blank=True, null=True)
    rush_att = models.IntegerField(blank=True, null=True)
    rush_yds = models.IntegerField(blank=True, null=True)
    rush_td = models.IntegerField(blank=True, null=True)
    targets = models.IntegerField(blank=True, null=True)
    receptions = models.IntegerField(blank=True, null=True)
    rec_yds = models.IntegerField(blank=True, null=True)
    rec_td = models.IntegerField(blank=True, null=True)
    xp_made = models.IntegerField(blank=True, null=True)
    xp_att = models.IntegerField(blank=True, null=True)
    fg_made = models.IntegerField(blank=True, null=True)
    fg_att = models.IntegerField(blank=True, null=True)
    fumbles = models.IntegerField(blank=True, null=True)
    fumbles_lost = models.IntegerField(blank=True, null=True)
    snap_count = models.IntegerField(blank=True, null=True)
    snap_pct = models.FloatField(blank=True, null=True)
    total_td = models.IntegerField(blank=True, null=True)
    two_pt_cons = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'player_game_logs'
        unique_together = (('playerid', 'gameid'),)
