import sys
import scripts.generic_game_log as game_log

'''
The second argument (sys.argv[1]) is designed to contain the indicator for which method we would like to call
KEY BELOW
"gameLog" == Get Player Game Log
'''

if sys.argv[1] == "gameLog":
    name = sys.argv[2]
    position = sys.argv[3]
    year = int(sys.argv[4])  #MUST typecast year
    print(game_log.get_player_game_log(name, position, year).to_html)
    
sys.stdout.flush()