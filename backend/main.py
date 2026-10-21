from fastapi import FastAPI, Path
from enum import Enum

app=FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/about")
def about():
    return {"message": "This is my first FastAPI project"}

# with Path Parameters
@app.get("items/item_id")
async def read_item(item_id):
    return {"item_id": item_id}

# with Path Parameters and Type Annotations
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

# Order matters
@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}


@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}


# Predefined values
class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

@app.get("/models/{models_name}")
async def get_model(models_name: ModelName):   #Declaring the path parameter as a ModelName type will automatically validate the input against the enum values.
    if models_name== ModelName.alexnet:
        return {"model_name": models_name, "message": "Deep Learning FTW!"}
    if models_name== ModelName.resnet:
        return {"model_name": models_name, "message": "ResNet is great!"}
    if models_name== ModelName.lenet:
        return {"model_name": models_name, "message": "LeNet is classic!"}
    
    return {"model_name": models_name, "message": "Have some residuals!"}


# Query Parameters
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]

# Optional parameters
from typing import Optional

@app.get("/items/{item_id}")
async def read_item(item_id: str, q: Optional[str] = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}

# Multiple path and query parameters
@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, q: Optional[str] = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item

# Required query parameters
@app.get("/items/{item_id}")
async def read_user_item(item_id: str, needy: str):
    item = {"item_id": item_id, "needy": needy}
    return item