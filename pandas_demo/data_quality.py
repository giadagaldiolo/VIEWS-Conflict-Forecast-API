import pandas as pd
from sklearn.ensemble import IsolationForest

def main():
    df = pd.read_csv("sample_data.csv")  # 適当なCSV用意してね

    print("欠損値チェック")
    print(df.isnull().sum())

    clf = IsolationForest(random_state=42)
    df['anomaly'] = clf.fit_predict(df.select_dtypes(include=['float64', 'int64']))

    print("異常検知結果（anomaly = -1が異常）")
    print(df[df['anomaly'] == -1])

if __name__ == "__main__":
    main()
