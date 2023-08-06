from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from bot import Retriever, llm_reply
from pydantic import BaseModel


class ChatModel(BaseModel):
    query: str


app = FastAPI()

try:
    app.mount(
        "/static",
        StaticFiles(directory="../frontend", html=True),
        name="static",
    )

    templates = Jinja2Templates(directory="../frontend")
except RuntimeError:
    pass


@app.get("/")
def root(request: Request):
    return templates.TemplateResponse("index.html", context={"request": request})


@app.post("/chat")
def chat(cm: ChatModel):
    query = cm.query

    r = Retriever(
        source="Mercedes-Benz-A-Class-Limousine.csv", searchable_column="content"
    )
    context = r.retrieve(query)
    prompt = context + "\n" + "Query:" + query
    return llm_reply(prompt=prompt)
