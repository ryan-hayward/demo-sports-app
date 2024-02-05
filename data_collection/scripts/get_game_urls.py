import pandas as pd
from bs4 import BeautifulSoup, Comment
import requests
import time
import datetime

REQUEST_COUNTER = 0


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
    week_count = get_week_count(base_url, season)
    
    # get a df of game links for the entire season
    game_links = get_game_links(base_url, season, week_count)
    return [game_links, REQUEST_COUNTER]

'''
Get the # of weeks for a given season
'''
def get_week_count(base_url: str, season: int) -> int:
    url = 'https://www.pro-football-reference.com/years/%s' % str(season)
    soup = get_soup(url)
    print(soup)
    # look for week contents in comments
    comments = soup.find_all(string=lambda text: isinstance(text, Comment))
    # iterate through comments to find comment regarding weeks
    target_comment = ""
    for c in comments:
        print(c)
        if "div_week_games" in c:
            target_comment = c
            break
    if target_comment == "":
        raise Exception("Cannot find week count.")
    else: # else return number of weeks
        return target_comment.count("</a>")
    


def get_game_links(url: str, season: int, week_count: int) -> pd.DataFrame:
    # set up dataframe structure
    data = {
        'season': [],
        'week': [],
        'link': []
    }
    base_pfr_url = 'https://www.pro-football-reference.com'

    # loop through weeks starting at 1
    for i in range (1, week_count + 1):
        ending = '/week_%s.htm' % i
        soup = get_soup(url + ending)
        summaries = soup.find("div", class_="game_summaries")
        print(summaries)
        game_links = summaries.find_all("td", attrs={"class": "right gamelink"})
        for game in game_links:
            game_ext = game.find('a').get('href')
            data['season'].append(season)
            data['week'].append(i)
            data['link'].append(base_pfr_url + game_ext)
    
    return pd.DataFrame(data=data)

        

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
    df = get_games(1971, 0)
    # df.to_csv('data_collection/data/test/test_games.csv', sep='\t', index=False)

if __name__ == '__main__':
    main()