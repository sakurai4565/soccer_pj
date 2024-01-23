import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import numpy as np

#チームのパラメーター
url_list = [
 "https://www.fifaindex.com/teams/?league=13&league=14&order=desc",#FIFAindex
  "https://www.fifaindex.com/teams/?page=2&league=13&league=14&order=desc"
]
#試合の結果
url_list_match = [
  "https://www.skysports.com/premier-league-results/2023-24",
  "https://www.skysports.com/premier-league-results/2022-23",#FIFAindex
  "https://www.skysports.com/premier-league-results/2021-22",
  "https://www.skysports.com/premier-league-results/2020-21",
  "https://www.skysports.com/premier-league-results/2019-20",
  "https://www.skysports.com/premier-league-results/2018-19"
]

data_list = []

vsname = []
vsscore = []

#チームのパラメーターの処理
for i in range(len(url_list)):
  #URL読み込み
  response = requests.get(url_list[i])

  if response.status_code == 200:#ブラウザから正常にスクレイピングできた場合
      soup = BeautifulSoup(response.text,'html.parser')
  #タグtdで取得（パラメータ＋名前）
  td_elements = soup.find_all('td')#30チーム
  #td_elements2 = soup.find_all('td')#ついかで30チーム

  for td_elem in td_elements:
      data_list.append(td_elem.get_text(strip=True))
  #for td_elem in td_elements2:
   #   data_list.append(td_elem.get_text(strip=True))

  th_elements = soup.find_all('th')
  colum_list = []#タグthで取得（カラム名）
  for th_elem in th_elements:
      colum_list.append(th_elem.get_text(strip=True))

#試合の結果の処理
for u in range(len(url_list_match)):

  #URL読み込み
  response = requests.get(url_list_match[u])

  if response.status_code == 200:#ブラウザから正常にスクレイピングできた場合
      soup = BeautifulSoup(response.text,'html.parser')

  teamNames = soup.find_all("span",class_='swap-text__target')#名前取得
  scores = soup.find_all("span",class_="matches__teamscores-side")#得点取得
  #print(len(teamNames))

  for name in teamNames[1:]:
    vsname.append(name.get_text(strip=True))#試合のチーム名
  for score in scores:
    vsscore.append(score.get_text(strip=True))#試合のスコア


#それぞれのデータフレームに変換
# 空の要素を取り除いて表示
cleaned_data = []
for item in data_list:
  if item:
    cleaned_data.append(item)
#cleaned_data = [item for item in data_list if item]
columns_data = [column for column in colum_list[:-1] if column]
team_Parameter = np.array(cleaned_data).reshape(-1,6)#２次元に変更
df_t_P = pd.DataFrame(team_Parameter)#データフレームに変更
df_t_P.columns = columns_data#カラム名を変更
#df_t_P

def changeSort(i,vsname,vsscore):#試合の順番をきれいにする
  results = [vsname[i],vsscore[i],vsscore[i+1],vsname[i+1]]
  return results

#二次元配列にする
results=[changeSort(i,vsname,vsscore) for i in  range(0,int(len(vsname)/2-1)) ]


df_result_team = pd.DataFrame(results)
# 列名を変更
df_result_team.columns = ["チーム1", "チーム1の得点", "チーム2の得点", "チーム2"]

#チーム名を合わせる
df_result_team.loc[df_result_team["チーム1"] == "Brighton and Hove Albion", "チーム1"] = "Brighton & Hove Albion"
df_result_team.loc[df_result_team["チーム2"] == "Brighton and Hove Albion", "チーム2"] = "Brighton & Hove Albion"
df_result_team.loc[df_result_team["チーム1"] == "Bournemouth", "チーム1"] = "AFC Bournemouth"
df_result_team.loc[df_result_team["チーム2"] == "Bournemouth", "チーム2"] = "AFC Bournemouth"

#データ結合
# 'チーム1' に関する結合
df_team_merged_1 = pd.merge(df_result_team, df_t_P, left_on="チーム1", right_on="Name", how='left').drop(columns="League")
# 'チーム2' に関する結合
df_team_merged_2 = pd.merge(df_result_team, df_t_P, left_on="チーム2", right_on="Name", how='left').drop(columns="League")
df_result_diff = pd.merge(df_team_merged_1,df_team_merged_2,on=['チーム1','チーム1の得点','チーム2の得点','チーム2'],how='outer',suffixes=['_1','_2']).drop(columns=["Name_1","Name_2"])
#intに変換
df_result_diff["ATT_1"] = df_result_diff["ATT_1"].astype(int)
df_result_diff["ATT_2"] = df_result_diff["ATT_2"].astype(int)
df_result_diff["MID_1"] = df_result_diff["MID_1"].astype(int)
df_result_diff["MID_2"] = df_result_diff["MID_2"].astype(int)
df_result_diff["DEF_1"] = df_result_diff["DEF_1"].astype(int)
df_result_diff["DEF_2"] = df_result_diff["DEF_2"].astype(int)
df_result_diff["OVR_1"] = df_result_diff["OVR_1"].astype(int)
df_result_diff["OVR_2"] = df_result_diff["OVR_2"].astype(int)
df_result_diff["チーム1の得点"] = df_result_diff["チーム1の得点"].astype(int)
df_result_diff["チーム2の得点"] = df_result_diff["チーム2の得点"].astype(int)
#チーム1とチーム２のスコア差を計算
df_result_diff["ATT_diff"] = df_result_diff["ATT_1"] - df_result_diff["ATT_2"]
df_result_diff["MID_diff"] = df_result_diff["MID_1"] - df_result_diff["MID_2"]
df_result_diff["DEF_diff"] = df_result_diff["DEF_1"] - df_result_diff["DEF_2"]
df_result_diff["OVR_diff"] = df_result_diff["OVR_1"] - df_result_diff["OVR_2"]
#HomeAwayはいったん考慮しない
#if df_result_diff["チーム1の得点"] > df_result_diff["チーム2の得点"]:
#    df_result_diff["Result"] = 1
#elif df_result_diff["チーム1の得点"] == df_result_diff["チーム2の得点"]:
#    df_result_diff["Result"] = 0
#elif df_result_diff["チーム1の得点"] < df_result_diff["チーム2の得点"]:
#    df_result_diff["Result"] = -1

#勝ち引き分け負けの場合
df_result_diff["Result"] = np.where(df_result_diff["チーム1の得点"] > df_result_diff["チーム2の得点"], 1, np.where(df_result_diff["チーム1の得点"] == df_result_diff["チーム2の得点"], 0, -1))
#勝ち負けのみの場合
#df_result_diff["Result"] = np.where(df_result_diff["チーム1の得点"] > df_result_diff["チーム2の得点"], 1, 0)
df_result = df_result_diff[['チーム1','チーム2',"チーム1の得点","チーム2の得点","ATT_diff","MID_diff","DEF_diff","OVR_diff","Result"]]
df_result['Team1'] = df_result['チーム1'].astype('category').cat.codes
df_result['Team2'] = df_result['チーム2'].astype('category').cat.codes
df_result = df_result.drop(columns=["チーム1","チーム2"])
#csvとして出力
df_result.to_csv('DF_result.csv')
df_t_P.to_csv("df_t_p.csv")
df_result_team.to_csv("df_result_team.csv")