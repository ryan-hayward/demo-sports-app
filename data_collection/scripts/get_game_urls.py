import pandas as pd
from bs4 import BeautifulSoup
import requests
import time
import datetime

REQUEST_COUNTER = 0


'''
Master driving method. Other classes use this.
'''
def get_games(season: int, counter: int) -> list:
    # set global counter to accurately reflect passed counter
    global REQUEST_COUNTER
    REQUEST_COUNTER = counter

    # check if season is valid
    if not 1970 <= season <= int(datetime.date.today().year):
        raise Exception('Year must be 1970 or later.')
    
    # establish base url
    base_url = 'https://www.pro-football-reference.com/years/%s' % str(season)
    
    # get the structure of the season given the value passed for season
    week_list = get_week_list(base_url, season)
    
    # get a df of game links for the entire season
    game_links = get_game_links(season, week_list)
    return [game_links, REQUEST_COUNTER]

'''
Return the list of valid week hrefs
'''
def get_week_list(base_url: str, season: int) -> list:
    url = 'https://www.pro-football-reference.com/years/%s' % str(season)
    soup = get_soup(url)
    href_list = [] # list of links
    target_week = soup.find("a", string="Week 1") # find the first week
    href_list.append(target_week.get('href')) # append first week
    # loop until the super bowl
    while target_week.text != "Super Bowl":
        target_week = target_week.find_next().find_next() # chain next to avoid duplicates
        href_list.append(target_week.get('href')) # append next week
    
    return href_list # return the week list



'''
Get the game links from all weeks in a given season and adds them to a dataframe.
'''
def get_game_links(season: int, week_list: list) -> pd.DataFrame:
    # set up dataframe structure
    data = {
        'season': [],
        'week': [],
        'link': []
    }
    base_pfr_url = 'https://www.pro-football-reference.com'       

    # loop through weeks starting at 1
    for week in week_list:
        # isolate week number from rest of string
        week_num = week.split('_')[1].replace('.htm', '')
        # get soup based on week
        soup = get_soup(base_pfr_url + week)
        # find all game summaries
        summaries = soup.find("div", class_="game_summaries")
        game_links = summaries.find_all("td", attrs={"class": "right gamelink"})
        # iterate through all games
        for game in game_links:
            print(game)
            game_ext = game.find('a').get('href')
            data['season'].append(season)
            data['week'].append(week_num)
            data['link'].append(base_pfr_url + game_ext)
    # send complete dataframe back
    return pd.DataFrame(data=data)

        
'''
Standard method used across scripts in the program
@TODO centralize get_soup and request counter as a separate module, as they are used
across the scripts
'''
def get_soup(request_url: str) -> BeautifulSoup:
    global REQUEST_COUNTER
    # if request counter is already at 20, sleep program for sixty seconds
    if REQUEST_COUNTER >= 19:
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
    df = get_games(1983, 0)
    # df.to_csv('data_collection/data/test/test_games.csv', sep='\t', index=False)

if __name__ == '__main__':
    main()