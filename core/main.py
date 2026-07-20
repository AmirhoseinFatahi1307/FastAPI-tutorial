from fastapi import FastAPI
import random
from typing import Optional

app = FastAPI()


names_list = [
    {"id": 1, "name": "ali"},
    {"id": 2, "name": "amir"},
    {"id": 3, "name": "maryam"},
    {"id": 4, "name": "mobina"},
    {"id": 5, "name": "mmad"},
    {"id": 7, "name": "ali"},
    {"id": 6, "name": "ali"},
]


# /names (GET(RETRIEVE), POST(CREATE))
@app.get("/names")
def retireve_names_list(q: Optionale[str] = None):
    if q:
        return [item for item in names_list if item["name"] == q]
    return names_list


# /names (GET(RETRIEVE), POST(CREATE))
@app.post("/names")
def create_name(name: str):
    name_obj = {"id": random.randint(6, 100), "name": name}
    names_list.append(name_obj)
    return f"id : {name_obj["id"]} and name : {name_obj["name"]}"


# /names/:id (GET(RETRIEVE), PUT/PATCH(UPDATE), DELETE(DELETE))
@app.get("/names/{name_id}")
def retrieving_name_detail(name_id: int):
    for name in names_list:
        if name["id"] == name_id:
            return name["name"]
    else:
        return "Detail : Object not found"


# /names/:id (GET(RETRIEVE), PUT/PATCH(UPDATE), DELETE(DELETE))
@app.put("/names/{name_id}")
def Update_name_detail(name_id: int, name: str):
    for item in names_list:
        if item["id"] == name_id:
            item["name"] = name
            return item
    return "Object not found"


# /names (GET(RETRIEVE), POST(CREATE))
@app.delete("/names/{name_id}")
def Delete_name(name_id: int):
    for item in names_list:
        if item["id"] == name_id:
            names_list.remove(item)
            return "Detail : Object remove succssesfully "
    return "Object not found"


@app.get("/")
def root():
    return {"message": "Hello World"}
