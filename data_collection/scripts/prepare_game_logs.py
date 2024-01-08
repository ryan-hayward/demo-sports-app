from eligible_players import eligible_players
from generic_game_log import generic_game_log
import psycopg2 as pg2

con = pg2.connect(
    host='localhost',
    port='5432',
    database='players',
    user='postgres',
    password='Mazomanie43!'
)