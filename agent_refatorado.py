from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

class AgentResumo:

    def __init__(self, api_key):
        self.llm = ChatGoogleGenerativeAI(
                model="gemini-1.5-pro",
                temperature=0.1,
                max_tokens=None,
                timeout=None,
                max_retries=2,
                api_key=api_key,
                # other params...
            )

    def gerar_resumo(self, texto):
        try:
            text_prompt = ChatPromptTemplate.from_messages(
                [
                    ("system", "Faça um resumo de cada documento. Pense passo a passo no sentido de: Quem foi que enviou o processo? Para quem foi enviado? Qual é o assunto principal do documento? E elenque esses pontos. Por fim, junte cada um dos resumos em um texto e me mostre. Não deixe de fazer esse resumo."),
                    ("human", "{input}")
                ]
            )

            parser = StrOutputParser()

            chain = text_prompt | self.llm | parser

            result = chain.invoke(
                {
                    "input": texto
                }
            )

            return result

        except Exception as e:
            return "Erro ao gerar o resumo."