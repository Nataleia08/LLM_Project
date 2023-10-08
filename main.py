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
from fastapi.websockets import WebSocket
from langchain.vectorstores import FAISS
from langchain.llms.openai import OpenAI, AzureOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from app.repository.llm import create_llm, question_from_llm
from app.database.config import OPENAI_API_KEY
from langchain.chains.question_answering import load_qa_chain

from app.routes import auth, users, history, upload, chat


app = FastAPI()

templates = Jinja2Templates(directory='app/templates')
app.mount('/static', StaticFiles(directory='app/static'), name='static')


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse('index.html', {"request": request})

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    new_memory = FAISS.load_local("/LLM_PROJECT/Data/llm.yaml", embeddings=OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY))
    new_llm = AzureOpenAI(temperature=0.5, max_tokens=500) 
    llm_chain = load_qa_chain(new_llm, chain_type="refine")
    await websocket.accept()
    await websocket.send_text("Welcome to the chat!")
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"You question: {data}")
            # await repository_history.create_message(chat_id, user_id, data, db)
            answer = llm_chain({"input_documents": new_memory, "question": data, "language": "English", "existing_answer" : ""}, return_only_outputs=True)
            await websocket.send_text(f"Answer: {answer}")
            # await websocket.send_text(f"Answer 2: {new_memory.similarity_search(data)}")
            
    except:
        await websocket.close()
        return templates.TemplateResponse("start_chat")


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
app.include_router(upload.router, prefix="/api")
app.include_router(chat.router, prefix="/api")



if __name__ == '__main__':
    # uvicorn.run(app, host='https://llm-project-2023.fly.dev', port=8000)
    #uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)
    uvicorn.run(app, host='localhost', port=8000)
