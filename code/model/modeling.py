
# coding: utf-8
import sys

import sqlite3
import joblib
import pandas as pd

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn import metrics


class Modeling:

    def __init__(self, db, output_model):
        self.db = db
        self.output_model = output_model

    
    def create_model(self):
        conn = sqlite3.connect(self.db)

        df = pd.read_sql("SELECT * FROM FEATURES WHERE APPEARENCES is not null", conn)
        print(df.head())

        df_info = df.drop(df.columns[[0]], axis=1)
        
        df_target = df_info['APPEARENCES']
        df_features = df_info.drop(df.columns[[-1]], axis=1)
        
        X_train, X_test, y_train, y_test = train_test_split(df_features, df_target, test_size=0.3, random_state=42, shuffle=True)
        rfr = RandomForestRegressor(n_estimators = 100, max_depth=10)  
        rfr.fit(X_train, y_train)

        y_pred = rfr.predict(X_test)
        meanSquaredError = metrics.mean_squared_error(y_test, y_pred)
        print(f"Mean Squared Error: {meanSquaredError}")
        
        joblib.dump(rfr, self.output_model)


if __name__ == "__main__":

    db = sys.argv[1]
    output_model = sys.argv[2]

    m = Modeling(db, output_model)
    m.create_model()

