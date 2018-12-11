import time
import pickle
import requests
import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm

'''Scraper for wacraftrealms since their csv download option does not work'''


# Get all the options for the servers and their respective ID
def get_server_and_id():
    request = requests.get("http://www.warcraftrealms.com/activity.php?").content
    soup_server = BeautifulSoup(request)
    server_and_id = {}
    for i in range(len(soup_server.find_all('table')[2].find('select').find_all('option'))):
        server_name = soup_server.find_all('table')[2].find('select').find_all('option')[i].text
        server_id = soup_server.find_all('table')[2].find('select').find_all('option')[i].attrs['value']
        server_and_id[server_id] = server_name
    return server_and_id


def create_table(soup):
    table = {"alliance_avg": [],
             "horde_average": []}
    hours = soup.find_all('table')[3].find_all('tr')[1:25]  # Only select the 24h of the day
    for hour in hours:
        row_entry = hour.find_all('td')[1:5]
        table["alliance_avg"].append(row_entry[0].text)
        # table['alliance_entries'].append(row_entry[1].text)
        table['horde_average'].append(row_entry[2].text)
        # table['horde_entries'].append(row_entry[3].text)
    return pd.DataFrame(table)


def scrape(server_and_id):
    ids = list(server_and_id.keys())
    for server_id in tqdm(ids):
        time.sleep(4)  # To be gently with wacraftrealms
        request = requests.get("http://www.warcraftrealms.com/activity.php?serverid={}".format(server_id)).content
        soup = BeautifulSoup(request)
        table = create_table(soup)
        name = server_and_id[server_id]
        server_and_id[server_id] = (name, table)
    pickle.dump(server_and_id, open("crawled_server_activity.p", 'wb'))
