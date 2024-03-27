from bs4 import BeautifulSoup
import requests, time, random


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
    # store response from request and pause to avoid ban
    response = requests.get(request_url)
    pause = round(random.uniform(0.5, 4.5), 2)
    time.sleep(pause)
    # return soup
    return BeautifulSoup(response.text, 'html.parser')