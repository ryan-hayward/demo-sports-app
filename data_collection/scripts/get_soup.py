from bs4 import BeautifulSoup
import requests, time, random
from requests_ip_rotator import ApiGateway

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
def get_soup(request_url: str, gateway: ApiGateway) -> BeautifulSoup:
    # start a request session and mount the gateway to serve as a proxy IP
    session = requests.session()
    session.mount("https://1.1.1.1:8080", gateway)
    # make the request to the specified URL
    response = session.get(request_url)
    print(response.status_code)
    pause = round(random.uniform(0, 1), 2)
    time.sleep(pause)
    # return soup
    return BeautifulSoup(response.text, 'html.parser')

