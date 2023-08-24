import uvicorn
from fastapi import FastAPI
from datainp import  USER
from pydantic import BaseModel
from datainp import  PRODUCT
from datainp import PRODUCTID
from datainp import  TrainDataInput
from datainp import  TrainDataInputem
from datainp import  UserInput
from typing import List,Dict
from content import *
import numpy as np
import pickle
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware
from content import *
from Item2 import *
from demo import *


app=FastAPI()
origins = [
    "http://localhost:3000",
    "localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get('/')
def index():
    return {'message':'hellosd'}


@app.post("/train")
def train_model(data: TrainDataInput):
    data_dict = {
        "sub_cat": data.sub_cat,
        "brand": data.brand,
        "item_id": data.item_id,
        "visited_count":data.visited_count,
        "user_id":data.user_id
    }
    df=pd.DataFrame(data_dict)
    item_item_recommender=ItemItemRecommender(df)
    with open("res3", 'wb') as pickle_out:
        pickle.dump(item_item_recommender,pickle_out)
    return {"dataframe":df}

class PredictInput(BaseModel):
    user_visited_items: List[str]
    top_n: int = 5



@app.post("/predict1")
def predict_recommendations(data:USER):
    pickle_in = open("res3", "rb")
    item_item_recommender=pickle.load(pickle_in)
    recommendations=item_item_recommender.get_recommendations(
        data.user_id
    )
    item_ids=[item for item in recommendations]
    return {"recommended_items":item_ids}




@app.post("/train3")
def train_modelll(data: TrainDataInputem):
    data_dict = {
        "sub_cat": data.sub_cat,
        "brand": data.brand,
        "item_id": data.item_id,


    }
    df=pd.DataFrame(data_dict)
    collab_recommender=CollabBasedRecommender(df)
    with open("res5",'wb') as pickle_out:
        pickle.dump(collab_recommender,pickle_out)
    return {"dataframe":df}

class PredictInput(BaseModel):
    user_visited_items:List[str]
    top_n: int=5



@app.post("/predict3")
def predict_recommendddd(data:PRODUCTID):
    pickle_in=open("res5","rb")
    collab_recommender=pickle.load(pickle_in)
    recommendations=collab_recommender.get_recommendation(
        data.product_id
    )
    return {"recommended_items":recommendations}



@app.post('/predict')
def predict_output(data:USER):
    print("yeloo")
    pickle_in=open("res9", "rb")
    content_recommender=pickle.load(pickle_in)
    recommendation=content_recommender.get_recommendations(data.user_id)
    return {"recommendation":recommendation}





@app.post('/postdetail')
def post_data(data:PRODUCT):
    data_dict = {
        "sub_cat": data.sub_cat,
        "brand": data.brand,
        "user_id":data.user_id,
        "item_id": data.item_id
    }

    # Create a DataFrame from the dictionary
    df=pd.DataFrame(data_dict)

    content_recommender=ContentBasedRecommender(df)
    with open("res9",'wb') as pickle_out:
        pickle.dump(content_recommender,pickle_out)

    return {"dataframe":df}













if __name__=='__main__':
    uvicorn.run(app,host='127.0.0.1',port=8000)





