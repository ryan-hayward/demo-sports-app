from bs4 import BeautifulSoup
import time, requests
from datetime import datetime

# declare Request Counter
REQUEST_COUNTER = 0



'''
Function to be utilized as module; takes a game url and returns a dictionary representing game data
'''
def get_game_data(game_url: str) -> dict:
    # declare empty game data dict
    game = {
        'gameID': '',
        'datetime_et': '', #!
        'playoff': '',
        'home_team': '', #
        'away_team': '', #
        'home_coach': '', #
        'away_coach': '', #
        'stadium': '', #
        'attendance': '', #
        'h1q_pts': '',
        'h2q_pts': '',
        'h3q_pts': '',
        'h4q_pts': '',
        'a1q_pts': '',
        'a2q_pts': '',
        'a3q_pts': '',
        'a4q_pts': '',
        'toss_winner': '',
        'favored_team': '',
        'favored_by': '',
        'over_under': '',
        'head_ref': '',
        'scorigami': '',
        'total_game_time': '', #!
        'week': '',
        'day_of_week': '', #
        'rest_days': '',
        'miles_traveled': '',
        'temp_f': '',
        'wind_chill_f': '',
        'humidity': '',
        'wind_speed': '',
        'home_yds': '',
        'home_pass_yds': '',
        'home_rush_yds': '',
        'home_fds': '',
        'home_tos': '',
        'home_penalties': '',
        'home_penalty_yds': '',
        'home_third_down_conv': '',
        'home_third_down_att': '',
        'home_fourth_down_conv': '',
        'home_fourth_down_att': '',
        'home_top': '',
        'away_yds': '',
        'away_pass_yds': '',
        'away_rush_yds': '',
        'away_fds': '',
        'away_tos': '',
        'away_penalties': '',
        'away_penalty_yds': '',
        'away_third_down_conv': '',
        'away_third_down_att': '',
        'away_fourth_down_conv': '',
        'away_fourth_down_att': '',
        'away_top': ''
    }

    soup = get_soup(game_url)

    scorebox = soup.find("div", {"class": "scorebox"})

    game = get_scorebox_elems(scorebox, game)

    print(game)
    
    
'''
Done for now. Gets game data from the div tagged "scorebox"
'''
def get_scorebox_elems(scorebox, game: dict) -> dict:
    # get the home team ID
    teams = scorebox.find_all("a", href=lambda href: href and href.startswith("/teams/"))

    # if exactly two teams cannot be found, raise an exception
    if len(teams) != 2:
        raise Exception("Invalid amount of teams found. Expected 2, found %." % len(teams))
    
    # trim first 7 characters from href to get team abbreviations
    game['away_team'] = teams[0]['href'][7:10]
    game['home_team'] = teams[1]['href'][7:10]

    # get coaches
    coaches = scorebox.find_all("a", href=lambda href: href and href.startswith("/coaches/"))

    # if exactly two teams cannot be found, raise an exception
    if len(coaches) != 2:
        raise Exception("Invalid amount of coaches found. Expected 2, found %." % len(coaches))
    
    # trim first 7 characters from href to get team abbreviations
    game['away_coach'] = coaches[0]['href'].replace('/coaches/', '').replace('.htm', '')
    game['home_coach'] = coaches[1]['href'].replace('/coaches/', '').replace('.htm', '')

    # get metadata sub div
    metadata = scorebox.find_all("div", {'class': 'scorebox_meta'})[0]
    # find all sub divs
    sub_meta = metadata.find_all("div")
    # get date string
    date_str = sub_meta[0].text
    # get day of week
    day_of_week = date_str[0:date_str.find(" ")]
    game['day_of_week'] = day_of_week
    # get date and properly format
    date = date_str.replace(day_of_week, '').strip()
    game['datetime_et'] = datetime.strptime(date, '%b %d, %Y')

    # @TODO add game datetime, stadium, attendance, time of game
    # get list of metadata provided alongside the game and update values as provided
    available_meta = []
    # if we find a strong tag, it is generally data we want
    for div in sub_meta:
        if div.find("strong"):
            available_meta.append(div)

    # iterate through divs with strong tags and insert data as applicable
    for elem in available_meta:
        strong_elem = elem.find("strong")
        if strong_elem.text == "Start Time":
            # add start time to game date time if available
            start_time = strong_elem.next_sibling[2:]
            game_datetime = game['datetime_et'].strftime('%Y-%m-%d') + ' ' + start_time
            game['datetime_et'] = datetime.strptime(game_datetime, '%Y-%m-%d %I:%M%p')
        elif strong_elem.text == "Stadium":
            # update stadium
            game['stadium'] = elem.find("a")['href'].replace('/stadiums/', '').replace('.htm', '')
        elif strong_elem.text == "Attendance":
            # update attendance
            game['attendance'] = int(elem.find("a").text.replace(',', ''))
        elif strong_elem.text == "Time of Game":
            # update total game time
            game['total_game_time'] = strong_elem.next_sibling[2:]
    
    return game



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