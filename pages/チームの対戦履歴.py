import streamlit as st
import pandas as pd

#データ取得
df_team = pd.read_csv("df_t_p.csv",index_col=0)

#チーム情報
st.header("チームの対戦履歴")
#データ取得
df_match_team = pd.read_csv("df_result_team.csv",index_col=0)
select_match_name = st.selectbox("チームを選択してください",(df_team["Name"].tolist()),key = "match_name")
# 選択したチームに関連する試合のデータを抽出
df_head = df_match_team[(df_match_team["チーム1"] == select_match_name) | (df_match_team["チーム2"] == select_match_name)].head(10)
st.table(df_head)