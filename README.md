# 🤖 Projeto RAG com LangChain - Agente de IA Completo

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![LangChain](https://img.shields.io/badge/LangChain-0.1+-green)](https://python.langchain.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> 📚 **Projeto de estudos baseado no vídeo:** [Agente de IA completo com Python - Projeto RAG com Langchain](https://www.youtube.com/watch?v=0M8iO5ykY-E) por Hashtag Programação

## 🎯 Sobre o Projeto

Sistema completo de agente de IA baseado em arquitetura **RAG** (Retrieval-Augmented Generation) para responder perguntas usando documentos PDF como base de conhecimento.

### 🚀 Funcionalidades Principais

- ✅ **Processamento automático de PDFs** - Extração e chunking inteligente
- ✅ **Busca semântica avançada** - Encontra conteúdo relevante por significado
- ✅ **Interface de consulta interativa** - Perguntas em linguagem natural
- ✅ **Banco vetorial persistente** - ChromaDB para armazenamento eficiente
- ✅ **Suporte a múltiplos documentos** - Processa vários PDFs simultaneamente
- ✅ **Controle de alucinações** - Responde apenas com base nos documentos

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
├── main.py              # Interface principal de consulta RAG
├── db.py               # Processamento e vetorização de documentos
├── .env                # Configuração de API keys (OpenAI/OpenRouter)
├── requirements.txt     # Dependências do projeto
├── base/               # 📂 Diretório com documentos PDF
│   └── FAQ Python Video YouTube.pdf
├── db/                 # 🗄️ Banco vetorial ChromaDB (criado automaticamente)
└── docs/               # 📚 Documentação completa do projeto
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

```bash
# Para OpenAI
OPENAI_API_KEY=sk-sua-key-aqui
EMBEDDING_MODEL=text-embedding-3-small
LLM_MODEL=gpt-3.5-turbo

# OU para OpenRouter (alternativa gratuita)
OPENAI_API_KEY=sk-or-v1-sua-key-aqui
EMBEDDING_MODEL=openai/text-embedding-3-small
LLM_MODEL=openai/gpt-3.5-turbo
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
| **Banco Vetorial** | ChromaDB | Armazenamento e busca de embeddings |
| **Embeddings** | OpenAI | Conversão de texto em vetores |
| **LLM** | OpenAI GPT | Geração de respostas |
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

- [ ] Interface web com Streamlit
- [ ] Suporte a DOCX e TXT
- [ ] Sistema de avaliação de respostas
- [ ] Interface de upload dinâmico
- [ ] Histórico de consultas
- [ ] Sistema de feedback

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