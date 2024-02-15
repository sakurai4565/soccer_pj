import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import math

#昇順・降順
def test(position,df,name_DF,option):
    if position == "DF":
        if name_DF =="すべて":
            st.table(df)
        else:
            if option == "昇順":
                st.table(df.sort_values(name_DF))
            else:
                st.table(df.sort_values(name_DF,ascending=False))
    elif position == "MF":
        if name_DF =="すべて":
            st.table(df)
        else:
            if option == "昇順":
                st.table(df.sort_values(name_DF))
            else:
                st.table(df.sort_values(name_DF,ascending=False))
    else:
        if name_DF =="すべて":
            st.table(df)
        else:
            if option == "昇順":
                st.table(df.sort_values(name_DF))
            else:
                st.table(df.sort_values(name_DF,ascending=False))

#レーダーチャート用に項目を追加DF
def addDFScore(df_DF):
    #DFの場合
    df_DF["TO"] = df_DF["G"] / df_DF["SHO"]#得点率計算
    
    # 無限大をNaNに置き換える
    df_DF["TO"] = df_DF["TO"].replace(np.inf, np.nan)
    NaN_countDF = df_DF["TO"].isnull().sum()#シュートが０の人
    df_DF["TO"] = df_DF["TO"].fillna(0)#NaNを０にする
    df_DF["CT"] = df_DF["TA"] + df_DF["CLR"]#守備力計算
    df_DF["mi"] = df_DF["Mins"] / (df_DF["STA"] + df_DF["SUB"])#出場時間/出場回数

    #パラメータを０～１００に変換
    df_DF["シュート回数"] = df_DF["SHO"] / df_DF["SHO"].max() * 100
    df_DF["得点率"] = df_DF["TO"] * 100
    df_DF["パス回数"] = df_DF["PAS"] / df_DF["PAS"].max() * 100
    df_DF["出場時間"] = df_DF["mi"] / df_DF["mi"].max() * 100
    df_DF["守備力"] = df_DF["CT"] / df_DF["CT"].max() * 100

    return df_DF,NaN_countDF

#レーダーチャート用に項目を追加MF
def addMFScore(df_MF):
    df_MF["TO"] = df_MF["G"] / df_MF["SHO"]  # 得点率計算

    # 無限大をNaNに置き換える
    df_MF["TO"] = df_MF["TO"].replace(np.inf, np.nan)
    NaN_countMF = df_MF["TO"].isnull().sum()  # シュートが０の人
    df_MF["TO"] = df_MF["TO"].fillna(0)  # NaNを０にする
    df_MF["mi"] = df_MF["Mins"] / (df_MF["STA"] + df_MF["SUB"])  # 出場時間/出場回数


    # パラメータを０～１００に変換
    df_MF["シュート回数"] = df_MF["SHO"] / df_MF["SHO"].max() * 100
    df_MF["得点率"] = df_MF["TO"] * 100
    df_MF["パス回数"] = df_MF["PAS"] / df_MF["PAS"].max() * 100
    df_MF["出場時間"] = df_MF["mi"] / df_MF["mi"].max() * 100


    return df_MF,NaN_countMF

#レーダーチャート用に項目を追加FW
def addFWScore(df_FW):
    df_FW["TO"] = df_FW["G"] / df_FW["SHO"]  # 得点率計算

    # 無限大をNaNに置き換える
    df_FW["TO"] = df_FW["TO"].replace(np.inf, np.nan)
    NaN_countFW = df_FW["TO"].isnull().sum()  # シュートが０の人
    df_FW["TO"] = df_FW["TO"].fillna(0)  # NaNを０にする
    df_FW["mi"] = df_FW["Mins"] / (df_FW["STA"] + df_FW["SUB"])  # 出場時間/出場回数

    # パラメータを０～１００に変換
    df_FW["シュート回数"] = df_FW["SHO"] / df_FW["SHO"].max() * 100
    df_FW["得点率"] = df_FW["TO"] * 100
    df_FW["パス回数"] = df_FW["PAS"] / df_FW["PAS"].max() * 100
    df_FW["出場時間"] = df_FW["mi"] / df_FW["mi"].max() * 100

    return df_FW,NaN_countFW

# レーダーチャートの平均値
def DFAvarageScore(df_DF_score, no_shootNumDF):
    # それぞれの合計
    shoot_total = int(df_DF_score["シュート回数"].sum())
    to_total = int(df_DF_score["得点率"].sum())
    pass_total = int(df_DF_score["パス回数"].sum())
    mins_total = int(df_DF_score["出場時間"].sum())
    syubi_total = int(df_DF_score["守備力"].sum())

    # それぞれの平均
    shoot_avarage = shoot_total / len(df_DF_score["シュート回数"])
    to_avarage = to_total / (len(df_DF_score)-no_shootNumDF) if no_shootNumDF < len(df_DF_score) else 0
    pass_avarage = pass_total / len(df_DF_score)
    mins_avarage = mins_total / len(df_DF_score)
    syubi_avarage = syubi_total / len(df_DF_score)

    return shoot_avarage, to_avarage, pass_avarage, mins_avarage, syubi_avarage

def MFAvarageScore(df_MF_score, no_shootNumMF):
    # それぞれの合計
    shoot_total = int(df_MF_score["シュート回数"].sum())
    to_total = int(df_MF_score["得点率"].sum())
    pass_total = int(df_MF_score["パス回数"].sum())
    mins_total = int(df_MF_score["出場時間"].sum())

    # それぞれの平均
    shoot_avarage = shoot_total / len(df_MF_score["シュート回数"])
    to_avarage = to_total / (len(df_MF_score)-no_shootNumMF) if no_shootNumMF < len(df_MF_score) else 0
    pass_avarage = pass_total / len(df_MF_score)
    mins_avarage = mins_total / len(df_MF_score)

    return shoot_avarage, to_avarage, pass_avarage, mins_avarage


def FWAvarageScore(df_FW_score, no_shootNumFW):
    # それぞれの合計
    shoot_total = int(df_FW_score["シュート回数"].sum())
    to_total = int(df_FW_score["得点率"].sum())
    pass_total = int(df_FW_score["パス回数"].sum())
    mins_total = int(df_FW_score["出場時間"].sum())

    # それぞれの平均
    shoot_avarage = shoot_total / len(df_FW_score["シュート回数"])
    to_avarage = to_total / (len(df_FW_score)-no_shootNumFW) if no_shootNumFW < len(df_FW_score) else 0
    pass_avarage = pass_total / len(df_FW_score)
    mins_avarage = mins_total / len(df_FW_score)

    return shoot_avarage, to_avarage, pass_avarage, mins_avarage

def radetchart(df_score,chart_player,column_names) :
    # 選んだ選手のパラメータを取得
    player_index_list = df_score[df_score["player"] == chart_player].index.tolist()
    player_index = player_index_list[0]
    chart_score = df_score.loc[player_index, column_names].tolist()

    fig = px.line_polar(df_score, r=chart_score, theta=column_names,
                    line_close=True, line_shape='linear', markers=True,
                    title=f'{chart_player}選手の能力評価')
    
    return fig
#取得した選手のスタッツを学習用の値に変換
def calculationDF(stats_shoot, stats_to, stats_pass, stats_min, stats_shyubi):
   
    DEFScore = stats_shoot+(stats_to)*1.2+(stats_pass)*1.2+(stats_min)*0.9+(stats_shyubi)*1.5
    return DEFScore

def calculationMF(stats_shoot, stats_to, stats_pass, stats_min):
   
    MIDScore = (stats_shoot)*1.1+(stats_to)*1.5+(stats_pass)*1.3+stats_min
    return MIDScore

def calculationFW(stats_shoot, stats_to, stats_pass, stats_min):
   
    ATTScore = stats_shoot+(stats_to)*1.5+(stats_pass)*1.2+stats_min
    return ATTScore

#ポジションごとに値を返す
def selectPlayerStats(select_team,df_score_DF,df_score_MF,df_score_FW):
    #初期値
    select_stats = None
    countDF = 0
    countMF = 0
    countFW = 0
    DEFScore = 0
    MIDScore = 0
    ATTScore = 0
    OVRScore = 0
    #各ポジションの合計の最大値を取得
    DF_stats_max,MF_stats_max,FW_stats_max = fullSelectPlayerStats(df_score_DF,df_score_MF,df_score_FW)
    #ポジションごとに該当する名前があれば計算する
    for player in select_team:
        if player in df_score_DF["player"].values:
            select_stats = df_score_DF.loc[df_score_DF["player"] == player, ["シュート回数", "得点率", "パス回数", "出場時間", "守備力"]]
            index = df_score_DF.loc[df_score_DF["player"] == player].index
            AddDEF = calculationDF(
                select_stats.loc[index, "シュート回数"].values[0],
                select_stats.loc[index, "得点率"].values[0],
                select_stats.loc[index, "パス回数"].values[0],
                select_stats.loc[index, "出場時間"].values[0],
                select_stats.loc[index, "守備力"].values[0]
            )
            DEFScore = math.floor(DEFScore + AddDEF)
            countDF+=1
  
        elif player in df_score_MF["player"].values:
            select_stats = df_score_MF.loc[df_score_MF["player"] == player, ["シュート回数", "得点率", "パス回数", "出場時間"]]
            index = df_score_MF.loc[df_score_MF["player"] == player].index
            AddMID = calculationMF(
                select_stats.loc[index, "シュート回数"].values[0],
                select_stats.loc[index, "得点率"].values[0],
                select_stats.loc[index, "パス回数"].values[0],
                select_stats.loc[index, "出場時間"].values[0]
            )
            MIDScore = math.floor(MIDScore + AddMID)
            countMF+=1

        elif player in df_score_FW["player"].values:
            select_stats = df_score_FW.loc[df_score_FW["player"] == player, ["シュート回数", "得点率", "パス回数", "出場時間"]]
            index = df_score_FW.loc[df_score_FW["player"] == player].index
            AddATT = calculationFW(
                select_stats.loc[index, "シュート回数"].values[0],
                select_stats.loc[index, "得点率"].values[0],
                select_stats.loc[index, "パス回数"].values[0],
                select_stats.loc[index, "出場時間"].values[0]
            )
            ATTScore = math.floor(ATTScore + AddATT)
            countFW+=1

        else:
          st.write("選手が見つからない")
    #人数分割る
    if countDF != 0:
        DEFScore = math.floor(DEFScore / countDF)
        #仮の最大値で計算
        DEFScore =  math.floor((DEFScore / DF_stats_max)*100)+10
    else:
        DEFScore = 0
    if countMF != 0:
        MIDScore = math.floor(MIDScore / countMF)
        #仮の最大値で計算
        MIDScore =  math.floor((DEFScore / MF_stats_max)*50)+50
    else:
        MIDScore = 0
    if countFW != 0:
        ATTScore = math.floor(ATTScore / countFW)
        #仮の最大値で計算    
        ATTScore =  math.floor((DEFScore / FW_stats_max)*50)+50
    else:
        ATTScore = 0    
    OVRScore = math.floor((DEFScore+MIDScore+ATTScore)/3)

    #st.write(DEFScore)
    #st.write(MIDScore)
    #st.write(ATTScore)
    #st.write(OVRScore)
    return DEFScore,MIDScore,ATTScore,OVRScore


#全体のスコア計算
def fullSelectPlayerStats(df_score_DF,df_score_MF,df_score_FW):
    df_score_DF["stats"] = df_score_DF["シュート回数"]+(df_score_DF["得点率"])*1.2+(df_score_DF["パス回数"])*1.2+(df_score_DF["出場時間"])*0.9+(df_score_DF["守備力"])*1.5
    df_score_MF["stats"] = (df_score_MF["シュート回数"])*1.1+(df_score_MF["得点率"])*1.5+(df_score_MF["パス回数"])*1.3+df_score_MF["出場時間"]
    df_score_FW["stats"] = df_score_FW["シュート回数"]+(df_score_FW["得点率"])*1.5+(df_score_FW["パス回数"])*1.2+df_score_FW["出場時間"]

    DF_stats_max = math.floor(df_score_DF["stats"].max())
    MF_stats_max = math.floor(df_score_MF["stats"].max())
    FW_stats_max = math.floor(df_score_FW["stats"].max())
    return DF_stats_max,MF_stats_max,FW_stats_max