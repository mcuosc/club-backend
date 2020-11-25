from typing import Optional

from fastapi import FastAPI, Form

from pydantic import BaseModel

from fastapi.openapi.utils import get_openapi
import pandas as pd

app = FastAPI(
    title="MCU-OSC"
)
"""
uvicorn main:app --reload --host 0.0.0.0
"""

@app.get("/")
def read_root():
    return {"Hello": "World"}

class Student_check(BaseModel):
    id: str
    code: str
    #code: Optional[str] = None
    
@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    return {"username": username}
    
@app.post("/api/ClassCheck")
async def login(student: Student_check):
    if student.code == 'mcu':
        df = pd.read_csv('usr.csv', index_col=0)
        try:
            if int(student.id) in df.index:
                return {"msg":"found"}
            else:
                return {"msg":"not found"}
        except:
            return {"msg":"input error"}
    #if student.id=='aaa':
    #    return {"msg":"bbb"}
    else:
        return {"msg":"code error"}
"""
@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}
"""

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="MCU-OSC backend-api",
        version="1.0.0",
        description="if you have any questions, please contract alanhc.tseng1999@gmail.com",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi