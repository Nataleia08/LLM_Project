import uvicorn
from typing import Callable

from fastapi import FastAPI, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi_limiter import FastAPILimiter
from sqlalchemy.orm import Session
from sqlalchemy import text
from starlette.middleware.cors import CORSMiddleware   #------------

from app.database.config import settings
from app.database.db import get_db
from app.routes import auth, llm_ws, upload_llm, users, history
from app.routes.auth import signup, login
from app.database.schemas import UserModel
from fastapi.security import OAuth2PasswordRequestForm
from app.services.auth import auth_service
from app.database.models import User

app = FastAPI()

templates = Jinja2Templates(directory='app/templates')
app.mount('/static', StaticFiles(directory='app/static'), name='static')


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse('index.html', {"request": request, "email": None, "password": None})


@app.post("/", response_class=HTMLResponse)
async def root(request: Request, email=Form(), password=Form(), db: Session = Depends(get_db)):
    new_user = db.query(User).filter(User.email==email).first()
    if new_user is None:
        new_user = await signup(UserModel(username=email, email=email, password=password), db)
    await login(OAuth2PasswordRequestForm(username=email, password=password), db)
    current_user = Depends(auth_service.get_current_user)
    return templates.TemplateResponse('upload.html', {"request": request, "current_user" : current_user})


@app.get("/api/healthchecker")
def healthchecker(db: Session = Depends(get_db)):
    try:
        # Make request
        result = db.execute(text("SELECT 1")).fetchone()
        if result is None:
            raise HTTPException(status_code=500, detail="Database is not configured correctly")
        return {"message": "Welcome to FastAPI!"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error connecting to the database")

app.include_router(auth.router, prefix="/api")
app.include_router(users.router, prefix="/api")
app.include_router(history.router, prefix="/api")
app.include_router(upload_llm.router, prefix="/api")
app.include_router(llm_ws.router, prefix="/api")


if __name__ == '__main__':
    # uvicorn.run(app, host='https://llm-project-2023.fly.dev', port=8000)
    uvicorn.run(app, host='localhost', port=8000)