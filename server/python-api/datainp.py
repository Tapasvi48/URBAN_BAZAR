from pydantic import BaseModel
from typing import List
class USER(BaseModel):
    user_id:str

class PRODUCTID(BaseModel):
    product_id:str






class UserInput(BaseModel):
    user_visited_items: List[str]
    top_n: int = 5




# sub cat brand user_id item_id
class PRODUCT(BaseModel):
    sub_cat:List[str]
    brand:List[str]
    user_id:List[str]
    item_id:List[str]



class TrainDataInput(BaseModel):
    sub_cat:List[str]
    brand:List[str]
    item_id:List[str]
    user_id:List[str]
    visited_count:List[str]

class TrainDataInputem(BaseModel):
    sub_cat:List[str]
    brand:List[str]
    item_id:List[str]






