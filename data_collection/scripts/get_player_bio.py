import pandas as pd  # type: ignore
import re
from bs4 import BeautifulSoup
from get_soup import get_soup
from datetime import datetime

VALID_POSITIONS = ['QB', 'RB', 'FB', 'WR', 'TE', 'K']

def get_player_bio(player: str, position: str) -> dict:
    # position arg must be formatted properly
    if position not in VALID_POSITIONS:
        raise Exception('Invalid position: "position" must be "QB", "RB", "FB", "WR", "TE", or "K"')

    # find href of player
    # href = get_href(player, position)
    player_list_soup = get_player_list(player)
    player_soup = get_href(player, position, player_list_soup)
    
    return get_bio(player, player_soup)


# helper function that gets the player's href
def get_href(player: str, position: str, player_list: BeautifulSoup) -> BeautifulSoup:
    players = player_list.find('div', id='div_players').find_all('p')
    for p in players:
        if player in p.text and position in p.text:
            return get_soup('https://www.pro-football-reference.com' + p.find('a').get('href'))
    raise Exception('Cannot find a ' + position + ' named ' + player)


# request BS4 object based on player last name initial
def get_player_list(name: str) -> BeautifulSoup:
    last_initial = name.split(' ')[1][0]
    url = 'https://www.pro-football-reference.com/players/%s/' % (last_initial)
    return get_soup(url)


def get_bio(player_name: str, player_soup: BeautifulSoup) -> dict:
    # set team to retired by default
    bio = {
        'name': player_name,
        'positions': [],
        'throws': '',
        'height': '',
        'weight': '',
        'team': 'Retired',
        'dob': '',
        'birth_region': '',
        'college': '',
        'draft': {
            'team': '',
            'round': '',
            'year': '',
            'overall': ''
        }
    }

    metadata = player_soup.find('div', id='meta').find_all('p')
    for attr in metadata:
        label = attr.find('strong')
        content = attr.text
        # if the content has a label, use label to assign content to the correct k,v in bio
        if label:
            # get position
            if label.text == 'Position':
                bio['positions'], bio['throws'] = get_positions(content)
                continue
            # get three char team
            if label.text == 'Team':
                team_link = attr.find('a', href=True)
                if team_link:
                    bio['team'] = team_link['href'][7:10]
                    continue
            # get date of birth and birth state
            if label.text == 'Born:':
                bio['dob'], bio['birth_region'] = get_birth_data(content)
            # get college
            if label.text == 'College':
                if attr.find('a'):
                    bio['college'] = attr.find('a').text
            # get draft data
            if label.text == 'Draft':
                draft_meta = attr.find_all('a')
                bio['draft']['team'] = draft_meta[0]['href'][7:10]
                bio['draft']['year'] = draft_meta[0]['href'][11:15]
                draft_position = content.split('in the')[1].split('of the')[0].strip()
                round_overall = re.findall(r'\d+', draft_position)
                bio['draft']['round'] = round_overall[0]
                bio['draft']['overall'] = round_overall[1]
        else:
            # get height and weight
            hw_array = content.split('\xa0')
            [feet, inches] = hw_array[0].split('-')
            bio['height'] = (int(feet) * 12) + int(inches.replace(',', ''))
            bio['weight'] = hw_array[1].replace('lb', '')
    
    return bio


'''
Helper method to get the positions a player has played as well as their throwing arm if they are a quarterback
'''
def get_positions(content: str) -> list:
    pos_str, throws_str = None, None
    # split off throws if applicable
    if 'Throws:' in content:
        pos_str = content.split('Throws:')[0]
        throws_str = content.split('Throws:')[1]
    else:
        pos_str = content
    # split off 'Position:' from actual data
    pos_content = pos_str.split(':')[1]
    # if applicable, split position on hyphen and strip formatting chars
    pos_array = pos_content.replace('\n', '').replace('\t', '').strip().split('-')
    # if QB, populate throws
    throws = ''
    if "QB" in pos_array and throws_str:
        throws = throws_str.replace('\n', '').replace('\t', '').strip()
    # populate positions
    return [pos_array, throws]


def get_birth_data(content: str) -> list:
    birth_arr = content.split('in')
    # return blank values if nothing is present
    if len(birth_arr) == 0:
        return ['', '']
    # format each birth string
    formatted_arr = []
    for s in birth_arr:
        formatted_arr.append(s.replace('\n', '').replace('\t', '').replace('\xa0', '').replace('Born:', '').strip())
    # format birth date string
    dob = datetime.strptime(formatted_arr[0], "%B %d,%Y")
    birthplace = ''
    if len(formatted_arr) > 1:
        birthplace = formatted_arr[1].split(',')[1]
    return [dob, birthplace]


def main():
    get_player_bio("Cordarrelle Patterson", "WR")

if __name__ == '__main__':
    main()