from langchain_google_genai import ChatGoogleGenerativeAI
from extraiTextoPDF import ler_texto_arquivos_diretorio

textos = ler_texto_arquivos_diretorio("Arquivos_Processo")

d1 = str(textos["d1.pdf"])

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    temperature=0.1,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    api_key="AIzaSyBaIXXItFniZpqwvnKsgsUZyhItCvv0QOc",
    # other params...
)

messages = [
    (
        "system",
        "Faça um resumo desse processo administrativo baseado nesse texto.",
    ),
    ("human", f"{d1}"),
]
ai_msg = llm.invoke(messages)
print(ai_msg.content)
