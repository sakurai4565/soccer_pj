import get_data
import pandas as pd
#選手URL
url_list_team1_UK = [
  "https://soccer.yahoo.co.jp/ws/category/eng/teams/102706/players/2631?gk=52",
  "https://soccer.yahoo.co.jp/ws/category/eng/teams/102706/players/5094?gk=52",
  "https://soccer.yahoo.co.jp/ws/category/eng/teams/102706/players/2178?gk=52",
  "https://soccer.yahoo.co.jp/ws/category/eng/teams/102706/players/5102?gk=52",
  "https://soccer.yahoo.co.jp/ws/category/eng/teams/102706/players/13436?gk=52",
  "https://soccer.yahoo.co.jp/ws/category/eng/teams/102706/players/13437?gk=52",
  "https://soccer.yahoo.co.jp/ws/category/eng/teams/102706/players/13423?gk=52",
  "https://soccer.yahoo.co.jp/ws/category/eng/teams/102706/players/3501?gk=52",
  "https://soccer.yahoo.co.jp/ws/category/eng/teams/102706/players/4627?gk=52",
  "https://soccer.yahoo.co.jp/ws/category/eng/teams/102706/players/9834?gk=52",
  "https://soccer.yahoo.co.jp/ws/category/eng/teams/102706/players/10929?gk=52",
  "https://soccer.yahoo.co.jp/ws/category/eng/teams/102706/players/13430?gk=52",
  "https://soccer.yahoo.co.jp/ws/category/eng/teams/102706/players/13434?gk=52",
  "https://soccer.yahoo.co.jp/ws/category/eng/teams/102706/players/12912?gk=52",
  "https://soccer.yahoo.co.jp/ws/category/eng/teams/102706/players/1213?gk=52",
  "https://soccer.yahoo.co.jp/ws/category/eng/teams/102706/players/13420?gk=52",
  "https://soccer.yahoo.co.jp/ws/category/eng/teams/102706/players/13382?gk=52",
  "https://soccer.yahoo.co.jp/ws/category/eng/teams/102706/players/5046?gk=52",
  "https://soccer.yahoo.co.jp/ws/category/eng/teams/102706/players/2585?gk=52",
  "https://soccer.yahoo.co.jp/ws/category/eng/teams/102706/players/13435?gk=52",
  "https://soccer.yahoo.co.jp/ws/category/eng/teams/102706/players/13431?gk=52",
  "https://soccer.yahoo.co.jp/ws/category/eng/teams/102706/players/13429?gk=52",
  "https://soccer.yahoo.co.jp/ws/category/eng/teams/102706/players/10322?gk=52",
  "https://soccer.yahoo.co.jp/ws/category/eng/teams/102706/players/3506?gk=52",
  "https://soccer.yahoo.co.jp/ws/category/eng/teams/102706/players/5048?gk=52",
  "https://soccer.yahoo.co.jp/ws/category/eng/teams/102706/players/13292?gk=52",
  "https://soccer.yahoo.co.jp/ws/category/eng/teams/102706/players/13414?gk=52",
  "https://soccer.yahoo.co.jp/ws/category/eng/teams/102706/players/13425?gk=52",

]
#requestのデータを保存
player_data = get_data.get_url(url_list_team1_UK)
#print(player_data)


#listを改行
num_columns = 8
#例 [(0~7),(8~15),(16~23),...]  の2次元配列に変換
new_list = [player_data[i:i+num_columns] for i in range(0,len(player_data),num_columns)]
#２次元配列をDataFrameに変換
df = pd.DataFrame(new_list)
#dfをcsvに変換
df.to_csv("soccer_data.csv",encoding="utf_8_sig")

