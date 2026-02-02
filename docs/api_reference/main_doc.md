# 📖 Documentação - main.py

## 🎯 Visão Geral

O arquivo `main.py` implementa a **interface principal de consulta** do sistema RAG, permitindo que usuários façam perguntas em linguagem natural e recebam respostas baseadas nos documentos processados.

### 🏗️ Arquitetura da Função Principal

O sistema implementa o fluxo completo de RAG (Retrieval-Augmented Generation):

```
📝 Pergunta do Usuário → 🧠 Embedding → 🔍 Busca no ChromaDB → 📄 Contexto Recuperado → 🤖 LLM → 💬 Resposta Final
```

---

## 📝 Código Completo e Explicação

```python
# 📚 Imports Necessários
from langchain_chroma.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# 🔧 Configuração Inicial
load_dotenv()  # Carrega variáveis de ambiente do .env

CAMINHO_DB = "db"  # Diretório do banco vetorial ChromaDB

# 🤖 Template de Prompt Estruturado
prompt_template = """Você é um assistente inteligente que ajuda os usuários com suas perguntas com base em documentos fornecidos:
{pergunta}

Utilize as informações do documentos para responder à pergunta acima. Forneça respostas detalhadas e precisas:

{base_conhecimento}

Se a informação não estiver disponível nos documentos, responda com "Desculpe, não sei a resposta para essa pergunta."
"""

# 🎯 Função Principal de Consulta RAG
def perguntar():
    pergunta = input("Digite sua pergunta: ")
    
    # 🧠 Carregar o banco de dados vetorizado
    func_embedding = OpenAIEmbeddings()
    db = Chroma(persist_directory=CAMINHO_DB, embedding_function=func_embedding)
    
    # 🔍 Comparar a pergunta com os documentos (similaridade semântica)
    resultados = db.similarity_search_with_relevance_scores(pergunta)
    print(resultados)
    print(len(resultados))
    
    # 📄 Construir o contexto para o LLM
    contexto = ""
    for doc, score in resultados:
        contexto += f"\n{doc.page_content}"
    
    # 🤖 Formatar o prompt completo
    prompt = ChatPromptTemplate.from_template(prompt_template)
    chain = prompt | ChatOpenAI()
    response = chain.invoke({
        "pergunta": pergunta,
        "base_conhecimento": contexto
    })
    
    print("Resposta da ia:")
    print(response.content)

# 🚀 Ponto de Entrada
if __name__ == "__main__":
    perguntar()
```

---

## 🔧 Componentes Detalhados

### 1. 📚 Imports e Dependências

```python
from langchain_chroma.vectorstores import Chroma          # Banco vetorial
from langchain_openai import OpenAIEmbeddings             # Geração de embeddings
from dotenv import load_dotenv                           # Carregar .env
from langchain_core.prompts import ChatPromptTemplate     # Templates de prompt
from langchain_openai import ChatOpenAI                  # Modelo LLM
```

**Propósito:** Importa todas as bibliotecas necessárias para o pipeline RAG.

### 2. 🔧 Configuração Inicial

```python
load_dotenv()          # Carrega OPENAI_API_KEY do arquivo .env
CAMINHO_DB = "db"      # Define onde está o banco vetorial
```

**Por que importante:**
- `load_dotenv()` garante segurança das API keys
- `CAMINHO_DB` permite flexibilidade de storage

### 3. 🤖 Template de Prompt

```python
prompt_template = """Você é um assistente inteligente...
{pergunta}             # ← Placeholder para pergunta do usuário
{base_conhecimento}     # ← Placeholder para contexto recuperado
...
"""
```

**Elementos-chave:**
- **Persona**: "assistente inteligente" - Define comportamento
- **Contexto**: `{base_conhecimento}` - Onde o RAG insere documentos
- **Fallback**: "não sei a resposta" - Controle de alucinações
- **Linguagem**: Português - Alinhado com os documentos

### 4. 🧠 Banco Vetorial e Embeddings

```python
func_embedding = OpenAIEmbeddings()                              # Cria função de embedding
db = Chroma(persist_directory=CAMINHO_DB, embedding_function=func_embedding)  # Carrega BD
```

**Como funciona:**
1. `OpenAIEmbeddings()` converte texto em vetores numéricos
2. `Chroma()` carrega o banco vetorial persistente do disco
3. O embedding function permite buscas semânticas

---

## 🔍 Fluxo de Execução Detalhado

### Etapa 1: 📝 Entrada do Usuário
```python
pergunta = input("Digite sua pergunta: ")
```
- Captura pergunta em linguagem natural
- Exemplo: "O que é herança em Python?"

### Etapa 2: 🧠 Carregamento do Banco Vetorial
```python
func_embedding = OpenAIEmbeddings()
db = Chroma(persist_directory=CAMINHO_DB, embedding_function=func_embedding)
```
- Inicializa a função de embedding (OpenAI)
- Carrega o ChromaDB do diretório "db/"
- Verifica integridade do banco vetorial

### Etapa 3: 🔍 Busca Semântica
```python
resultados = db.similarity_search_with_relevance_scores(pergunta)
```

**O que acontece internamente:**
1. **Embedding da Pergunta**: Pergunta → Vetor numérico
2. **Comparação Vetorial**: Vetor da pergunta vs todos os vetores do BD
3. **Ranking**: Ordenação por similaridade (cosseno)
4. **Seleção**: Retorna os k mais similares (padrão: k=4)

**Saída esperada:**
```python
[
    (Document(page_content="Herança é um conceito...", metadata={'source': 'base/FAQ...pdf'}), 0.89),
    (Document(page_content="Classes filhas herdam...", metadata={'source': 'base/FAQ...pdf'}), 0.85),
    (Document(page_content="Em POO, herança permite...", metadata={'source': 'base/FAQ...pdf'}), 0.78)
]
```

### Etapa 4: 📄 Construção do Contexto
```python
contexto = ""
for doc, score in resultados:
    contexto += f"\n{doc.page_content}"
```

**Processo:**
1. Extrai apenas o conteúdo textual dos documentos
2. Concatena todos os chunks recuperados
3. Cria uma base de conhecimento unificada

**Resultado final:**
```python
contexto = """
Herança é um dos pilares da programação orientada a objetos...
Classes filhas herdam atributos e métodos das classes mães...
Em POO, herança permite reutilização de código...
"""
```

### Etapa 5: 🤖 Formatação e Invocação do LLM
```python
prompt = ChatPromptTemplate.from_template(prompt_template)
chain = prompt | ChatOpenAI()
response = chain.invoke({
    "pergunta": pergunta,
    "base_conhecimento": contexto
})
```

**Pipeline LangChain:**
1. `ChatPromptTemplate.from_template()` → Formata o prompt
2. `| ChatOpenAI()` → Cria a chain do modelo
3. `.invoke()` → Executa com os parâmetros

**Prompt final enviado ao LLM:**
```python
"""Você é um assistente inteligente que ajuda os usuários com suas perguntas com base em documentos fornecidos:
O que é herança em Python?

Utilize as informações do documentos para responder à pergunta acima. Forneça respostas detalhadas e precisas:

Herança é um dos pilares da programação orientada a objetos...
Classes filhas herdam atributos e métodos das classes mães...
Em POO, herança permite reutilização de código...

Se a informação não estiver disponível nos documentos, responda com "Desculpe, não sei a resposta para essa pergunta."
"""
```

---

## ⚙️ Parâmetros e Configurações

### Constantes Globais
```python
CAMINHO_DB = "db"                    # Diretório do ChromaDB
prompt_template = "..."              # Template do prompt
```

### Variáveis de Ambiente (.env)
```bash
OPENAI_API_KEY=sk-xxx               # Chave da API OpenAI
LLM_MODEL=gpt-3.5-turbo             # Modelo do LLM
EMBEDDING_MODEL=text-embedding-3-small  # Modelo de embedding
```

### Configurações Implícitas
- **k=4**: Número padrão de documentos recuperados
- **score_threshold**: Sempre retorna os k mais similares
- **temperature**: Default do modelo (criatividade)

---

## 🎓 Exemplos de Uso

### Exemplo 1: Pergunta Direta
```bash
python main.py
Digite sua pergunta: O que é Python?

# Sistema busca documentos sobre definição de Python
# Retorna resposta baseada nos PDFs processados
```

### Exemplo 2: Pergunta Comparativa
```bash
Digite sua pergunta: Qual a diferença entre lista e tupla?

# Busca por menções de ambos os termos
# Compara informações dos documentos
```

### Exemplo 3: Pergunta Prática
```bash
Digite sua pergunta: Como instalar uma biblioteca?

# Procura por tutorias ou instruções nos documentos
# Responde com base no conteúdo encontrado
```

---

## 🚀 Melhorias e Extensões

### 1. Adicionar Filtros de Relevância
```python
# Filtrar por score mínimo
resultados_filtrados = [(doc, score) for doc, score in resultados if score > 0.7]
```

### 2. Personalizar Número de Resultados
```python
# Buscar mais documentos para perguntas complexas
k = 6 if len(pergunta.split()) > 10 else 4
resultados = db.similarity_search_with_relevance_scores(pergunta, k=k)
```

### 3. Adicionar Metadata nos Resultados
```python
print(f"Fonte: {doc.metadata.get('source', 'Desconhecido')}")
print(f"Score: {score:.2f}")
```

---

## ⚠️ Pontos de Atenção

### Requisitos Obrigatórios
- ✅ Arquivo `.env` configurado com `OPENAI_API_KEY`
- ✅ Banco vetorial criado em `db/` (executar `python db.py` primeiro)
- ✅ Dependências instaladas (`pip install -r requirements.txt`)

### Limitações Conhecidas
- **Créditos API**: Cada consulta consome tokens da OpenAI
- **Tamanho do Contexto**: Muitos documentos podem exceder o limite
- **Performance**: Latência depende da API OpenAI

### Boas Práticas
- 💰 Monitore consumo da API OpenAI
- 📊 Use scores de relevância para filtrar resultados
- 🎯 Faça perguntas específicas para melhores respostas
- 🔄 Limpe o cache do ChromaDB se atualizar documentos

---

## 🔮 Possíveis Melhorias Futuras

1. **Interface Web**: Adicionar Streamlit ou Flask
2. **Histórico**: Salvar conversas anteriores
3. **Feedback**: Sistema de avaliação de respostas
4. **Batch**: Processar múltiplas perguntas
5. **Cache**: Respostas em cache para perguntas repetidas
6. **Métricas**: Análise de qualidade das respostas

---

## 📊 Resumo Técnico

| Componente | Tecnologia | Função |
|------------|------------|--------|
| **Banco Vetorial** | ChromaDB | Armazenamento e busca de embeddings |
| **Embeddings** | OpenAI | Conversão texto → vetor |
| **LLM** | GPT-3.5/4 | Geração de respostas |
| **Template** | LangChain | Formatação de prompts |
| **Interface** | Terminal CLI | Interação com usuário |

Este arquivo representa o coração da interface RAG, conectando usuários a conhecimento especializado através de busca semântica e geração aumentada.