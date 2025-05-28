from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_community.llms import LlamaCpp

app = FastAPI()

# Rota raiz para evitar erro 404
@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <h1>Simulador de Paciente com IA</h1>
    <p>Use o endpoint <code>/consulta</code> com método POST para interagir com o paciente simulado.</p>
    """

# Configuração do modelo LlamaCpp
llm = LlamaCpp(
    model_path="lmu.famerp.br/tiago/models/ggml-model-Q5_K_M.gguf",
    n_ctx=32768,
    n_batch=64,
    n_threads=4,
    temperature=0.7,
    max_tokens=256,
    verbose=False
)

# Memória de conversação
memory = ConversationBufferMemory()
conversation = ConversationChain(llm=llm, memory=memory)

# Prompt do paciente simulado
PACIENTE_PROMPT = """
Você é um paciente em uma consulta médica. 
Seu nome é João, 45 anos, pedreiro. 
Apresenta dor no peito há 3 semanas, piora ao esforço, irradia para braço esquerdo. 
Responda com naturalidade, como se estivesse conversando com um médico. 
Não mencione que é um modelo de linguagem ou IA.
"""

# Modelo de entrada da API
class ConsultaInput(BaseModel):
    pergunta: str

# Endpoint da consulta
@app.post("/consulta")
def consulta(input: ConsultaInput):
    prompt = f"{PACIENTE_PROMPT}\n\nMédico: {input.pergunta}\nPaciente:"
    resposta = conversation.predict(input=prompt)
    return {"resposta": resposta}

