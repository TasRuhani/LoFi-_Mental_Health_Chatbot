from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from chatbot import get_bot_response
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

class ChatInput(BaseModel):
    message: str
    music_recommended: bool

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/chat")
async def chat(input_data: ChatInput):
    response_data = get_bot_response(
        message=input_data.message,
        music_recommended=input_data.music_recommended
    )
    return JSONResponse(content=response_data)
