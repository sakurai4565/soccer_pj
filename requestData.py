import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

def position_list(url,DF_players,MF_players,FW_players,DF_list,MF_list,FW_list):#teamのURL,DFの人数,MFの人数,FWの人数
    
    #URL読み込み
    response = requests.get(url)

    if response.status_code == 200:#ブラウザから正常にスクレイピングできた場合
        soup = BeautifulSoup(response.text,'html.parser')
    td_elements = soup.find_all('td')#タグtdで取得

    count = 0

    for td in td_elements:#ポジションごとに分割
        count+=1#for文の回数
        if count < DF_players*16+1:
            DF_list.append(td.text)#DFのリスト追加
        elif count < (DF_players*16+1)+(MF_players*15):#DFの数とMFの数
            MF_list.append(td.text)#MFのリスト追加
        elif count < (DF_players*16+1)+(MF_players*15)+(FW_players*15):#DFの数とMFの数とFWの数
            FW_list.append(td.text)#FWのリスト追加
        else:
            continue

        
    return DF_list,MF_list,FW_list

def getColumns(url):#取得したデータのカラム名を取得
    DF_columns = ['player']
    MF_FW_columns = ['player']

    response = requests.get(url)
    if response.status_code == 200:#ブラウザから正常にスクレイピングできた場合
        soup = BeautifulSoup(response.text,'html.parser')

    columns_elements = soup.find_all('div',class_='Px(cell-padding-x) Py(cell-padding-y) Va(m) C(th-font-color) Fw(n) Fz(th-font-size) Ta(end) C(inverse-text)! Fw(500)!')#タグtdで取得
    columns = 0

    for t in columns_elements:
        columns+=1
        if columns < 16:
            DF_columns.append(t.text)
        elif columns < 30:
            MF_FW_columns.append(t.text)
        else:
            continue
    return DF_columns,MF_FW_columns
