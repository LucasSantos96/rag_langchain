from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

PASTA_BASE = "base"


def create_db():
    # carregar documentos
    documents = load_documents()

    # dividir os documentos em pedaços menores (chunks)
    chunks = split_documents(documents)

    # vetorização dos pedaços com embeddings
    vetorizar_chunks(chunks)


def load_documents():
    loader = PyPDFDirectoryLoader(PASTA_BASE)
    documents = loader.load()
    return documents


def split_documents(documents):
    docs_separator = RecursiveCharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=500,
        length_function=len,
        add_start_index=True,
    )
    chunks = docs_separator.split_documents(documents)
    print(len(chunks))
    return chunks


def vetorizar_chunks(chunks):

    db = Chroma.from_documents(chunks, OpenAIEmbeddings(), persist_directory="db")
    print("Salvando vetorização no disco...")


create_db()
