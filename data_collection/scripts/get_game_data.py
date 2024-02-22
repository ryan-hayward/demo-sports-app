from bs4 import BeautifulSoup, Comment
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
        'datetime_et': '', 
        'playoff': False, 
        'week': '', 
        'home_team': '', #
        'home_team_code': '', #!
        'away_team': '', #
        'away_team_code': '', #!
        'home_coach': '', #
        'away_coach': '', #
        'stadium': '', #
        'attendance': '', #
        'h1q_pts': 0, #
        'h2q_pts': 0, #
        'h3q_pts': 0, #
        'h4q_pts': 0, #
        'h_ot_pts': 0, #!
        'hfinal_pts': 0, #!
        'a1q_pts': 0, #
        'a2q_pts': 0, #
        'a3q_pts': 0, #
        'a4q_pts': 0, #
        'a_ot_pts': 0, #!
        'afinal_pts': 0, #!
        'toss_winner': '', #
        'toss_deferred': False, #!
        'favored_team': '', #
        'favored_by': '', #
        'over_under': '', #
        'head_ref': '', #
        'total_game_time': '', #!
        'day_of_week': '', #
        'home_yds': '', #
        'home_pass_att': '', #!
        'home_pass_yds': '', #
        'home_rush_att': '', #!
        'home_rush_yds': '', #
        'home_fds': '', #
        'home_int': '', #!
        'home_fum': '', #!
        'home_fum_lost': '', #!
        'home_penalties': '', #
        'home_penalty_yds': '', #
        'home_third_down_conv': '', #
        'home_third_down_att': '', #
        'home_fourth_down_conv': '', #
        'home_fourth_down_att': '', #
        'home_top': '', #
        'away_yds': '', #
        'away_pass_att': '', #!
        'away_pass_yds': '', #
        'away_rush_att': '', #!
        'away_rush_yds': '', #
        'away_fds': '', #
        'away_int': '', #!
        'away_fum': '', #!
        'away_fum_lost': '', #!
        'away_penalties': '', #
        'away_penalty_yds': '', #
        'away_third_down_conv': '', #
        'away_third_down_att': '', #
        'away_fourth_down_conv': '', #
        'away_fourth_down_att': '', #
        'away_top': '' #
    }

    # get soup and find non-content wrapped elems
    soup = get_soup(game_url)
    game = get_week_and_playoff(soup, game)

    # get metadata elements
    meta = soup.find("div", {"class": "scorebox"})
    game = add_meta_elems(meta, game)

    # get quarterly score
    box_score = soup.find("div", {"class": "linescore_wrap"})
    game = add_quarterly_score(box_score, game)

    # Add game stats by targeting the first content grid
    game_info = soup.find("div", {"class": "content_grid"})
    game = add_game_info(game_info, game)

    game_stats = soup.find("div", {"id": "all_team_stats"})
    game = add_game_stats(game_stats, game)

    print(game)
    return game



def get_week_and_playoff(soup: BeautifulSoup, game: dict) -> dict:
    week_tag = get_comment_tags(soup.find("div", {"id": "all_other_scores"}))
    week_str_list = week_tag.find("h2").text.split(' ')
    week = week_str_list[-1]
    if week == "Playoffs":
        game['playoff'] = True
        game['week'] = 99
    else:
        game['week'] = week
    
    return game


    
'''
Done for now. Gets game data from the div tagged "scorebox"
'''
def add_meta_elems(meta: BeautifulSoup, game: dict) -> dict:
    # get the home team ID
    teams = meta.find_all("a", href=lambda href: href and href.startswith("/teams/"))

    # if exactly two teams cannot be found, raise an exception
    if len(teams) != 2:
        raise Exception("Invalid amount of teams found. Expected 2, found %." % len(teams))
    
    # trim first 7 characters from href to get team abbreviations
    game['away_team'] = teams[0].text
    game['away_team_code'] = teams[0]['href'][7:10]
    game['home_team'] = teams[1].text
    game['home_team_code'] = teams[1]['href'][7:10]

    # get coaches
    coaches = meta.find_all("a", href=lambda href: href and href.startswith("/coaches/"))

    # if exactly two teams cannot be found, raise an exception
    if len(coaches) != 2:
        raise Exception("Invalid amount of coaches found. Expected 2, found %." % len(coaches))
    
    # trim first 7 characters from href to get team abbreviations
    game['away_coach'] = coaches[0]['href'].replace('/coaches/', '').replace('.htm', '')
    game['home_coach'] = coaches[1]['href'].replace('/coaches/', '').replace('.htm', '')

    # get metadata sub div
    metadata = meta.find_all("div", {'class': 'scorebox_meta'})[0]
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



def add_quarterly_score(box_score: BeautifulSoup, game: dict) -> dict:
    # get relevaant table cells
    score_table = box_score.find('tbody').find_all('td')

    q_scores = []
    for cell in score_table:
        # ignore cells that contain non-text information
        if cell.find("div"):
            continue
        else:
            q_scores.append(cell.text)
    
    # get location of home and away within the array
    a_index = q_scores.index(game['away_team'])
    h_index = q_scores.index(game['home_team'])
    away_scores = (q_scores[a_index + 1:h_index]) #ignore team name
    home_scores = (q_scores[h_index + 1:]) #ignore team name

    # catch error for too few quarters
    if len(away_scores) < 5:
        raise Exception("Less quarters than expected.")
    # add regular scores
    game['h1q_pts'] = int(home_scores[0])
    game['h2q_pts'] = int(home_scores[1])
    game['h3q_pts'] = int(home_scores[2])
    game['h4q_pts'] = int(home_scores[3])
    game['a1q_pts'] = int(away_scores[0])
    game['a2q_pts'] = int(away_scores[1])
    game['a3q_pts'] = int(away_scores[2])
    game['a4q_pts'] = int(away_scores[3])

    # add finals for non-OT games
    if len(away_scores) == 5:
        game['h_ot_pts'] = 0
        game['hfinal_pts'] = int(home_scores[4])
        game['a_ot_pts'] = 0
        game['afinal_pts'] = int(away_scores[4])
    # OT Games
    else:
        # get OTs
        for i in range(4, len(away_scores) - 1):
            game['h_ot_pts'] = game['h_ot_pts'] + int(home_scores[i])
            game['a_ot_pts'] = game['a_ot_pts'] + int(away_scores[i])
        # get final PTs
        game['hfinal_pts'] = int(home_scores[len(home_scores) - 1])
        game['afinal_pts'] = int(away_scores[len(away_scores) - 1])

    return game



def add_game_info(game_info: BeautifulSoup, game: dict) -> dict:
    # get the betting stats from the first table
    betting_stats = game_info.find("div", {"id": "all_game_info"})
    betting_table = get_comment_tags(betting_stats)
    # get the table rows, omitting the header
    table_rows = betting_table.find_all('tr')[1:]
    # iterate through rows, identify rows that have data in them, and add them to the game dicts
    for row in table_rows:
        key = row.find("th").text
        value  = row.find("td").text

        # use key to find correct game attribute to write to. Insert value
        if key == "Won Toss":
            toss_array = value.split(" ")
            game['toss_winner'] = toss_array[0]
            if len(toss_array) == 2:
                game['toss_deferred'] = True
        elif key == "Vegas Line":
            spread_array = value.split('-')
            # only write vegas lines when a team is favored (i.e. ignore pickems if they exist)
            if len(spread_array) == 2:
                game['favored_team'] = spread_array[0].strip()
                game['favored_by'] = spread_array[1]
        elif key == "Over/Under":
            ou_array = value.split(' ')
            # ignore (over/under)
            game['over_under'] = ou_array[0]
        # @TODO could add in surface and roof variables here, also could shift collection or att and duration to here
    
    # get head ref (IF AVAILABLE)
    officials = game_info.find("div", {"id": "all_officials"})
    if(officials):
        official_table = get_comment_tags(officials)
        # get the table rows, omitting the header
        o_table_rows = official_table.find_all('tr')[1:]
        for row in o_table_rows:
            key = row.find("th").text
            value  = row.find("td").text
            if key == "Referee":
                game['head_ref'] = value
                break
            # @TODO could add additional referee info here
        return game
    else:
        return game



'''
Add total stats for each team to the game dictionary
'''
def add_game_stats(game_stats: BeautifulSoup, game: dict) -> dict:
    stat_table = get_comment_tags(game_stats)
    table_rows = stat_table.find_all('tr')[1:] #omit header row, get table rows
    # insert data
    for row in table_rows:
        # find row header
        key = row.find("th").text
        # find home and away values
        aval = row.find("td", {"data-stat": 'vis_stat'}).text
        hval = row.find("td", {"data-stat": 'vis_stat'}).text

        # use key to find correct game attribute to write to. Insert value
        if key == "First Downs":
            game['home_fds'] = hval
            game['away_fds'] = aval
        elif key == "Rush-Yds-TDs":
            game['home_rush_att'] = hval.split('-')[0]
            game['home_rush_yds'] = hval.split('-')[1]
            game['away_rush_att'] = aval.split('-')[0]
            game['away_rush_yds'] = aval.split('-')[1]
        elif key == "Cmp-Att-Yd-TD-INT":
            game['home_pass_att'] = hval.split('-')[1]
            game['home_pass_yds'] = hval.split('-')[2]
            game['home_int'] = hval.split('-')[4]
            game['away_pass_att'] = aval.split('-')[1]
            game['away_pass_yds'] = aval.split('-')[2]
            game['away_int'] = aval.split('-')[4]
        elif key == "Total Yards":
            game['home_yds'] = hval
            game['away_yds'] = aval
        elif key == "Fumbles-Lost":
            game['home_fum'] = hval.split('-')[0]
            game['home_fum_lost'] = hval.split('-')[1]
            game['away_fum'] = aval.split('-')[0]
            game['away_fum_lost'] = aval.split('-')[1]
        elif key == "Penalties-Yards":
            game['home_penalties'] = hval.split('-')[0]
            game['home_penalty_yds'] = hval.split('-')[1]
            game['away_penalties'] = aval.split('-')[0]
            game['away_penalty_yds'] = aval.split('-')[1]
        elif key == "Third Down Conv.":
            game['home_third_down_conv'] = hval.split('-')[0]
            game['home_third_down_att'] = hval.split('-')[1]
            game['away_third_down_conv'] = aval.split('-')[0]
            game['away_third_down_att'] = aval.split('-')[1]
        elif key == "Fourth Down Conv.":
            game['home_fourth_down_conv'] = hval.split('-')[0]
            game['home_fourth_down_att'] = hval.split('-')[1]
            game['away_fourth_down_conv'] = aval.split('-')[0]
            game['away_fourth_down_att'] = aval.split('-')[1]
        elif key == "Time of Possession":
            game['home_top'] = hval
            game['away_top'] = aval

    return game
        


'''
Extracts the first comment from a bs4 object, return comments as list of bs4 tag objects. Need
to make sure to submit a bs4 tag with only one commeent
'''
def get_comment_tags(soup: BeautifulSoup) -> list:
    comment = soup.find(string=lambda text: isinstance(text, Comment))
    return BeautifulSoup(comment.extract(), 'html.parser')



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
    get_game_data('https://www.pro-football-reference.com/boxscores/198701030cle.htm')



if __name__ == '__main__':
    main()