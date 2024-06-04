import streamlit as st
import pandas as pd
import appDef
import pickle

#各ポジションのCSVを取得
df_DF = pd.read_csv('DF_stats.csv',index_col=0)#Unnamed=0削除
df_MF = pd.read_csv('MF_stats.csv',index_col=0)
df_FW = pd.read_csv('FW_stats.csv',index_col=0)

df_DF.insert(0,"po","DF")
df_MF.insert(0,"po","MF")
df_FW.insert(0,"po","FW")
#st.write(df_FW)


#レーダーチャートの結果をポジションごとに保存
po_li = ["DF","MF","FW"]
for po in po_li:
    if po == "DF":
        df_score_DF,no_shootNumDF = appDef.addDFScore(df_DF)
    elif po == "MF":
        df_score_MF,no_shootNumMF = appDef.addMFScore(df_MF)
    else:
        df_score_FW,no_shootNumFW = appDef.addFWScore(df_FW)

#df_score_DF.insert(0,"po","DF")
#df_score_MF.insert(0,"po","MF")
#df_score_FW.insert(0,"po","FW")

#勝敗予測
st.header("対戦")
df_total = pd.concat([df_DF, df_MF,df_FW],axis=0,ignore_index=True)

# "player"と"po"の列を組み合わせたリストを作成
df_total['player_po'] = '(' + df_total['po'] + ')' + df_total['player'] 

#選手を選択10人まで
st.subheader("チーム1")
select_team1 = st.multiselect('好きな選手を10人選んでください',options=df_total["player_po"].tolist(), default=[],max_selections=10, key="team1_selection")
#st.write(select_team1)
#"player_no"index番号を取得して選手の名前を表示させてそれを関数に渡す
selected_indices_team1 = []
selected_names_team1 = []
# 選択された選手のインデックス番号と名前を取得して表示
for player_po in select_team1:
    player_index_team1 = df_total[df_total['player_po'] == player_po].index[0]
    selected_indices_team1.append(player_index_team1)
    selected_names_team1.append(df_total.loc[player_index_team1, 'player'])
#df_total["player_po"]いらなかったら削除のコードを選択の下に書いといて(多分いる)

DEFScore_team1,MIDScore_team1,ATTScore_team1,OVRScore_team1 = appDef.selectPlayerStats(selected_names_team1,df_score_DF,df_score_MF,df_score_FW)
#st.write(DEFScore_team1,MIDScore_team1,ATTScore_team1,OVRScore_team1)
#２チームめを作るか既存のチームにするか選択
st.subheader("チーム2")
select_team2 = st.selectbox('2チームを作るor既存のチーム',("作る","既存のチームを選ぶ"))
#データ取得
df_team = pd.read_csv("df_t_p.csv",index_col=0)
if select_team2 == "作る":   
    available_players_team2 = [player for player in df_total["player_po"].tolist() if player not in select_team1]

    #"player_no"index番号を取得して選手の名前を表示させてそれを関数に渡す
    selected_indices_team2 = []
    selected_names_team2 = []
    # 選択された選手のインデックス番号と名前を取得して表示
    for player_po in available_players_team2:
        player_index_team2 = df_total[df_total['player_po'] == player_po].index[0]
        selected_indices_team2.append(player_index_team2)
        selected_names_team2.append(df_total.loc[player_index_team2, 'player'])

    select_team2 = st.multiselect('好きな選手を10人選んでください',options=available_players_team2, default=[],max_selections=10, key="team2_selection")
    #st.write(select_team2)
    DEFScore_team2,MIDScore_team2,ATTScore_team2,OVRScore_team2 = appDef.selectPlayerStats(selected_names_team2,df_score_DF,df_score_MF,df_score_FW)
    #st.write(DEFScore_team2,MIDScore_team2,ATTScore_team2,OVRScore_team2)

    #スコアの差分計算
    teamID = 45
    DEF_diff = DEFScore_team1 - DEFScore_team2
    MID_diff = MIDScore_team1 - MIDScore_team2
    ATT_diff = ATTScore_team1 - ATTScore_team2
    OVR_diff = OVRScore_team1 - OVRScore_team2
else:
    #すでにいるチーム
    team_select = st.selectbox("対戦チームを選んでください",(df_team["Name"].tolist()))
    teamID = df_team["Name"].tolist().index(team_select)
    DEFScore_team2 = df_team.loc[df_team["Name"] == team_select, "DEF"].values[0]
    MIDScore_team2 = df_team.loc[df_team["Name"] == team_select, "MID"].values[0]
    ATTScore_team2 = df_team.loc[df_team["Name"] == team_select, "ATT"].values[0]
    OVRScore_team2 = df_team.loc[df_team["Name"] == team_select, "OVR"].values[0]
    DEF_diff = DEFScore_team1 - DEFScore_team2
    MID_diff = MIDScore_team1 - MIDScore_team2
    ATT_diff = ATTScore_team1 - ATTScore_team2
    OVR_diff = OVRScore_team1 - OVRScore_team2

# モデルのオープン
with open('model.pickle', mode='rb') as f:
    clf = pickle.load(f)

st.subheader("チーム1とチーム2の勝敗予想")
# 評価データ
data = [[44,teamID,ATT_diff,MID_diff,DEF_diff,OVR_diff]]

ans = clf.predict(data)
if not select_team1 or not select_team2:
   st.write("チームを選んでください")
else: 
   if ans[0] == 1:
     st.write("チーム1の勝利")
   elif ans[0] == 0:
     st.write("引き分け")
   elif ans[0] == -1:
     st.write("チーム2の勝利")
   else:
     st.write("ミス")
