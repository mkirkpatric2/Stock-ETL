from typing import Annotated
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from starlette import status
from database import engine, SessionLocal
from sqlalchemy import text

app = FastAPI()

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.get("/", status_code=status.HTTP_200_OK)
async def print_chars(db: db_dependency):

    with engine.connect() as con:
        rs = con.execute(text('select volume, date from msft '
                              'ORDER BY volume DESC LIMIT 1; '))
        rs_dict = rs.mappings().all()

    return rs_dict