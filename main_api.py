from fastapi import FastAPI, Request
from agent_refatorado import AgentResumo

class APIResumo():
    def __init__(self, agent):
        self.agent = agent

    async def fazer_resumo(self, request: Request):
        json = await request.json()
        link = json["link"]
        resumo = self.agent.make(link)
        retJson = {
            "message": resumo
        }

        return retJson



app = FastAPI()

agent = AgentResumo()
api_resumo = APIResumo(agent)

@app.post('/fazer_resumo')
async def fazer_resumo_endpoint(request: Request):
    return await api_resumo.fazer_resumo(request)

