import streamlit as st
# import pandas as pd
# import numpy as np
# import matplotlib as mt
# import appDef
# import pickle
# import plotly.graph_objects as go

st.title("サッカーの勝敗予測アプリ")
#リーグ選択プレミアリーグ、ブンデスリーガ、セリエA、ラ・リーガ、リーグ・アン
league = st.selectbox("リーグ",("Premier league","La Liga","Serie A","Bundesliga","Ligue 1"))

# st.header("総合スコア表")#スコア表

# #各ポジションのCSVを取得
# df_DF = pd.read_csv('DF_stats.csv',index_col=0)#Unnamed=0削除
# df_MF = pd.read_csv('MF_stats.csv',index_col=0)
# df_FW = pd.read_csv('FW_stats.csv',index_col=0)

# #選択されたリーグの順位表を表示
# if league=="Premier league":#ここは変更する予定
#     position = st.selectbox("スコア表_ポジション",("DF","MF","FW"))
#     name_DF =st.selectbox("項目選択",("すべて","STA","SUB","G","A","SHO","PAS","TA","CLR","COR","FC","FS","Y","R","PEN","Mins"))
#     option = st.radio("filetr",("昇順","降順"))
#     if position == "DF":
#         appDef.test(position,df_DF,name_DF,option)
#     elif position == "MF":
#         appDef.test(position,df_MF,name_DF,option)
#     else:
#         appDef.test(position,df_FW,name_DF,option)

# st.header("レーダーチャート")#スコアチャート

# # レーダーチャート用ポジション選択
# chart_position = st.selectbox("レーダーチャート_ポジション", ("DF", "MF", "FW"), key="chart_position")

# # レーダーチャートの選手選択
# if chart_position == "DF":
#     chart_player = st.selectbox("選手名", df_DF["player"], key="chart_player_DF")
#     df_score, no_shootNumDF = appDef.addDFScore(df_DF)
#     column_names = ['シュート回数', '得点率', 'パス回数', '出場時間', '守備力']  # 表示する項目
#     average_score = appDef.DFAvarageScore(df_score, no_shootNumDF)[0:5]
#     fig = appDef.radetchart(df_score,chart_player,column_names)

# elif chart_position == "MF":
#     chart_player = st.selectbox("選手名", df_MF["player"], key="chart_player_MF")
#     df_score, no_shootNumMF = appDef.addMFScore(df_MF)
#     column_names = ['シュート回数', '得点率', 'パス回数', '出場時間']  # 表示する項目
#     average_score = appDef.MFAvarageScore(df_score, no_shootNumMF)[0:4]
#     fig = appDef.radetchart(df_score,chart_player,column_names)

# elif chart_position == "FW":
#     chart_player = st.selectbox("選手名", df_FW["player"], key="chart_player_FW")
#     df_score, no_shootNumFW = appDef.addFWScore(df_FW)
#     column_names = ['シュート回数', '得点率', 'パス回数', '出場時間']  # 表示する項目
#     average_score = appDef.FWAvarageScore(df_score, no_shootNumFW)[0:4]
#     fig = appDef.radetchart(df_score,chart_player,column_names)


# # 線の透明度を指定（選手）
# line_alpha = 0.8
# fig.update_traces(line=dict(color=f'rgba(106, 90, 205, {line_alpha})',
#                             width=2, dash='solid'),
#                   fill='toself', fillcolor='rgba(106, 90, 205, 0.2)')
# # タプルからリストに変換
# average_score_list = list(average_score)
# # 最初の要素をリストに追加
# average_score_list.append(average_score[0])

# # 平均値のレーダーチャートを追加、色の指定
# average_trace = go.Scatterpolar(r=average_score_list, theta=column_names,
#                                 fill='toself', fillcolor='rgba(255, 0, 0, 0.2)',
#                                 line=dict(color=f'rgba(255, 0, 0, {line_alpha})', width=2, dash='solid'),
#                                 mode='markers+lines',
#                                 name='Average')


# fig.add_trace(average_trace)

# # 0～100までのグラフ、色
# fig.update_polars(radialaxis=dict(visible=True, range=[0, 100], tickfont=dict(color='purple')))

# st.plotly_chart(fig)

# #レーダーチャートの結果をポジションごとに保存
# po_li = ["DF","MF","FW"]
# for po in po_li:
#     if po == "DF":
#         df_score_DF,no_shootNumDF = appDef.addDFScore(df_DF)
#     elif po == "MF":
#         df_score_MF,no_shootNumMF = appDef.addMFScore(df_MF)
#     else:
#         df_score_FW,no_shootNumFW = appDef.addFWScore(df_FW)

# #勝敗予測
# st.header("対戦")
# df_total = pd.concat([df_DF, df_MF,df_FW],axis=0,ignore_index=True)
# #選手を選択10人まで
# st.subheader("チーム1")
# select_team1 = st.multiselect('好きな選手を10人選んでください',options=df_total["player"].tolist(), default=[],max_selections=10, key="team1_selection")
# DEFScore_team1,MIDScore_team1,ATTScore_team1,OVRScore_team1 = appDef.selectPlayerStats(select_team1,df_score_DF,df_score_MF,df_score_FW)
# #st.write(DEFScore_team1,MIDScore_team1,ATTScore_team1,OVRScore_team1)
# #２チームめを作るか既存のチームにするか選択
# st.subheader("チーム2")
# select_team2 = st.selectbox('2チームを作るor既存のチーム',("作る","既存のチームを選ぶ"))
# #データ取得
# df_team = pd.read_csv("df_t_p.csv",index_col=0)
# if select_team2 == "作る":   
#     select_team2 = st.multiselect('好きな選手を10人選んでください',options=df_total["player"].tolist(), default=[],max_selections=10, key="team2_selection")
#     DEFScore_team2,MIDScore_team2,ATTScore_team2,OVRScore_team2 = appDef.selectPlayerStats(select_team2,df_score_DF,df_score_MF,df_score_FW)
#     #st.write(DEFScore_team2,MIDScore_team2,ATTScore_team2,OVRScore_team2)

#     #スコアの差分計算
#     teamID = 45
#     DEF_diff = DEFScore_team1 - DEFScore_team2
#     MID_diff = MIDScore_team1 - MIDScore_team2
#     ATT_diff = ATTScore_team1 - ATTScore_team2
#     OVR_diff = OVRScore_team1 - OVRScore_team2
# else:
#     #すでにいるチーム
#     team_select = st.selectbox("対戦チームを選んでください",(df_team["Name"].tolist()))
#     teamID = df_team["Name"].tolist().index(team_select)
#     DEFScore_team2 = df_team.loc[df_team["Name"] == team_select, "DEF"].values[0]
#     MIDScore_team2 = df_team.loc[df_team["Name"] == team_select, "MID"].values[0]
#     ATTScore_team2 = df_team.loc[df_team["Name"] == team_select, "ATT"].values[0]
#     OVRScore_team2 = df_team.loc[df_team["Name"] == team_select, "OVR"].values[0]
#     DEF_diff = DEFScore_team1 - DEFScore_team2
#     MID_diff = MIDScore_team1 - MIDScore_team2
#     ATT_diff = ATTScore_team1 - ATTScore_team2
#     OVR_diff = OVRScore_team1 - OVRScore_team2

# # モデルのオープン
# with open('model.pickle', mode='rb') as f:
#     clf = pickle.load(f)

# st.subheader("チーム1とチーム2の勝敗予想")
# # 評価データ
# data = [[44,teamID,ATT_diff,MID_diff,DEF_diff,OVR_diff]]

# ans = clf.predict(data)
# if not select_team1 or not select_team2:
#    st.write("チームを選んでください")
# else: 
#    if ans[0] == 1:
#      st.write("チーム1の勝利")
#    elif ans[0] == 0:
#      st.write("引き分け")
#    elif ans[0] == -1:
#      st.write("チーム2の勝利")
#    else:
#      st.write("ミス")

# #チーム情報
# st.header("チームの対戦履歴")
# #データ取得
# df_match_team = pd.read_csv("df_result_team.csv",index_col=0)
# select_match_name = st.selectbox("チームを選択してください",(df_team["Name"].tolist()),key = "match_name")
# # 選択したチームに関連する試合のデータを抽出
# df_head = df_match_team[(df_match_team["チーム1"] == select_match_name) | (df_match_team["チーム2"] == select_match_name)].head(10)
# st.table(df_head)
# #直近のグラフ
# st.header("チームの得失点差")
# #選択したチームに関するデータ
# select_pitch_name = st.selectbox("チームを選択してください",(df_team["Name"].tolist()),key = "pitch_name")
# df_pitch = df_match_team[(df_match_team["チーム1"] == select_pitch_name) | (df_match_team["チーム2"] == select_pitch_name)]

# def SetPitch(row):
#     if row["チーム1"] == select_pitch_name:
#          return int(row["チーム1の得点"] - row["チーム2の得点"])
#     elif row["チーム2"] == select_pitch_name:
#          return int(row["チーム2の得点"] - row["チーム1の得点"])

# # applyメソッドを使用して新しい列 "pitch" を計算
# df_pitch["pitch"] = df_pitch.apply(SetPitch, axis=1)

# #st.table(df_pitch)
# st.line_chart(df_pitch["pitch"].head(20))