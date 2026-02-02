import streamlit as st
import os
import sys
from dotenv import load_dotenv
import time
import json
from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title="🤖 Assistente RAG - Python Knowledge",
    page_icon="🐍",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Carregar variáveis de ambiente
load_dotenv()

# Configurações
CAMINHO_DB = "db"
PASTA_DOCUMENTOS = "base"

# Imports do projeto
try:
    from langchain_chroma.vectorstores import Chroma
    from langchain_openai import OpenAIEmbeddings
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_groq import ChatGroq
except ImportError as e:
    st.error(f"❌ Erro ao importar bibliotecas: {e}")
    st.stop()

# Configurações
CAMINHO_DB = "db"

# CSS para estilização
st.markdown(
    """
<style>
    /* Header styles */
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    
    /* Chat message styles with dark text */
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        color: #000000 !important;
    }
    .chat-message p, .chat-message span, .chat-message div {
        color: #000000 !important;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
        color: #000000 !important;
    }
    .user-message strong {
        color: #1565c0 !important;
    }
    .ai-message {
        background-color: #f3e5f5;
        border-left: 4px solid #9c27b0;
        color: #000000 !important;
    }
    .ai-message strong {
        color: #7b1fa2 !important;
    }
    
    /* Text input styles - ensure dark text */
    .stTextInput > div > div > input {
        background-color: #ffffff;
        color: #000000 !important;
        border: 2px solid #e0e0e0;
        font-size: 1rem;
    }
    .stTextInput > div > div > input::placeholder {
        color: #9e9e9e !important;
    }
    .stTextInput > label {
        color: #333333 !important;
        font-weight: 500;
    }
    
    /* Source and expander styles */
    .source-info {
        font-size: 0.85rem;
        color: #424242 !important;
        margin-top: 0.5rem;
    }
    .score-badge {
        background-color: #4caf50;
        color: white !important;
        padding: 0.2rem 0.5rem;
        border-radius: 0.3rem;
        font-size: 0.8rem;
        font-weight: bold;
    }
    
    /* Streamlit expander styles - ensure dark text */
    .streamlit-expanderHeader {
        color: #333333 !important;
        font-weight: 500;
    }
    .streamlit-expanderContent {
        color: #333333 !important;
    }
    
    /* General text colors */
    p, span, div, label {
        color: #333333;
    }
    
    /* Button styles */
    .stButton > button {
        font-weight: 500;
    }
    
    /* Caption styles */
    .stCaption {
        color: #666666 !important;
        font-size: 0.85rem;
    }
</style>
""",
    unsafe_allow_html=True,
)


# Função para verificar se o banco de dados existe
@st.cache_resource(show_spinner=False)
def carregar_banco_dados():
    """Carrega o banco vetorial com cache para performance."""
    if not os.path.exists(CAMINHO_DB):
        st.error("❌ Banco de dados não encontrado! Execute `python db.py` primeiro.")
        return None

    try:
        embeddings = OpenAIEmbeddings()
        db = Chroma(persist_directory=CAMINHO_DB, embedding_function=embeddings)
        return db
    except Exception as e:
        st.error(f"❌ Erro ao carregar banco de dados: {e}")
        return None


# Função para verificar documentos disponíveis
def verificar_documentos():
    """Verifica quais documentos PDF estão disponíveis."""
    if not os.path.exists(PASTA_DOCUMENTOS):
        return []

    documentos = []
    for arquivo in os.listdir(PASTA_DOCUMENTOS):
        if arquivo.endswith(".pdf"):
            caminho_completo = os.path.join(PASTA_DOCUMENTOS, arquivo)
            tamanho_mb = os.path.getsize(caminho_completo) / (1024 * 1024)
            documentos.append(
                {
                    "nome": arquivo,
                    "tamanho": f"{tamanho_mb:.1f} MB",
                    "caminho": caminho_completo,
                }
            )

    return documentos


# Função para buscar informações do sistema
def obter_info_sistema(db):
    """Obtém informações detalhadas sobre o banco de dados."""
    if db is None:
        return {}

    try:
        # Tenta obter informações da coleção
        info = {}

        # Tamanho do banco
        if os.path.exists(f"{CAMINHO_DB}/chroma.sqlite3"):
            tamanho_bytes = os.path.getsize(f"{CAMINHO_DB}/chroma.sqlite3")
            info["tamanho_banco"] = f"{tamanho_bytes / (1024 * 1024):.1f} MB"

        # Documentos disponíveis
        info["documentos"] = verificar_documentos()
        info["num_documentos"] = len(info["documentos"])

        # Configurações de modelo
        info["embedding_model"] = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
        info["llm_model"] = os.getenv("LLM_MODEL", "gpt-3.5-turbo")

        return info
    except Exception as e:
        st.error(f"Erro ao obter informações: {e}")
        return {}


# Função para processar a pergunta
def processar_pergunta(pergunta, db, k_docs=4, temperature=0.1):
    """Processa uma pergunta usando o sistema RAG com parâmetros configuráveis."""
    try:
        start_time = time.time()

        # Mostrar spinner durante processamento
        with st.spinner("🔍 Buscando informações no banco de conhecimento..."):
            # Buscar documentos similares
            resultados = db.similarity_search_with_relevance_scores(pergunta, k=k_docs)

        if not resultados:
            return (
                "Não encontrei informações relevantes para sua pergunta nos documentos disponíveis.",
                [],
                0.0,
            )

        # Construir contexto
        contexto = ""
        fontes = []

        for i, (doc, score) in enumerate(resultados):
            contexto += f"\n📄 **Documento {i + 1}** (Similaridade: {score:.3f}):\n{doc.page_content}\n"
            fontes.append(
                {
                    "conteudo": doc.page_content[:300] + "...",
                    "fonte": doc.metadata.get("source", "Desconhecido"),
                    "score": score,
                    "pagina": doc.metadata.get("page", "N/A"),
                    "chunk_id": i + 1,
                }
            )

        # Gerar resposta com LLM
        with st.spinner("🤖 Gerando resposta com IA..."):
            prompt_template = """Você é um assistente inteligente especialista em Python que ajuda os usuários com suas perguntas com base nos documentos fornecidos.

**PERGUNTA DO USUÁRIO:**
{pergunta}

**CONTEXTO DISPONÍVEL (Base de Conhecimento):**
{base_conhecimento}

**INSTRUÇÕES ESPECÍFICAS:**
1. Responda APENAS com base nas informações fornecidas nos documentos acima
2. Se a informação não estiver disponível, responda claramente: "Desculpe, não encontrei essa informação específica nos documentos disponíveis."
3. Seja claro, direto e educativo na sua resposta
4. Use exemplos práticos quando os documentos fornecerem
5. Estruture sua resposta em parágrafos curtos e fáceis de ler
6. Seja honesto sobre as limitações do conhecimento disponível

**RESPOSTA:**"""

            prompt = ChatPromptTemplate.from_template(prompt_template)

            # Configurar modelo com GROQ (gratuito e ultra-rápido)
            groq_api_key = os.getenv("GROQ_API_KEY")
            groq_model = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

            if not groq_api_key:
                return "❌ Erro: GROQ_API_KEY não configurada no arquivo .env", [], 0.0

            chat = ChatGroq(
                temperature=temperature,
                model=groq_model,
                api_key=groq_api_key,
            )
            chain = prompt | chat
            response = chain.invoke(
                {"pergunta": pergunta, "base_conhecimento": contexto}
            )

        processing_time = time.time() - start_time
        return response.content, fontes, processing_time

    except Exception as e:
        return f"❌ Erro ao processar pergunta: {str(e)}", [], 0.0


def verificar_banco_dados():
    """Retorna (True, db) se o banco estiver carregado, caso contrário (False, None)."""
    db = carregar_banco_dados()
    if db is None:
        return False, None
    return True, db


# Função principal
def main():
    # Header
    st.markdown(
        '<div class="main-header">🤖 Assistente RAG</div>', unsafe_allow_html=True
    )
    st.markdown(
        '<div class="sub-header">Consulte o conhecimento sobre Python com IA</div>',
        unsafe_allow_html=True,
    )

    # Sidebar com informações
    with st.sidebar:
        st.header("📊 Informações do Sistema")

        # Verificar API Key
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            st.success("✅ API Key configurada")
            st.write(f"**Key:** {api_key[:10]}...")
        else:
            st.error("❌ API Key não encontrada")
            st.info("Configure a variável OPENAI_API_KEY no arquivo .env")

        st.divider()

        # Status do banco de dados
        st.header("🗄️ Banco de Dados")
        if os.path.exists(CAMINHO_DB):
            st.success("✅ Banco de dados encontrado")

            # Tentar carregar e mostrar informações
            try:
                embeddings = OpenAIEmbeddings()
                db = Chroma(persist_directory=CAMINHO_DB, embedding_function=embeddings)

                # Contar documentos (se possível)
                st.info("📊 Banco de dados carregado com sucesso")

            except Exception as e:
                st.error(f"❌ Erro ao carregar banco: {e}")
        else:
            st.error("❌ Banco de dados não encontrado")
            st.code("python db.py")

        st.divider()

        # Informações do modelo
        st.header("🤖 Modelo de Chat")
        groq_model = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

        st.success(f"✅ {groq_model}")
        st.write("🚀 Groq - Inferência Ultra-Rápida")
        st.write("🆓 Modelo Gratuito")
        st.write("⚡ Respostas em milissegundos")

        if groq_api_key := os.getenv("GROQ_API_KEY"):
            st.caption(f"🔑 API Key: {groq_api_key[:10]}...")

        st.divider()

        # Informações do projeto
        st.header("ℹ️ Sobre o Projeto")
        st.write("""
        **Sistema RAG com LangChain**
        
        - 📚 Baseado em documentos PDF
        - 🧠 Busca semântica avançada
        - 🤖 Respostas geradas por IA
        - 🔍 Fontes sempre citadas
        """)

        st.divider()

        # Link do projeto
        st.header("🔗 Links")
        st.markdown("""
        [📂 Repositório GitHub](https://github.com/LucasSantos96/rag_langchain)
        
        [🎥 Vídeo Tutorial](https://www.youtube.com/watch?v=0M8iO5ykY-E)
        """)

        st.divider()

        # Estatísticas
        st.header("📈 Como Funciona")
        st.write("""
        1. 📄 Sua pergunta é convertida em embedding
        2. 🔍 Busca nos documentos por similaridade
        3. 📄 Contexto relevante é recuperado
        4. 🤖 IA gera resposta baseada no contexto
        """)

    # Área principal
    st.header("💬 Faça sua Pergunta")

    # Input da pergunta
    col1, col2 = st.columns([4, 1])

    with col1:
        pergunta = st.text_input(
            "Digite sua pergunta sobre Python:",
            placeholder="Ex: O que é programação orientada a objetos?",
            key="input_pergunta",
        )

    with col2:
        st.write("")
        st.write("")
        if st.button("🔍 Perguntar", type="primary"):
            if not pergunta.strip():
                st.warning("⚠️ Por favor, digite uma pergunta.")
            else:
                # Verificar banco de dados
                resultado, db = verificar_banco_dados()
                if resultado:
                    # Processar pergunta
                    resposta, fontes, processing_time = processar_pergunta(pergunta, db)

                    # Salvar no histórico
                    if "historico" not in st.session_state:
                        st.session_state.historico = []

                    st.session_state.historico.append(
                        {
                            "pergunta": pergunta,
                            "resposta": resposta,
                            "fontes": fontes,
                            "timestamp": time.time(),
                            "processing_time": processing_time,
                        }
                    )

    # Exibir histórico
    if "historico" in st.session_state and st.session_state.historico:
        st.divider()
        st.header("📜 Histórico de Conversas")

        # Exibir em ordem reversa (mais recente primeiro)
        for i, conversa in enumerate(reversed(st.session_state.historico)):
            with st.container():
                # Pergunta do usuário
                st.markdown(
                    f"""
                <div class="chat-message user-message">
                    <strong>👤 Você:</strong> {conversa["pergunta"]}
                </div>
                """,
                    unsafe_allow_html=True,
                )

                # Resposta da IA
                st.markdown(
                    f"""
                <div class="chat-message ai-message">
                    <strong>🤖 Assistente:</strong> {conversa["resposta"]}
                </div>
                """,
                    unsafe_allow_html=True,
                )

                # Fontes e scores
                if conversa["fontes"]:
                    with st.expander(
                        f"📚 Fontes e Relevância ({len(conversa['fontes'])} documentos)"
                    ):
                        for j, fonte in enumerate(conversa["fontes"]):
                            st.markdown(
                                f"""
                            <div style="border-left: 3px solid #2196f3; padding-left: 1rem; margin-bottom: 0.5rem;">
                                <strong>Fonte {j + 1}:</strong> {fonte["fonte"]}
                                <span class="score-badge">Score: {fonte["score"]:.3f}</span>
                                <br>
                                <em>{fonte["conteudo"]}</em>
                            </div>
                            """,
                                unsafe_allow_html=True,
                            )

                # Tempo de processamento
                if "processing_time" in conversa:
                    st.caption(f"⚡ Processado em {conversa['processing_time']:.2f}s")

                st.divider()

    # Limpar histórico
    if "historico" in st.session_state and st.session_state.historico:
        if st.button("🗑️ Limpar Histórico"):
            st.session_state.historico = []
            st.rerun()

    # Footer
    st.markdown("---")
    st.markdown(
        """
    <div style="text-align: center; color: #666; font-size: 0.9rem;">
        🤖 Powered by <strong>LangChain + Groq (Llama 3.1) + ChromaDB</strong> | 
        📚 Projeto RAG Completo | 
        🔗 <a href="https://github.com/LucasSantos96/rag_langchain" target="_blank">GitHub</a>
    </div>
    """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
