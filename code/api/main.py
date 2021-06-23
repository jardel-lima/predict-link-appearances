import sys
sys.path.append('..')
from fastapi import FastAPI
import joblib
import numpy as np

from util.db import DataBase
from features.features import Features

app = FastAPI()
db_location = "database/database.db"
model_location = "model/model.pkl"


@app.get("/")
async def root():
    return {"message": "Predict Link Appearance"}


@app.get("/link/features")
async def link_features(link: str):
    db = DataBase(db_location)
    result = db.get_link_features(link)

    if len(result) == 0:
        f = Features(link)
        result = f.get_features()
        f.insert_in_db(db_location)

    db.close()
    return {"link": link, "features": result}


@app.get("/link/appearances")
async def link_features(link: str):
    db = DataBase(db_location)
    db.create_table_predictions()
    result = db.get_link_predictions(link)
    
    if len(result) == 0:
        f = Features(link)
        features = f.get_features()
        f.insert_in_db(db_location)

        model = joblib.load(model_location)
        result = model.predict(np.array(features).reshape(1,-1))[0]
        result = round(result,0)

        db.insert_predictions(link, result)

    else:
        result = result[0][0]

    db.close()
    return {"link": link, "appearances": result}
