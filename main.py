from extraiTextoPDF import ler_texto_arquivos_diretorio
from agent_refatorado import AgentResumo
from dotenv import load_dotenv
import os

load_dotenv(".env")
API_KEY = os.getenv("API_KEY")

agent = AgentResumo(api_key=API_KEY)
textos = ler_texto_arquivos_diretorio("Arquivos_Processo")

d1 = str(textos["d1.pdf"])

result = agent.gerar_resumo(d1)

print(result)


