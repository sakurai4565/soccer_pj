import streamlit as st
import pandas as pd

#データ取得
df_team = pd.read_csv("df_t_p.csv",index_col=0)
df_match_team = pd.read_csv("df_result_team.csv",index_col=0)

#直近のグラフ
st.header("チームの得失点差")
#選択したチームに関するデータ
select_pitch_name = st.selectbox("チームを選択してください",(df_team["Name"].tolist()),key = "pitch_name")
df_pitch = df_match_team[(df_match_team["チーム1"] == select_pitch_name) | (df_match_team["チーム2"] == select_pitch_name)]

def SetPitch(row):
    if row["チーム1"] == select_pitch_name:
         return int(row["チーム1の得点"] - row["チーム2の得点"])
    elif row["チーム2"] == select_pitch_name:
         return int(row["チーム2の得点"] - row["チーム1の得点"])

# applyメソッドを使用して新しい列 "pitch" を計算
df_pitch["pitch"] = df_pitch.apply(SetPitch, axis=1)

#st.table(df_pitch)
st.line_chart(df_pitch["pitch"].head(30))

