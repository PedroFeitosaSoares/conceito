from fastapi import FastAPI, Request
from main import make

app = FastAPI()

@app.post('/fazer_resumo')
async def fazer_resumo(request: Request):
    json = await request.json()

    link = json["link"]

    resumo = make(link)

    retJson = {
        "message": resumo
    }

    return retJson

