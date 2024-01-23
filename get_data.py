import urllib.request
from bs4 import BeautifulSoup
import re
def get_url(url_list):#データを取得
    team_data_list = []#データを収納

    for url in url_list:    
        request = urllib.request.urlopen(url)#
        soup = BeautifulSoup(request,"html.parser")
        elems = soup.find_all("td",class_='sc-tableSection__data')

        for i in range(0,len(elems)):
            try:
                elem = elems[i].contents[0].strip()
                if elem.isdigit():#int型に変換
                    elem = int(elem)
                team_data_list.append(elem)#listに追加
            except IndexError:
                continue

    return team_data_list