import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage # As mensagens que o usuário envia e as mensagens do sistema (instruções para o modelo)
from langchain_core.output_parsers import StrOutputParser # Parser para garantir que a saída seja uma string
from langchain_ollama.chat_models import ChatOllama # A classe que interage com o modelo de linguagem do Ollama
from langchain_core.prompts import ChatPromptTemplate # Para criar templates de prompts de chat


load_dotenv()
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "localhost")
OLLAMA_BASE_URL = f"http://{OLLAMA_HOST}:11434"
MODEL = os.getenv("INFERENCE_MODEL", "mistral")
base_url = OLLAMA_BASE_URL

model = ChatOllama(model=MODEL, temperature=0.5, base_url=base_url)
parser = StrOutputParser()

message_template = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant that translates {FROM} to {TO}. If the text is in another language, respond that you can only translate between {FROM} and {TO}, and that the user should change the selected language. Answer with only the translation, without any additional text."),
    ("user", "{text}")
])

chain = message_template | model | parser
