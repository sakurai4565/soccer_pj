import streamlit as st
import pandas as pd
import appDef
import plotly.graph_objects as go

#各ポジションのCSVを取得
df_DF = pd.read_csv('DF_stats.csv',index_col=0)#Unnamed=0削除
df_MF = pd.read_csv('MF_stats.csv',index_col=0)
df_FW = pd.read_csv('FW_stats.csv',index_col=0)

st.header("レーダーチャート")#スコアチャート

# レーダーチャート用ポジション選択
chart_position = st.selectbox("レーダーチャート_ポジション", ("DF", "MF", "FW"), key="chart_position")

# レーダーチャートの選手選択
if chart_position == "DF":
    chart_player = st.selectbox("選手名", df_DF["player"], key="chart_player_DF")
    df_score, no_shootNumDF = appDef.addDFScore(df_DF)
    column_names = ['シュート回数', '得点率', 'パス回数', '出場時間', '守備力']  # 表示する項目
    average_score = appDef.DFAvarageScore(df_score, no_shootNumDF)[0:5]
    fig = appDef.radetchart(df_score,chart_player,column_names)

elif chart_position == "MF":
    chart_player = st.selectbox("選手名", df_MF["player"], key="chart_player_MF")
    df_score, no_shootNumMF = appDef.addMFScore(df_MF)
    column_names = ['シュート回数', '得点率', 'パス回数', '出場時間']  # 表示する項目
    average_score = appDef.MFAvarageScore(df_score, no_shootNumMF)[0:4]
    fig = appDef.radetchart(df_score,chart_player,column_names)

elif chart_position == "FW":
    chart_player = st.selectbox("選手名", df_FW["player"], key="chart_player_FW")
    df_score, no_shootNumFW = appDef.addFWScore(df_FW)
    column_names = ['シュート回数', '得点率', 'パス回数', '出場時間']  # 表示する項目
    average_score = appDef.FWAvarageScore(df_score, no_shootNumFW)[0:4]
    fig = appDef.radetchart(df_score,chart_player,column_names)


# 線の透明度を指定（選手）
line_alpha = 0.8
fig.update_traces(line=dict(color=f'rgba(106, 90, 205, {line_alpha})',
                            width=2, dash='solid'),
                  fill='toself', fillcolor='rgba(106, 90, 205, 0.2)')
# タプルからリストに変換
average_score_list = list(average_score)
# 最初の要素をリストに追加
average_score_list.append(average_score[0])

# 平均値のレーダーチャートを追加、色の指定
average_trace = go.Scatterpolar(r=average_score_list, theta=column_names,
                                fill='toself', fillcolor='rgba(255, 0, 0, 0.2)',
                                line=dict(color=f'rgba(255, 0, 0, {line_alpha})', width=2, dash='solid'),
                                mode='markers+lines',
                                name='Average')


fig.add_trace(average_trace)

# 0～100までのグラフ、色
fig.update_polars(radialaxis=dict(visible=True, range=[0, 100], tickfont=dict(color='purple')))

st.plotly_chart(fig)

#レーダーチャートの結果をポジションごとに保存
po_li = ["DF","MF","FW"]
for po in po_li:
    if po == "DF":
        df_score_DF,no_shootNumDF = appDef.addDFScore(df_DF)
    elif po == "MF":
        df_score_MF,no_shootNumMF = appDef.addMFScore(df_MF)
    else:
        df_score_FW,no_shootNumFW = appDef.addFWScore(df_FW)
