import datetime
import time
import pandas as pd
import requests
from bs4 import BeautifulSoup


headers = {
    'Connection': 'keep-alive',
    'User-Agent': 'Chrome/102.0.5005.63 Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.5 (KHTML, like Gecko) Safari/536.5',
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate',
    'Content-Type': 'text',
    'Accept-Language': 'en-US,en;q=0.8'
}

# ================================================================================
#                         Getting data
# ================================================================================
def get_url():
    print('==================== Getting States value ====================')
    soup = BeautifulSoup(requests.get("https://www.broadcastify.com/listen/", headers=headers).content, 'lxml')
    lls = soup.find('select', {'name': 'stid'}).find_all('option')
    option_list = []
    for ll in lls:
        option = ''
        try:
            option = ll['value']
        except:
            pass
        option_list.append(option)

    print('==================== Getting COUNTY urls ====================')
    url = "https://www.broadcastify.com/listen/stid/"
    feeds = []
    count = 0
    for opt_num in option_list:
        count += 1
        print('Getting state ' + str(count) + ' out of ' + str(len(option_list)))
        soup = BeautifulSoup(requests.get(url + str(opt_num), headers=headers).content, 'lxml')
        try:
            lis = soup.find('select', {'name': 'ctid'}).find_all('option')
            for li in lis:
                ctid = ''
                try:
                    temp = li['value']
                    ctid = str(temp).split(',')[-1]
                except:
                    pass
                if len(str(ctid)) > 0:
                    if ctid not in feeds:
                        feeds.append(ctid)
        except:
            pass
    print('==================== Getting Feeds data ====================')
    ll = 0
    for ctid_num in feeds:
        ll += 1
        print('Getting county link ' + str(ll) + ' out of ' + str(len(feeds)))
        soup = BeautifulSoup(requests.get("https://www.broadcastify.com/listen/ctid/" + str(ctid_num), headers=headers).content, 'lxml')
        country = ''
        city = ''
        county = ''
        try:
            country = '"' + soup.find('div', {'class': 'contentBox'}).find_all('a')[0].text.replace('\n', '').strip() + '"'
        except:
            pass
        try:
            city = '"' + soup.find('div', {'class': 'contentBox'}).find_all('a')[1].text.replace('\n', '').strip() + '"'
        except:
            pass
        try:
            county = '"' + soup.find('div', {'class': 'contentBox'}).find_all('a')[2].text.replace('\n', '').strip() + '"'
        except:
            pass
        try:
            lis = soup.find('table', {'class': 'btable'}).find_all('tr')
            print("Feeds here: ", len(lis))
            for li in lis:
                feed_id = ''
                player_link = ''
                feed_name = ''
                feed_des = ''
                feed_genre = ''
                listeners = ''
                status = ''
                try:
                    feed_id = '"' + li.find_all('td')[0]['id'] + '"'
                except:
                    pass
                try:
                    if len(feed_id) > 2:
                        temp = str(feed_id).split('-')[-1]
                        player_link = '"' + "https://broadcastify.cdnstream1.com/" + str(temp) + '"'
                except:
                    pass
                try:
                    feed_name = '"' + li.find_all('td')[1].find('a').text.replace('\n', '').strip() + '"'
                except:
                    pass
                try:
                    feed_des = '"' + li.find_all('td')[1].find('span', {'class': 'rrfont'}).text.replace('\n', '').strip() + '"'
                except:
                    pass
                try:
                    feed_genre = '"' + li.find_all('td')[2].text.replace('\n', '').strip() + '"'
                except:
                    pass
                try:
                    listeners = '"' + li.find_all('td')[3].text.replace('\n', '').strip() + '"'
                except:
                    pass
                try:
                    status = '"' + li.find_all('td')[6].text.replace('\n', '').strip() + '"'
                except:
                    pass

                if len(str(feed_id)) > 2:
                    data = {
                        'Feed ID': feed_id,
                        'Country': country,
                        'City': city,
                        'County': county,
                        'Feed Name': feed_name,
                        'Feed Description': feed_des,
                        'Feed Genre': feed_genre,
                        'Listeners Count': listeners,
                        'Status': status,
                        'Player Link': player_link,
                    }
                    df = pd.DataFrame([data])
                    df.to_csv('Broadcastify_Data.csv', mode='a', header=not os.path.exists('Broadcastify_Data.csv'), encoding='utf-8-sig', index=False)
        except:
            pass
    print("Data scraped successfully....")




if __name__ == '__main__':
    get_url()