import time
import json
import requests
from bs4 import BeautifulSoup
from pprint import pprint


# ===============================================================================
# config
dir_parsed_pages = 'pages'
ireland_cities = {
    0: 'donegal'
}


# ===============================================================================
def scraping_loop(city):
    page = 1
    while True:
        # get html
        html = request_daft_offers_html(city, page)

        # get offers
        offers = get_offers_from_html(html)

        # errors check
        if len(offers) == 0 or offers is False:
            break

        # actuality check
        # TODO: add

        # write html
        write_html(build_html_filepath(city, page), html)

        # handle offers
        handle_offers(offers)

        # stop on the last page
        if len(offers) < 20:
            break
        
        # increment page
        page = page + 1
        time.sleep(5)


def request_daft_offers_html(city, page):
    """
    get content from daft.ie site with list of properties for rent
    
    param city: Ireland city name for search
    param page: page number
    """
    url = f"https://www.daft.ie/property-for-rent/{city}"
    params = {
        'from': (page - 1) * 20,
        'pageSize': 20,
        'sort': 'publishDateDesc'
    }
    r = requests.get(url, params = params)
    return r.text

def build_html_filepath(city, page):
    return f"{dir_parsed_pages}/daft_{city}_{page}.html"

def write_html(filepath, html):
    with open(filepath, 'w+') as f:
        f.write(html)

def read_html(filepath):
    with open(filepath, 'r+') as f:
        return f.read()

def get_offers_from_html(html):
    try:
        soup = BeautifulSoup(html, 'html.parser')
        soup_res = soup.find('script', {"id": "__NEXT_DATA__"}, type='application/json')
        objects = json.loads(soup_res.contents[0])
        return objects['props']['pageProps']['listings']
    except:
        return False
    
def handle_offers(offers):
    print(len(offers))


# ===============================================================================
def main():
    scraping_loop(ireland_cities[0])
    

# ===============================================================================
if __name__ == "__main__":
    main()
