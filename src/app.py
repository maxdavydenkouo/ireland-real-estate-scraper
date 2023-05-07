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
def request_daft_property_html(city, page):
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

def parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    soup_res = soup.find('script', {"id": "__NEXT_DATA__"}, type='application/json')
    objects = json.loads(soup_res.contents[0])
    return objects['props']['pageProps']['listings']


# ===============================================================================
def main():
    page = 1
    # get html
    html = request_daft_property_html(ireland_cities[0], page)

    # save html
    write_html(build_html_filepath(ireland_cities[0], page), html)
    
    # read_html
    html = read_html(build_html_filepath(ireland_cities[0], page))

    # parse html
    rent_items = parse_html(html)
    pprint(rent_items[0])


# ===============================================================================
if __name__ == "__main__":
    main()
