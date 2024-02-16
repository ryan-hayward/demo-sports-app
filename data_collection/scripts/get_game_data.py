from bs4 import BeautifulSoup
import time, requests, sys

# append path to database directory here, as we will be accessing a DB model to write data into
sys.path.append('./data_collection')
from db.players.models import Game




def get_game_data(game_url: str):
    # declare game data object
    game = {
        'gameID',
        'date',
        'playoff',
        'home_team',
        'away_team',
        'home_coach',
        'away_coach',
        'stadium',
        'attendance',
        'h1q_pts',
        'h2q_pts',
        'h3q_pts',
        'h4q_pts',
        'a1q_pts',
        'a2q_pts',
        'a3q_pts',
        'a4q_pts',
        'toss_winner',
        'favored_team',
        'favored_by',
        'over_under',
        'head_ref',
        'scorigami',
        'start_time_et',
        'week',
        'day_of_week',
        'rest_days',
        'miles_traveled',
        'temp_f',
        'wind_chill_f',
        'humidity',
        'wind_speed',
        'home_yds',
        'home_pass_yds',
        'home_rush_yds',
        'home_fds',
        'home_tos',
        'home_penalties',
        'home_penalty_yds',
        'home_third_down_conv',
        'home_third_down_att',
        'home_fourth_down_conv',
        'home_fourth_down_att',
        'home_top',
        'away_yds',
        'away_pass_yds',
        'away_rush_yds',
        'away_fds',
        'away_tos',
        'away_penalties',
        'away_penalty_yds',
        'away_third_down_conv',
        'away_third_down_att',
        'away_fourth_down_conv',
        'away_fourth_down_att',
        'away_top'
    }
    


'''
A helper method to make requests to a webpage for HTML and convert the HTML to a Beautiful Soup object.
A counter has been included to track the # of requests made in a given run

    Args:
        request_url (str): address of page we would like to scrape
    
    Returns:
        BeautifulSoup object representing parsed html
    
    @NOTE I have added sleep() in order to prevent session locking from PFR. These limitations are put in
    to maintain site performance.
'''
def get_soup(request_url: str) -> BeautifulSoup:
    global REQUEST_COUNTER
    # if request counter is already at 20, sleep program for sixty seconds
    if REQUEST_COUNTER >= 20:
        print("Maximum requests per minute reached, now sleeping program for sixty seconds.")
        reset_request_counter() # reset request counting file
        for i in range(60, 0, -1):
            time.sleep(1)
            print(i)
        REQUEST_COUNTER = 0
    # store response from request
    response = requests.get(request_url)
    # update the request counter
    REQUEST_COUNTER += 1
    # return soup
    return BeautifulSoup(response.text, 'html.parser')



'''
Reset the stored request counter to zero
'''
def reset_request_counter():
    file = open("data_collection/utils/request_counter.txt", "w")
    file.write("0")
    file.close()



def main():
    get_game_data('https://www.pro-football-reference.com/boxscores/202309070kan.htm')



if __name__ == '__main__':
    main()