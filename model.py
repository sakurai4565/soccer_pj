import pandas as pd
import numpy as np
import requestData

#teamurlリスト+人数
url_numPeaple = [
        #URL + DFの人数 + MFの人数 + FWの人数
       'https://sports.yahoo.com/soccer/teams/manchester-city/stats/',7,10,3,
       'https://sports.yahoo.com/soccer/teams/arsenal/stats',7,8,5,
       'https://sports.yahoo.com/soccer/teams/bournemouth/stats',7,8,7,
       'https://sports.yahoo.com/soccer/teams/brighton-and-hove-albion/stats',7,12,6,
       'https://sports.yahoo.com/soccer/teams/chelsea/stats',9,7,7,
       'https://sports.yahoo.com/soccer/teams/everton/stats',7,9,4,
       'https://sports.yahoo.com/soccer/teams/liverpool/stats',8,5,7,
       'https://sports.yahoo.com/soccer/teams/newcastle-united/stats',11,12,3,
       'https://sports.yahoo.com/soccer/teams/sheffield-united/stats',10,10,5,
       'https://sports.yahoo.com/soccer/teams/west-ham-united/stats',8,6,5,
       'https://sports.yahoo.com/soccer/teams/aston-villa/stats',7,10,4,
       'https://sports.yahoo.com/soccer/teams/brentford/stats',7,10,7,
       'https://sports.yahoo.com/soccer/teams/burnley/stats',8,6,11,
       'https://sports.yahoo.com/soccer/teams/crystal-palace/stats',6,11,3,
       'https://sports.yahoo.com/soccer/teams/fulham/stats/',8,6,7,
       'https://sports.yahoo.com/soccer/teams/luton-town/stats',7,9,6,
       'https://sports.yahoo.com/soccer/teams/manchester-united/stats',9,10,5,
       'https://sports.yahoo.com/soccer/teams/nottingham-forest/stats',11,8,5,
       'https://sports.yahoo.com/soccer/teams/tottenham-hotspur/stats',6,10,5,
       'https://sports.yahoo.com/soccer/teams/wolverhampton-wanderers/stats',9,5,4,
]

#url_t = 'https://sports.yahoo.com/soccer/teams/arsenal/stats/'
#df = 7
#mf = 8

DF_list = []
MF_list = []
FW_list = []
#for文で回す
for i in range(0, len(url_numPeaple), 4):
  url = url_numPeaple[i]#teamURL
  DF_players = url_numPeaple[i+1]#DF人数
  MF_players = url_numPeaple[i+2]#MF人数
  FW_players = url_numPeaple[i+3]#FW人数

  #スクレイピングしてきたデータをポジションごとにリストで分割してそれぞれのリストに追加
  DF_list,MF_list,FW_list = requestData.position_list(url,DF_players,MF_players,FW_players,DF_list,MF_list,FW_list)
#print(DF_list)
#print(MF_list)
#print(FW_list)

#2次元配列に変換
DF_arr = np.array(DF_list).reshape(-1,16)
MF_arr = np.array(MF_list).reshape(-1,15)
FW_arr = np.array(FW_list).reshape(-1,15)

#dfに変換
df_DF = pd.DataFrame(DF_arr)
df_MF = pd.DataFrame(MF_arr)
df_FW = pd.DataFrame(FW_arr)

#カラム名を取得
columnUrl = 'https://sports.yahoo.com/soccer/teams/manchester-city/stats/'
DF_columns,MF_FW_columns = requestData.getColumns(columnUrl)

#データフレームのカラム名を変更
df_DF.columns = DF_columns
df_MF.columns = MF_FW_columns
df_FW.columns = MF_FW_columns
#print(url_numPeaple)
teamlist = [
        "manchester-city","arsenal","bournemouth","brighton-and-hove-albion","chelsea",
        "everton","liverpool","newcastle-united","sheffield-united","west-ham-united",
        "aston-villa","brentford","burnley","crystal-palace","fulham",
        "luton-town","manchester-united","nottingham-forest","tottenham-hotspur","wolverhampton-wanderers"
            ]

n_DF = 0
n_MF = 0
n_FW = 0
count = 0
# チーム名の列を追加
for i in range(0, len(url_numPeaple), 4):
    num_DF = url_numPeaple[i + 1]#各チームの人数
    # DFのチーム名入力

    df_DF.loc[n_DF:n_DF + num_DF - 1, 'Team'] = teamlist[count]#人数分Team列にチーム名を入力
    n_DF = n_DF + num_DF#入力したチーム名のindex番号

    num_MF = url_numPeaple[i + 2]#各チームの人数
    # MFのチーム名入力

    df_MF.loc[n_MF:n_MF + num_MF - 1, 'Team'] = teamlist[count]
    n_MF = n_MF + num_MF  

    num_FW = url_numPeaple[i + 3]#各チームの人数
    # FWのチーム名入力

    df_FW.loc[n_FW:n_FW + num_FW - 1, 'Team'] = teamlist[count]
    n_FW = n_FW + num_FW

    count+=1

#print(df_DF)
#csvとして出力
df_DF.to_csv('DF_stats.csv')
df_MF.to_csv('MF_stats.csv')
df_FW.to_csv('FW_stats.csv')