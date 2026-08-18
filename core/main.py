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
    Depends,
)
from fastapi.responses import JSONResponse
import random
from typing import Annotated
from typing import Optional
from contextlib import asynccontextmanager
from dataclasses import dataclass
from schemas import PersonCreateSchema, PersonResponseSchema, PersonUpdateSchema
from typing import List
from database import Base, engine, get_db, Person
from sqlalchemy.orm import session


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application startup")
    Base.metadata.create_all(engine)
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
@app.get("/names", response_model=List[PersonResponseSchema])
def retireve_names_list(
    q: Annotated[
        str | None,
        Query(
            deprecated=True,
            alias="search",
            description="it will be searched with the title you provided",
            example="ali",
            max_length=50,
        ),
    ] = None,
    db: session = Depends(get_db),
):
    query = db.query(Person)
    if q:
        query = query.filter_by(name=q)
    result = query.all()
    return result
    # if q:
    # return [item for item in names_list if item["name"] == q]
    # return names_list


# /names (GET(RETRIEVE), POST(CREATE))
@app.post(
    "/names", status_code=status.HTTP_201_CREATED, response_model=PersonResponseSchema
)
async def create_name(
    request: PersonCreateSchema,
    db: session = Depends(get_db),
):
    # name_obj = {"id": random.randint(6, 100), "name": person.name}
    # names_list.append(name_obj)
    new_person = Person(name=request.name)
    db.add(new_person)
    db.commit()
    db.refresh(new_person)
    return new_person


# /names/:id (GET(RETRIEVE), PUT/PATCH(UPDATE), DELETE(DELETE))
@app.get("/names/{name_id}", response_model=PersonResponseSchema)
async def retrieving_name_detail(
    name_id: int = Path(
        title="Object id",
        description="The id of the name in names-list",
    ),
    db: session = Depends(get_db),
):
    query = db.query(Person).filter_by(id=name_id).one_or_none()
    if query:
        return query
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Object not found"
        )
    # for name in names_list:
    # if name["id"] == name_id:
    # return name["name"]
    # raise HTTPException(
    # status_code=status.HTTP_404_NOT_FOUND, detail="Object not found"
    # )


# /names/:id (GET(RETRIEVE), PUT/PATCH(UPDATE), DELETE(DELETE))
@app.put(
    "/names/{name_id}",
    status_code=status.HTTP_200_OK,
    response_model=PersonResponseSchema,
)
def Update_name_detail(
    request: PersonUpdateSchema, name_id: int = Path(), db: session = Depends(get_db)
):
    person = db.query(Person).filter_by(id=name_id).one_or_none()
    if person:
        person.name = request.name
        db.commit()
        db.refresh(person)
        return person
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Object not found"
        )
    # for item in names_list:
    # if item["id"] == name_id:
    # item["name"] = person.name
    # return item
    # raise HTTPException(
    #  status_code=status.HTTP_404_NOT_FOUND, detail="Object not found"
    # )


# /names (GET(RETRIEVE), POST(CREATE))
@app.delete("/names/{name_id}")
def Delete_name(name_id: int, db: session = Depends(get_db)):
    person = db.query(Person).filter_by(id=name_id).one_or_none()
    if person:
        db.delete(person)
        db.commit()
        return JSONResponse(content={"Detail": "Object remove succssesfully "})
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Object not found"
        )
    # for item in names_list:
    # if item["id"] == name_id:
    # names_list.remove(item)
    # return JSONResponse(
    # content={"Detail": "Object remove succssesfully "},
    # status_code=status.HTTP_200_OK,
    # raise HTTPException(
    # status_code=status.HTTP_404_NOT_FOUND, detail="Object not found"


# )


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
