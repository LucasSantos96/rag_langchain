from langchain_chroma.vectorstores import Chroma 
from langchain_openai import OpenAIEmbeddings 
from dotenv import load_dotenv 
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
load_dotenv()

CAMINHO_DB = "db"

prompt_template = """ 
Você é um assistente inteligente que ajuda os usuários com suas perguntas com base em documentos fornecidos:
{pergunta}

Utilize as informações do documentos para responder à pergunta acima. Forneça respostas detalhadas e precisas:

{base_conhecimento}

"""

def perguntar():
    pergunta = input("Digite sua pergunta: ")

    # carregar o banco de dados vetorizado
    func_embedding = OpenAIEmbeddings()

    db = Chroma(persist_directory=CAMINHO_DB, embedding_function=func_embedding)

    # comparar a pergunta do usuário (embedding) com os documentos no banco de dados
    resultados = db.similarity_search_with_relevance_scores(pergunta, k=3)

    if len(resultados) == 0 or resultados[0][1] < 0.7:
        print("Desculpe, não sei a resposta para essa pergunta.")
        return

    
    textos_resultado = []
    for resultado in resultados:
        texto = resultado[0].page_content
        textos_resultado.append(texto)

    base_conhecimento = "\n\n----\n\n".join(textos_resultado)


    prompt = ChatPromptTemplate.from_template(prompt_template)
    prompt = prompt.invoke({"pergunta": pergunta, "base_conhecimento": base_conhecimento})
    #print(prompt)

    modelo = ChatOpenAI()
    texto_resposta = modelo.invoke(prompt)
    print("Resposta da ia:" , texto_resposta.content)
perguntar()   

