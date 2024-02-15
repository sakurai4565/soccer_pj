import streamlit as st
import pandas as pd
import numpy as np
import matplotlib as mt
import appDef
import pickle
import plotly.graph_objects as go

#リーグデータ集まるまでプレミアリーグで固定
league =  "Premier league"
st.header("総合スコア表")#スコア表

#各ポジションのCSVを取得
df_DF = pd.read_csv('DF_stats.csv',index_col=0)#Unnamed=0削除
df_MF = pd.read_csv('MF_stats.csv',index_col=0)
df_FW = pd.read_csv('FW_stats.csv',index_col=0)

#選択されたリーグの順位表を表示
if league=="Premier league":#ここは変更する予定
    position = st.selectbox("スコア表_ポジション",("DF","MF","FW"))
    name_DF =st.selectbox("項目選択",("すべて","STA","SUB","G","A","SHO","PAS","TA","CLR","COR","FC","FS","Y","R","PEN","Mins"))
    option = st.radio("filetr",("昇順","降順"))
    if position == "DF":
        appDef.test(position,df_DF,name_DF,option)
    elif position == "MF":
        appDef.test(position,df_MF,name_DF,option)
    else:
        appDef.test(position,df_FW,name_DF,option)