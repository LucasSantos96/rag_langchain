# 🤖 Projeto RAG com LangChain - Agente de IA Completo

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![LangChain](https://img.shields.io/badge/LangChain-0.1+-green)](https://python.langchain.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.53+-red)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> 📚 **Projeto de estudos baseado no vídeo:** [Agente de IA completo com Python - Projeto RAG com Langchain](https://www.youtube.com/watch?v=0M8iO5ykY-E) por Hashtag Programação

## 🌐 Deploy Online

🚀 **Aplicação disponível em:** http://localhost:8501 *(rodando localmente)*

💡 Para deploy em produção, considere usar [Streamlit Cloud](https://streamlit.io/cloud) ou [Railway](https://railway.app/)

## 🎯 Sobre o Projeto

Sistema completo de agente de IA baseado em arquitetura **RAG** (Retrieval-Augmented Generation) para responder perguntas usando documentos PDF como base de conhecimento.

### 🚀 Funcionalidades Principais

- ✅ **Interface Web com Streamlit** - Interface moderna e intuitiva
- ✅ **Processamento automático de PDFs** - Extração e chunking inteligente
- ✅ **Busca semântica avançada** - Encontra conteúdo relevante por significado
- ✅ **Banco vetorial persistente** - ChromaDB para armazenamento eficiente
- ✅ **Suporte a múltiplos documentos** - Processa vários PDFs simultaneamente
- ✅ **Controle de alucinações** - Responde apenas com base nos documentos
- ✅ **Histórico de conversas** - Mantém contexto das perguntas anteriores
- ✅ **Score de relevância** - Mostra quais documentos foram usados
- ✅ **Integração com Groq** - Modelo Llama 3.1 gratuito e ultra-rápido

## 🏗️ Arquitetura RAG

```
📄 PDFs → 🧠 Embeddings → 🗄️ ChromaDB → 🔍 Busca → 🤖 LLM → 💬 Resposta
```

1. **Indexação**: Documentos PDF são convertidos em vetores numéricos (embeddings)
2. **Armazenamento**: Vetores salvos no ChromaDB para busca eficiente
3. **Consulta**: Pergunta convertida em embedding e comparada com a base
4. **Recuperação**: Documentos mais similares são recuperados
5. **Geração**: Contexto recuperado alimenta o LLM para resposta precisa

## 📁 Estrutura do Projeto

```
rag_langchain/
├── app.py              # 🎨 Interface web Streamlit (RECOMENDADO)
├── main.py             # Interface terminal de consulta RAG
├── db.py               # Processamento e vetorização de documentos
├── .env                # Configuração de API keys
├── requirements.txt    # Dependências do projeto
├── base/               # 📂 Diretório com documentos PDF
├── db/                 # 🗄️ Banco vetorial ChromaDB (auto-gerado)
├── docs/               # 📚 Documentação e tutoriais
└── venv/               # Ambiente virtual Python
```

## 🚀 Como Começar

### 📋 Pré-requisitos

- Python 3.8 ou superior
- API Key da OpenAI ou OpenRouter
- Git para clonar o repositório

### 1. Clonar o Repositório

```bash
git clone https://github.com/LucasSantos96/rag_langchain.git
cd rag_langchain
```

### 2. Configurar Ambiente Virtual

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar (Linux/Mac)
source venv/bin/activate

# Ativar (Windows)
venv\Scripts\activate
```

### 3. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar API Key

Crie um arquivo `.env` com sua configuração:

**Opção 1: Groq (Recomendado - Gratuito e Ultra-rápido)** 🚀
```bash
# Crie conta gratuita em: https://console.groq.com
GROQ_API_KEY=gsk-sua-key-aqui
GROQ_MODEL=llama-3.1-8b-instant

# Embeddings via OpenRouter (gratuito)
OPENAI_API_KEY=sk-or-v1-sua-key-aqui
OPENAI_BASE_URL=https://openrouter.ai/api/v1
OPENAI_MODEL=qwen/qwen3-embedding-0.6b
```

**Opção 2: OpenAI (Pago)** 💰
```bash
OPENAI_API_KEY=sk-sua-key-aqui
EMBEDDING_MODEL=text-embedding-3-small
LLM_MODEL=gpt-3.5-turbo
```

### 5. Adicionar Documentos

Coloque seus arquivos PDF na pasta `base/`:

```bash
# Exemplo:
cp seus-documentos/*.pdf base/
```

### 6. Processar Documentos

```bash
python db.py
```

**Saída esperada:**
```
245
Salvando vetorização no disco...
```

### 7. Fazer Consultas

#### Opção A: Interface Web (Recomendado) 🎨
```bash
streamlit run app.py
```

A interface web será aberta em `http://localhost:8501` com:
- 🎨 **Interface moderna e intuitiva**
- 💬 **Histórico completo de conversas**
- 📚 **Visualização detalhada das fontes**
- 🔍 **Score de relevância dos documentos**
- 📊 **Status do sistema em tempo real**

#### Opção B: Interface Terminal 🖥️
```bash
python main.py
```

**Exemplo de uso:**
```
Digite sua pergunta: O que é herança em Python?

[
    (Document(page_content='Herança é um dos pilares...', metadata={'source': 'base/FAQ Python Video YouTube.pdf'}), 0.89),
    (Document(page_content='Classes filhas herdam...', metadata={'source': 'base/FAQ Python Video YouTube.pdf'}), 0.85)
]

Resposta da ia: Herança em Python é um conceito de POO que permite...
```

## 📖 Documentação Completa

👉 **Acesse a pasta `docs/` para documentação detalhada:**

- [`docs/setup.md`](docs/setup.md) - Guia completo de instalação e configuração
- [`docs/api_reference/main_doc.md`](docs/api_reference/main_doc.md) - Documentação do `main.py`
- [`docs/api_reference/db_doc.md`](docs/api_reference/db_doc.md) - Documentação do `db.py`
- [`docs/concepts/rag_explained.md`](docs/concepts/rag_explained.md) - Conceitos RAG explicados
- [`docs/tutorials/`](docs/tutorials/) - Tutoriais passo a passo

## 🔧 Tecnologias Utilizadas

| Componente | Tecnologia | Descrição |
|-----------|------------|-----------|
| **Framework** | LangChain | Orquestração do pipeline RAG |
| **Interface Web** | Streamlit | Interface moderna e interativa |
| **Banco Vetorial** | ChromaDB | Armazenamento e busca de embeddings |
| **LLM** | Groq (Llama 3.1) | Geração de respostas gratuita e rápida |
| **Embeddings** | OpenRouter | Conversão de texto em vetores (gratuito) |
| **Processamento PDF** | PyPDF | Extração de conteúdo de PDFs |
| **Chunking** | RecursiveCharacterTextSplitter | Divisão inteligente de documentos |

## 🎓 Conceitos Aprendidos

Com este projeto você aprenderá:

- 🧠 **Arquitetura RAG** - Como combinar recuperação e geração
- 🗄️ **Bancos Vetoriais** - Armazenamento e busca semântica
- 📊 **Embeddings** - Representação numérica do texto
- 🔄 **Pipeline Completo** - Do documento à resposta
- 🤖 **Prompt Engineering** - Templates e controle de saída
- 📈 **Processamento de Lotes** - Múltiplos documentos

## 🚀 Exemplos de Uso

### Consultas Simples
```bash
python main.py
# "Como funciona lista em Python?"
# "Quais são os tipos de dados primitivos?"
# "O que é programação orientada a objetos?"
```

### Múltiplos Documentos
```bash
# Adicione vários PDFs na pasta base/
python db.py
# O sistema processará todos automaticamente
```

## 🎯 Casos de Uso

- 📚 **Assistentes de estudo** - Respostas baseadas em material didático
- 💼 **Chatbots corporativos** - Baseado em documentos internos  
- 🔬 **Pesquisa acadêmica** - Consultas em artigos científicos
- 📖 **Documentação técnica** - Ajuda baseada em manuais
- 🎓 **Tutores personalizados** - Explicações com base em apostilas

## 🔮 Próximos Passos

- [x] ✅ **Interface web com Streamlit** - Implementado!
- [x] ✅ **Histórico de consultas** - Implementado!
- [x] ✅ **Sistema de feedback** - Score de relevância implementado!
- [ ] Suporte a DOCX e TXT
- [ ] Sistema de avaliação de respostas
- [ ] Interface de upload dinâmico
- [ ] Deploy na nuvem (Streamlit Cloud/Railway)

## 🤝 Contribuição

Este é um projeto de estudos. Sinta-se à vontade para:

- 🐛 Reportar issues
- 💡 Sugerir melhorias
- 📚 Contribuir com documentação
- 🔄 Fazer fork e adaptar

## 📄 Licença

MIT License - Sinta-se livre para usar e modificar

## 🙏 Agradecimentos

- **Hashtag Programação** - Pelo excelente vídeo tutorial
- **LangChain Community** - Framework incrível
- **OpenAI** - APIs de embeddings e LLM

---

**🔗 Link do Vídeo Original:** [Agente de IA completo com Python](https://www.youtube.com/watch?v=0M8iO5ykY-E)

**🔗 Repositório:** [github.com/LucasSantos96/rag_langchain](https://github.com/LucasSantos96/rag_langchain)

---

<div align="center">
  <strong>🚀 Construa seus próprios agentes de IA com RAG!</strong>
</div>