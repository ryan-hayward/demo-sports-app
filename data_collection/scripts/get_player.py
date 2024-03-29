import re, os, sys
from bs4 import BeautifulSoup
from datetime import datetime
from requests_ip_rotator import ApiGateway

# add root directory of project to path and get api gateway
sys.path.insert(1, "/".join(os.path.realpath(__file__).split("/")[0:-3]))
from data_collection.utils.api_gateway import create_api_gateway, shutdown_api_gateway
from data_collection.scripts.get_soup import get_soup

VALID_POSITIONS = ['QB', 'RB', 'FB', 'WR', 'TE', 'K']

class Player:
    # note: not assigning position right away as multiple can be added
    def __init__(self, player_name: str, position: str, gateway: ApiGateway):
        # utils
        self.gateway = gateway
        self.initial_position = position
        # data to write to db
        self.name = player_name
        self.positions = []
        self.throws = ''
        self.height = ''
        self.weight = ''
        self.team= 'Retired'
        self.dob = ''
        self.birth_region = ''
        self.college = ''
        self.draft = {
            'team': '',
            'round': '',
            'year': '',
            'overall': ''
        }

    # driver to generate player bio
    def populate_bio(self):
        # position arg must be formatted properly
        if self.initial_position not in VALID_POSITIONS:
            raise Exception('Invalid position: "position" must be "QB", "RB", "FB", "WR", "TE", or "K"')

        # find href of player
        # href = get_href(player, position)
        player_list_soup = self.get_player_list()
        player_soup = self.get_href(player_list_soup)
        # make a call to get player biographical data
        try:
            self.get_bio_data(player_soup)
        except Exception as e:
            print(e)

    # request BS4 object based on player last name initial
    def get_player_list(self) -> BeautifulSoup:
        last_initial = self.name.split(' ')[1][0]
        url = 'https://www.pro-football-reference.com/players/%s/' % (last_initial)
        return get_soup(url, self.gateway)

    # helper function that gets the player's href
    def get_href(self, player_list: BeautifulSoup) -> BeautifulSoup:
        players = player_list.find('div', id='div_players').find_all('p')
        for p in players:
            if self.name in p.text and self.initial_position in p.text:
                return get_soup('https://www.pro-football-reference.com' + p.find('a').get('href'), self.gateway)
        raise Exception('Cannot find a ' + self.initial_position + ' named ' + self.player)


    def get_bio_data(self, player_soup: BeautifulSoup) -> dict:
        # get metadata div from the player pagee
        metadata = player_soup.find('div', id='meta').find_all('p')
        # get each paragraph tag from metadata object
        for attr in metadata:
            # find labels and content based on formatting
            label = attr.find('strong')
            content = attr.text
            # if the content has a label, use label to assign content to the correct k,v in bio
            if label:
                # get position with helper method
                if label.text == 'Position':
                    self.positions, self.throws = self.get_positions(content)
                    continue
                # get three char team
                if label.text == 'Team':
                    team_link = attr.find('a', href=True)
                    if team_link:
                        self.team = team_link['href'][7:10]
                        continue
                # get date of birth and birth state
                if label.text == 'Born:':
                    self.dob, self.birth_region = self.get_birth_data(content)
                    continue
                # get college
                if label.text == 'College':
                    if attr.find('a'):
                        self.college = attr.find('a').text
                    continue
                # get draft data
                if label.text == 'Draft':
                    draft_meta = attr.find_all('a')
                    self.draft['team'] = draft_meta[0]['href'][7:10]
                    self.draft['year'] = draft_meta[0]['href'][11:15]
                    draft_position = content.split('in the')[1].split('of the')[0].strip()
                    round_overall = re.findall(r'\d+', draft_position)
                    self.draft['round'] = round_overall[0]
                    self.draft['overall'] = round_overall[1]
            else:
                # get height and weight
                hw_array = content.split('\xa0')
                [feet, inches] = hw_array[0].split('-')
                self.height = (int(feet) * 12) + int(inches.replace(',', ''))
                self.weight = hw_array[1].replace('lb', '')

    '''
    Helper method to get the positions a player has played as well as their throwing arm if they are a quarterback
    '''
    def get_positions(self, content: str) -> list:
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

    '''
    Helper method to get birth data
    '''
    def get_birth_data(self, content: str) -> list:
        # format content so that 'in' can be accurately removed and split off
        content = repr(content)
        birth_arr = content.split('in\\xa0')
        # return blank values if nothing is present
        if len(birth_arr) == 0:
            return ['', '']
        # format each birth string
        formatted_arr = []
        for s in birth_arr:
            formatted_arr.append(s.replace('\\n', '')
                                .replace('\\t', '')
                                .replace('\\xa0', '')
                                .replace('Born:', '')
                                .replace("'", "")
                                .strip())
        # format birth date string
        dob = datetime.strptime(formatted_arr[0], "%B %d,%Y")
        birthplace = ''
        if len(formatted_arr) > 1:
            birthplace = formatted_arr[1].split(',')[1]
        return [dob, birthplace]


def main():
    gateway = create_api_gateway()
    player = Player("Chad Henne", "QB", gateway)
    player.populate_bio()
    print(player.draft)
    shutdown_api_gateway(gateway)

if __name__ == '__main__':
    main()