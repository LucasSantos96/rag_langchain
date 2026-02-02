# 🚀 Guia de Instalação e Configuração

Guia completo para configurar o ambiente e colocar o projeto RAG funcionando.

## 📋 Pré-requisitos

### Sistema Operacional
- ✅ Windows 10/11
- ✅ macOS 10.14+
- ✅ Linux (Ubuntu, Debian, Fedora)

### Python
- Python 3.8 ou superior
- Recomendado: Python 3.10+ para melhor compatibilidade

### API Key
- OpenAI API Key (paga) **OU**
- OpenRouter API Key (alternativa com plano gratuito)

### Verificar Versão do Python
```bash
python --version
# ou
python3 --version
```

Se não tiver Python instalado, baixe em: [python.org](https://www.python.org/downloads/)

---

## 🔧 Passo 1: Clonar o Repositório

```bash
# Clonar do GitHub
git clone https://github.com/LucasSantos96/rag_langchain.git

# Entrar no diretório
cd rag_langchain

# Listar arquivos
ls -la
```

**Estrutura esperada:**
```
rag_langchain/
├── README.md
├── main.py
├── db.py
├── requirements.txt
├── .env.example
└── base/
```

---

## 🐍 Passo 2: Configurar Ambiente Virtual

### Linux / macOS
```bash
# Criar ambiente virtual
python3 -m venv venv

# Ativar ambiente
source venv/bin/activate

# Verificar se está ativo (prompt deve mostrar (venv))
which python
# Saída esperada: /path/to/rag_langchain/venv/bin/python
```

### Windows (CMD)
```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente
venv\Scripts\activate

# Verificar
where python
# Saída esperada: C:\path\to\rag_langchain\venv\Scripts\python.exe
```

### Windows (PowerShell)
```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente
.\venv\Scripts\Activate.ps1

# Verificar
Get-Command python
```

---

## 📦 Passo 3: Instalar Dependências

```bash
# Atualizar pip primeiro
pip install --upgrade pip

# Instalar requirements
pip install -r requirements.txt

# Verificar instalação
pip list | grep langchain
```

**Se não tiver requirements.txt:**
```bash
# Instalar manualmente
pip install langchain langchain-openai langchain-community langchain-chroma
pip install python-dotenv pypdf chromadb
pip install tiktoken openai
```

---

## 🔑 Passo 4: Configurar API Keys

### Opção A: OpenAI (Recomendado)

1. **Criar conta** em [platform.openai.com](https://platform.openai.com)
2. **Gerar API Key**: Settings → API Keys → Create new secret key
3. **Adicionar crédito** (mínimo $5 para começar)

### Opção B: OpenRouter (Alternativa Gratuita)

1. **Criar conta** em [openrouter.ai](https://openrouter.ai)
2. **Gerar API Key**: Dashboard → API Keys
3. **Plano gratuito** disponível

### Configurar Arquivo .env

```bash
# Copiar arquivo de exemplo
cp .env.example .env

# Editar o arquivo
nano .env  # Linux/macOS
# ou
notepad .env  # Windows
```

**Conteúdo do arquivo .env:**

```bash
# Para OpenAI
OPENAI_API_KEY=sk-sua-chave-aqui
EMBEDDING_MODEL=text-embedding-3-small
LLM_MODEL=gpt-3.5-turbo

# OU para OpenRouter
# OPENAI_API_KEY=sk-or-v1-sua-chave-aqui
# EMBEDDING_MODEL=openai/text-embedding-3-small
# LLM_MODEL=openai/gpt-3.5-turbo
```

**Importante:** Nunca compartilhe seu arquivo .env ou inclua no Git!

---

## 📁 Passo 5: Preparar Documentos

### Opção 1: Usar Documento de Exemplo
O projeto já inclui `base/FAQ Python Video YouTube.pdf`

### Opção 2: Adicionar Seus PDFs
```bash
# Adicionar seus documentos
cp /path/seus/pdfs/*.pdf base/

# Verificar
ls -la base/
```

**Dicas para melhores resultados:**
- PDFs textuais (não imagens)
- Conteúdo estruturado
- Tamanho razoável (< 50MB por arquivo)
- Conteúdo em português ou inglês

---

## 🧪 Passo 6: Testar Configuração

### Testar Importações
```bash
python -c "
import langchain
import chromadb
import openai
print('✅ Importações OK!')
"
```

### Testar API Key
```bash
python -c "
from dotenv import load_dotenv
import os
load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
print(f'API Key configurada: {bool(api_key)}')
"
```

---

## 🏃‍♂️ Passo 7: Executar o Projeto

### 1. Processar Documentos
```bash
python db.py
```

**Saída esperada:**
```
245
Salvando vetorização no disco...
```

### 2. Fazer Consultas
```bash
python main.py
```

**Exemplo de uso:**
```
Digite sua pergunta: O que é Python?
[Document(..., metadata={...}), 0.89]
Resposta da ia: Python é uma linguagem...
```

---

## 🐛 Solução de Problemas

### Erro: "ModuleNotFoundError"
```bash
# Garantir ambiente virtual ativo
source venv/bin/activate  # Linux/macOS
# ou
venv\Scripts\activate  # Windows

# Reinstalar dependências
pip install -r requirements.txt
```

### Erro: "API key not found"
```bash
# Verificar arquivo .env
cat .env

# Verificar se está sendo carregado
python -c "from dotenv import load_dotenv; load_dotenv(); import os; print(os.getenv('OPENAI_API_KEY')[:10])"
```

### Erro: "PDF text extraction failed"
- Verifique se o PDF não é apenas imagens
- Tente com outros arquivos PDF
- Use PDFs menores para teste

### Erro: "Embedding model not found"
- Verifique se API key tem créditos
- Confirme o nome do modelo no .env
- Teste com modelo diferente

---

## 🔧 Configurações Avançadas

### Customizar Chunk Size
Edite `db.py`:
```python
docs_separator = RecursiveCharacterTextSplitter(
    chunk_size=1000,        # Reduzir para chunks menores
    chunk_overlap=200,       # Menos sobreposição
    length_function=len,
    add_start_index=True,
)
```

### Mudar Modelo de LLM
Edite `.env`:
```bash
LLM_MODEL=gpt-4o          # Mais capaz, mas mais caro
LLM_MODEL=claude-3-haiku  # Alternativa Anthropic
```

### Configurar Proxy (se necessário)
```bash
export HTTP_PROXY=http://proxy:port
export HTTPS_PROXY=http://proxy:port
```

---

## 📊 Verificar Funcionamento

### Testes Rápidos
```bash
# 1. Verificar banco vetorial criado
ls -la db/

# 2. Verificar tamanho do banco
du -sh db/

# 3. Testar com pergunta simples
echo "O que é programação?" | python main.py
```

### Performance
- **Processamento inicial**: 1-5 minutos (depende do tamanho dos PDFs)
- **Consultas**: 2-10 segundos (depende do modelo e API)
- **Armazenamento**: ~1MB por 100 chunks

---

## 🎯 Próximos Passos

1. ✅ **Instalação completa**
2. 📖 [Entender conceitos RAG](concepts/rag_explained.md)
3. 🔍 [Explorar documentação API](api_reference/)
4. 🎓 **Fazer o tutorial prático** [Primeiros Passos](tutorials/getting_started.md)

---

## 💡 Dicas de Boas Práticas

- **Ambiente virtual**: Sempre use venv para isolar dependências
- **API Keys**: Nunca commit .env no Git, use .env.example
- **Documentos**: Comece com poucos PDFs para testar
- **Créditos**: Monitore consumo da API OpenAI
- **Backup**: Salve pasta db/ após processamento demorado

---

**🔗 Recursos adicionais:**
- [Documentação LangChain](https://python.langchain.com/)
- [ChromaDB Guide](https://docs.trychroma.com/)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)

---

**❓ Precisa de ajuda?** Verifique [Perguntas Frequentes](faq.md) ou abra uma issue no repositório.