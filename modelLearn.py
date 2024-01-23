from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import cross_val_score
import pickle
import pandas as pd

df_result = pd.read_csv("df_result.csv")

#データをtrainとtestに分割
features = ["Team1", "Team2",  "ATT_diff", "MID_diff", "DEF_diff","OVR_diff"]
X = df_result[features]
y = df_result["Result"]
# データをトレーニングセットとテストセットに分割
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#ロジスティクス回帰モデル作成
# ロジスティック回帰モデルの初期化と学習
lg = LogisticRegression(random_state=42, solver='sag', max_iter=3000)
lg.fit(X_train, y_train)

# テストデータでの予測
y_pred = lg.predict(X_test)

# モデルの評価
accuracy = accuracy_score(y_test, y_pred)
print('Accuracy:', accuracy)

# 分類レポートの表示
print("Classification Report:")
print(classification_report(y_test, y_pred))


#学習モデルの保存
with open('model.pickle', mode='wb') as f:
    pickle.dump(lg,f,protocol=2)