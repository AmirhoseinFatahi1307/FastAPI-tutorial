from fastapi import (
    FastAPI,
    Query,
    status,
    HTTPException,
    Path,
    Form,
    Body,
    UploadFile,
    File,
)
from fastapi.responses import JSONResponse
import random
from typing import Annotated
from typing import Optional
from contextlib import asynccontextmanager
from dataclasses import dataclass


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application startup")
    yield
    print("Application shutdown")


app = FastAPI(lifespan=lifespan)


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
def retireve_names_list(
    q: Annotated[str | None, Query(alias="search", max_length=50)] = None,
):
    if q:
        return [item for item in names_list if item["name"] == q]
    return names_list


@dataclass
class Student:
    name: str
    age: int


@dataclass
class StudentResponse:
    id: int
    name: str
    age: int


# /names (GET(RETRIEVE), POST(CREATE))
@app.post("/names", status_code=status.HTTP_201_CREATED, response_model=StudentResponse)
async def create_name(student: Student):
    name_obj = {"id": random.randint(6, 100), "name": student.name}
    names_list.append(name_obj)
    return name_obj


# /names/:id (GET(RETRIEVE), PUT/PATCH(UPDATE), DELETE(DELETE))
@app.get("/names/{name_id}")
def retrieving_name_detail(
    name_id: int = Path(
        alias="Object_id",
        title="Object id",
        description="The id of the name in names-list",
    )
):
    for name in names_list:
        if name["id"] == name_id:
            return name["name"]
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Object not found"
    )


# /names/:id (GET(RETRIEVE), PUT/PATCH(UPDATE), DELETE(DELETE))
@app.put("/names/{name_id}", status_code=status.HTTP_200_OK)
def Update_name_detail(name_id: int = Path(), name: str = Form()):
    for item in names_list:
        if item["id"] == name_id:
            item["name"] = name
            return item
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Object not found"
    )


# /names (GET(RETRIEVE), POST(CREATE))
@app.delete("/names/{name_id}")
def Delete_name(name_id: int):
    for item in names_list:
        if item["id"] == name_id:
            names_list.remove(item)
            return JSONResponse(
                content={"Detail": "Object remove succssesfully "},
                status_code=status.HTTP_200_OK,
            )
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Object not found"
    )


@app.get("/")
def root():
    return JSONResponse(
        content={"Massage": "Hello World"}, status_code=status.HTTP_202_ACCEPTED
    )


# estefade az file va faghat haminja behesh dastresi darim vali dar uploadfile behine tar va behtare
# @app.post("/Upload_Files/")
# async def uploading_file(file :bytes = File(...)):
# return {"file size": len(file)}


@app.post("/Upload_Files/")
async def uploading_file(file: UploadFile = File(...)):
    content = await file.read()  # Asynchronous reading
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "file_size": len(content),
    }
