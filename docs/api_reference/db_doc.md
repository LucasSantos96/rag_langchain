# 📖 Documentação - db.py

## 🎯 Visão Geral

O arquivo `db.py` é responsável pelo **pipeline completo de processamento de documentos**, desde a leitura dos PDFs até a criação e persistência do banco vetorial ChromaDB.

### 🏗️ Pipeline de Processamento

```
📁 Pasta base/ (PDFs) → 📄 PyPDFLoader → 🧠 Text Splitter → 🎯 Chunks → 🔢 Embeddings → 🗄️ ChromaDB
```

Este arquivo implementa as 3 etapas fundamentais do processamento RAG:
1. **Carregamento**: Leitura dos arquivos PDF
2. **Chunking**: Divisão inteligente em pedaços
3. **Vetorização**: Criação e armazenamento dos embeddings

---

## 📝 Código Completo e Explicação

```python
# 📚 Imports Principais
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

# 🔧 Configuração Inicial
load_dotenv()

PASTA_BASE = "base"  # Diretório contendo os arquivos PDF

# 🚀 Função Principal - Orquestrador do Pipeline
def create_db():
    # 1. 📄 Carregar documentos PDF
    documents = load_documents()
    
    # 2. ✂️ Dividir documentos em chunks menores
    chunks = split_documents(documents)
    
    # 3. 🎯 Vetorizar e salvar no banco de dados
    vetorizar_chunks(chunks)

# 📁 Função 1: Carregamento de Documentos
def load_documents():
    loader = PyPDFDirectoryLoader(PASTA_BASE)
    documents = loader.load()
    return documents

# ✂️ Função 2: Divisão Inteligente de Documentos  
def split_documents(documents):
    docs_separator = RecursiveCharacterTextSplitter(
        chunk_size=2000,        # Tamanho máximo de cada chunk
        chunk_overlap=500,       # Sobreposição entre chunks
        length_function=len,     # Função para medir tamanho
        add_start_index=True,    # Adicionar índice original
    )
    chunks = docs_separator.split_documents(documents)
    print(len(chunks))  # Mostra quantidade de chunks criados
    return chunks

# 🎯 Função 3: Vetorização e Persistência
def vetorizar_chunks(chunks):
    db = Chroma.from_documents(chunks, OpenAIEmbeddings(), persist_directory="db")
    print("Salvando vetorização no disco...")

# 🚀 Ponto de Entrada do Script
if __name__ == "__main__":
    create_db()
```

---

## 🔧 Componentes Detalhados

### 1. 📚 Imports e Dependências

```python
from langchain_community.document_loaders import PyPDFDirectoryLoader  # Loader de PDFs
from langchain_text_splitters import RecursiveCharacterTextSplitter   # Splitter inteligente
from langchain_chroma.vectorstores import Chroma                       # Banco vetorial
from langchain_openai import OpenAIEmbeddings                          # Embeddings OpenAI
from dotenv import load_dotenv                                       # Variáveis de ambiente
```

**Propósito de cada import:**
- **PyPDFDirectoryLoader**: Lê automaticamente todos PDFs de uma pasta
- **RecursiveCharacterTextSplitter**: Divide documentos mantendo contexto
- **Chroma**: Banco vetorial para armazenar e buscar embeddings
- **OpenAIEmbeddings**: Gera representações numéricas do texto

### 2. 🔧 Configuração Inicial

```python
load_dotenv()          # Carrega OPENAI_API_KEY do .env
PASTA_BASE = "base"    # Diretório onde estão os PDFs
```

**Importância:**
- Segurança das credenciais API
- Flexibilidade do diretório de documentos

---

## 📁 Função 1: `load_documents()`

### Código
```python
def load_documents():
    loader = PyPDFDirectoryLoader(PASTA_BASE)
    documents = loader.load()
    return documents
```

### 🔄 O que acontece internamente:

1. **Escaneamento do Diretório**
   ```bash
   base/
   ├── FAQ Python Video YouTube.pdf
   ├── outro_documento.pdf
   └── mais_um.pdf
   ```

2. **Processamento de Cada PDF**
   ```
   PDF Página 1 → Document(page_content="texto da página 1...", metadata={...})
   PDF Página 2 → Document(page_content="texto da página 2...", metadata={...})
   ```

3. **Estrutura do Retorno**
   ```python
   [
       Document(page_content="Conteúdo extraído...", metadata={'source': 'base/arquivo1.pdf', 'page': 1}),
       Document(page_content="Mais conteúdo...", metadata={'source': 'base/arquivo1.pdf', 'page': 2}),
       Document(page_content="Outro documento...", metadata={'source': 'base/arquivo2.pdf', 'page': 1})
   ]
   ```

### 💡 Detalhes do PyPDFDirectoryLoader:
- **Automático**: Lê todos arquivos .pdf da pasta
- **Metadados**: Adiciona source e page automaticamente
- **Robusto**: Trata erros de PDF corrompidos
- **Texto puro**: Extrai apenas o conteúdo textual

---

## ✂️ Função 2: `split_documents()`

### Código
```python
def split_documents(documents):
    docs_separator = RecursiveCharacterTextSplitter(
        chunk_size=2000,        # Tamanho máximo em caracteres
        chunk_overlap=500,       # Sobreposição entre chunks
        length_function=len,     # Como medir o tamanho
        add_start_index=True,    # Guardar posição original
    )
    chunks = docs_separator.split_documents(documents)
    print(len(chunks))  # Feedback visual
    return chunks
```

### 🎯 Configurações Detalhadas

#### `chunk_size=2000`
- **Por que 2000?**: Equilíbrio entre contexto e performance
- **Muito pequeno**: Perde contexto semântico
- **Muito grande**: Ineficiente para embeddings
- **Tokens**: ~500 tokens por chunk (regra: 1 token ≈ 4 chars)

#### `chunk_overlap=500` 
- **Finalidade**: Mantém continuidade entre chunks
- **Exemplo prático**:
  ```
  Chunk 1: chars 0-2000
  Chunk 2: chars 1500-3500  ← 500 chars de overlap
  Chunk 3: chars 3000-5000  ← 500 chars de overlap
  ```

#### `add_start_index=True`
- **Utilidade**: Referência ao documento original
- **Uso**: Debugging e citações precisas

### 🧠 Como funciona o RecursiveCharacterTextSplitter:

1. **Análise Hierárquica**:
   ```
   Tenta dividir por:
   1. Parágrafos (\n\n)
   2. Linhas (\n)  
   3. Espaços ( )
   4. Caracteres (a-z)
   ```

2. **Preservação de Contexto**:
   ```python
   # Antes: Documento completo
   "Herança em POO é um conceito fundamental. Classes podem herdar..."
   
   # Depois: Chunks com contexto mantido
   Chunk 1: "Herança em POO é um conceito fundamental. Classes podem herdar..."
   Chunk 2: "...herdar características de outras classes. Isso permite..."
   ```

3. **Exemplo de Saída**:
   ```python
   [
       Document(page_content="Herança em POO é um conceito...", metadata={...}),
       Document(page_content="Classes podem herdar características...", metadata={...}),
       Document(page_content="Isso permite reutilização de código...", metadata={...})
   ]
   ```

---

## 🎯 Função 3: `vetorizar_chunks()`

### Código
```python
def vetorizar_chunks(chunks):
    db = Chroma.from_documents(chunks, OpenAIEmbeddings(), persist_directory="db")
    print("Salvando vetorização no disco...")
```

### 🔄 Processo Interno de Vetorização:

#### Etapa 1: Embeddings Generation
```python
OpenAIEmbeddings()  # Inicializa o modelo de embedding
```

**O que acontece:**
- Cada chunk de texto → Vetor numérico (ex: [0.1, -0.3, 0.8, ...])
- Dimensão típica: 1536 (text-embedding-3-small)
- API OpenAI: 1 chamada por chunk

#### Etapa 2: ChromaDB Creation
```python
Chroma.from_documents(chunks, OpenAIEmbeddings(), persist_directory="db")
```

**Componentes criados:**
- **coleção**: Armazena os vetores e metadados
- **índices**: Para busca rápida por similaridade
- **persistência**: Arquivos no disco (SQLite + dados)

#### Etapa 3: Persistência no Disco
```
db/
├── chroma.sqlite3          # Banco de dados principal  
└── 9f636556-54f0-410f-9e89-79defead8e44/  # ID da coleção
    ├── data.bin             # Dados dos embeddings
    └── index.bin            # Índices de busca
```

---

## 🚀 Função Principal: `create_db()`

### Código
```python
def create_db():
    documents = load_documents()      # 📄 PDF → Document objects
    chunks = split_documents(documents)  # ✂️ Documentos → Chunks
    vetorizar_chunks(chunks)           # 🎯 Chunks → Banco vetorial
```

### 📊 Pipeline Visual Completo:
```
📁 base/arquivo.pdf 
       ↓ (PyPDFDirectoryLoader)
📄 Document(page_content="texto completo...", metadata={source, page})
       ↓ (RecursiveCharacterTextSplitter)  
🎯 Chunk 1: "Herança é um conceito..." (2000 chars)
🎯 Chunk 2: "...permite reutilização..." (2000 chars, 500 overlap)
🎯 Chunk 3: "...código orientado objeto..." (2000 chars, 500 overlap)
       ↓ (OpenAIEmbeddings)
🔢 [0.1, -0.3, 0.8, ..., 0.2]  (vetor 1536 dimensões)
🔢 [-0.2, 0.5, -0.1, ..., 0.7]  (vetor 1536 dimensões)
🔢 [0.3, -0.4, 0.6, ..., -0.1]  (vetor 1536 dimensões)
       ↓ (ChromaDB)
🗄️ Banco vetorial persistente + índices de busca
```

---

## 📊 Métricas e Performance

### Configurações Atuais
| Parâmetro | Valor | Impacto |
|-----------|-------|---------|
| **chunk_size** | 2000 chars | Equilíbrio contexto/eficiência |
| **chunk_overlap** | 500 chars (25%) | Mantém continuidade semântica |
| **embedding model** | text-embedding-3-small | Rápido e econômico |
| **storage** | Local (ChromaDB) | Acesso rápido, sem custos de API |

### Performance Esperada
- **Documentos**: 1 PDF de 350KB → ~245 chunks
- **Tempo de processamento**: 2-5 minutos (depende do tamanho)
- **Consumo API**: ~245 chamadas de embedding  
- **Armazenamento**: ~10-50MB (depende dos documentos)
- **Consulta**: <1s (busca local)

---

## 🎓 Exemplos Práticos de Uso

### Exemplo 1: Processamento Único
```bash
python db.py
# Saída:
# 245
# Salvando vetorização no disco...
```

### Exemplo 2: Múltiplos Documentos
```bash
# Adicionar mais PDFs na pasta base/
cp novos_documentos/*.pdf base/
python db.py
# Processará todos os arquivos (novos e existentes)
```

### Exemplo 3: Monitoramento
```python
# Adicionar mais feedback
def create_db():
    print("🚀 Iniciando processamento de documentos...")
    
    documents = load_documents()
    print(f"📄 {len(documents)} páginas carregadas")
    
    chunks = split_documents(documents)
    print(f"🎯 {len(chunks)} chunks criados")
    
    vetorizar_chunks(chunks)
    print("✅ Banco vetorial criado com sucesso!")
```

---

## ⚙️ Personalização e Configuração

### Mudar Tamanho dos Chunks
```python
# Para documentos técnicos (maior contexto)
chunk_size=3000
chunk_overlap=600

# Para conversas (menor granularidade)  
chunk_size=1000
chunk_overlap=200
```

### Usar Outros Modelos de Embedding
```python
# Modelo mais potente (mais caro)
OpenAIEmbeddings(model="text-embedding-3-large")

# Modelo mais rápido (menos preciso)
OpenAIEmbeddings(model="text-embedding-ada-002")
```

### Mudar Diretório de Storage
```python
# Para múltiplos bancos
Chroma.from_documents(chunks, OpenAIEmbeddings(), persist_directory="db_python")
Chroma.from_documents(chunks, OpenAIEmbeddings(), persist_directory="db_javascript")
```

---

## 🛠️ Troubleshooting Comum

### Erro: "No PDF files found"
```bash
# Verificar se há PDFs na pasta
ls -la base/
# Adicionar .pdf se necessário
```

### Erro: "PDF text extraction failed" 
- PDF pode ser escaneado (imagens)
- Tente com PDFs diferentes
- Use OCR para converter imagens

### Erro: "Embedding quota exceeded"
- Verifique créditos OpenAI
- Use modelo menor (ada-002)
- Processe menos documentos

### Erro: "Permission denied"
```bash
# Verificar permissões do diretório
chmod 755 db/
# ou executar como administrador
```

---

## 🔮 Possíveis Melhorias Futuras

### 1. Processamento Incremental
```python
# Processar apenas novos documentos
def process_new_docs():
    existing_docs = load_existing_db()
    new_docs = find_new_pdfs()
    # Processar apenas o que é novo
```

### 2. Métricas de Qualidade
```python
# Análise dos chunks criados
def analyze_chunks(chunks):
    sizes = [len(c.page_content) for c in chunks]
    print(f"Tamanho médio: {sum(sizes)/len(sizes):.0f}")
    print(f"Chunks muito pequenos: {sum(1 for s in sizes if s < 500)}")
```

### 3. Suporte a Outros Formatos
```python
# Adicionar DOCX, TXT, HTML
from langchain_community.document_loaders import DirectoryLoader
loader = DirectoryLoader("base/", glob="**/*.txt")
```

### 4. Processamento Paralelo
```python
# Para muitos documentos
from concurrent.futures import ThreadPoolExecutor
# Processar embeddings em paralelo
```

---

## 📊 Resumo Técnico

| Componente | Função | Benefício |
|------------|--------|-----------|
| **PyPDFDirectoryLoader** | Leitura automática de PDFs | Zero configuração |
| **RecursiveCharacterTextSplitter** | Divisão inteligente | Mantém contexto |
| **OpenAIEmbeddings** | Geração de vetores | Alta qualidade semântica |
| **ChromaDB** | Banco vetorial | Busca rápida persistente |

Este arquivo representa o alicerce do sistema RAG, transformando documentos estáticos em um banco de conhecimento consultável e inteligente.