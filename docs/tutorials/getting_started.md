# 🚀 Primeiros Passos - Tutorial RAG

## 🎯 Objetivo

Este tutorial vai guiá-lo através do seu primeiro sistema RAG completo, desde a instalação até a primeira consulta bem-sucedida.

---

## 📋 Pré-requisitos

Antes de começar, certifique-se de que você tem:

- ✅ Python 3.8+ instalado
- ✅ Acesso à internet (para instalar dependências)
- ✅ 15-20 minutos de tempo livre
- ✅ (Opcional) API Key da OpenAI com alguns créditos

---

## 🚀 Passo 1: Configuração do Ambiente

### 1.1 Clonar o Projeto

Abra o terminal e execute:

```bash
# Clonar o repositório
git clone https://github.com/LucasSantos96/rag_langchain.git

# Entrar no diretório
cd rag_langchain

# Verificar os arquivos
ls -la
```

**Você deverá ver:**
```
-rw-r--r--  README.md
-rw-r--r--  main.py
-rw-r--r--  db.py
-rw-r--r--  requirements.txt
drwxr-xr-x  base/
drwxr-xr-x  docs/
```

### 1.2 Ambiente Virtual

```bash
# Criar ambiente virtual
python3 -m venv venv

# Ativar ambiente
source venv/bin/activate

# Verificar (deve aparecer (venv) no início do prompt)
(venv) $ 
```

### 1.3 Instalar Dependências

```bash
# Instalar tudo de uma vez
pip install -r requirements.txt

# Verificar instalação
pip list | grep langchain
```

---

## 🔑 Passo 2: Configurar API Key

### 2.1 Obter API Key

**Opção A: OpenAI (Recomendado)**
1. Vá para [platform.openai.com](https://platform.openai.com)
2. Crie uma conta ou faça login
3. Vá em Settings → API Keys
4. Clique "Create new secret key"
5. Copie a key (começa com `sk-`)

**Opção B: OpenRouter (Alternativa Gratuita)**
1. Vá para [openrouter.ai](https://openrouter.ai)
2. Crie uma conta gratuita
3. Vá em Dashboard → API Keys
4. Copie sua key

### 2.2 Configurar Arquivo .env

```bash
# Copiar arquivo de exemplo
cp .env.example .env

# Editar com nano, vim ou VS Code
nano .env
```

**Adicione sua API key:**
```bash
# Para OpenAI
OPENAI_API_KEY=sk-sua-chave-exata-aqui
EMBEDDING_MODEL=text-embedding-3-small
LLM_MODEL=gpt-3.5-turbo

# OU para OpenRouter
# OPENAI_API_KEY=sk-or-v1-sua-chave-aqui
# EMBEDDING_MODEL=openai/text-embedding-3-small  
# LLM_MODEL=openai/gpt-3.5-turbo
```

**IMPORTANTE:** Nunca compartilhe este arquivo ou coloque no GitHub!

### 2.3 Testar Configuração

```bash
# Testar se a API key funciona
python -c "
import os
from dotenv import load_dotenv
load_dotenv()
key = os.getenv('OPENAI_API_KEY')
print(f'API Key configurada: {bool(key)}')
print(f'Primeiros 10 chars: {key[:10] if key else None}')
"
```

**Saída esperada:**
```
API Key configurada: True
Primeiros 10 chars: sk-proj-9x
```

---

## 📁 Passo 3: Preparar Documentos

### 3.1 Verificar Documento de Exemplo

```bash
# O projeto já inclui um documento
ls -la base/
```

Você deverá ver:
```
-rw-r--r--  1 user  user  347800 Jul 14  2025 FAQ Python Video YouTube.pdf
```

### 3.2 (Opcional) Adicionar Seus Próprios PDFs

```bash
# Copiar seus PDFs para a pasta base
cp /caminho/seus/pdfs/*.pdf base/

# Verificar
ls -la base/
```

**Dicas para melhores resultados:**
- ✅ PDFs com texto (não apenas imagens)
- ✅ Conteúdo educacional ou técnico
- ✅ Tamanho menor que 50MB cada
- ❌ Evite PDFs escaneados ou imagens

---

## 🏗️ Passo 4: Processar Documentos

### 4.1 Executar o Processamento

```bash
# Processar todos os PDFs
python db.py
```

**O que está acontecendo:**
1. 📄 Lendo os PDFs da pasta `base/`
2. ✂️ Dividindo em pedaços de 2000 caracteres
3. 🧠 Convertendo cada pedaço em embeddings
4. 💾 Salvando no banco vetorial ChromaDB

### 4.2 Saída Esperada

```
245
Salvando vetorização no disco...
```

**Significado:**
- `245`: Número de "chunks" (pedaços) criados
- `Salvando vetorização`: Banco vetorial sendo criado

### 4.3 Verificar Resultados

```bash
# Verificar se o banco foi criado
ls -la db/
```

Você deverá ver:
```
drwxr-xr-x  3 user  staff   96 Feb  1 17:55 .
drwxr-xr-x  5 user  staff  160 Feb  1 17:55 ..
drwxr-xr-x  2 user  staff   64 Feb  1 17:55 9f636556-54f0-410f-9e89-79defead8e44
-rw-r--r--  1 user  staff   692224 Feb  1 17:55 chroma.sqlite3
```

---

## 🔍 Passo 5: Fazer Primeira Consulta

### 5.1 Executar o Sistema de Consulta

```bash
python main.py
```

### 5.2 Fazer uma Pergunta

Quando aparecer:
```
Digite sua pergunta: 
```

Tente algumas perguntas:

**Exemplo 1:**
```
Digite sua pergunta: O que é Python?
```

**Exemplo 2:**
```
Digite sua pergunta: Como instalar bibliotecas em Python?
```

**Exemplo 3:**
```
Digite sua pergunta: O que é programação orientada a objetos?
```

### 5.3 Entendendo a Saída

A saída terá duas partes:

**Parte 1 - Resultados Brutos:**
```
[
    (Document(page_content='Python é uma linguagem de programação...', metadata={'source': 'base/FAQ Python Video YouTube.pdf'}), 0.89),
    (Document(page_content='Para instalar bibliotecas em Python...', metadata={'source': 'base/FAQ Python Video YouTube.pdf'}), 0.85)
]
2
```

**Significado:**
- `Document(...)`: Conteúdo recuperado e metadata
- `0.89`: Score de similaridade (0 a 1, mais alto = mais relevante)
- `2`: Número de documentos recuperados

**Parte 2 - Resposta da IA:**
```
Resposta da ia:
Python é uma linguagem de programação de alto nível, criada por Guido van Rossum em 1991. É conhecida por sua sintaxe clara e legível...
```

---

## 🎯 Passo 6: Experimentar Diferentes Consultas

### 6.1 Perguntas Simples

```bash
python main.py
Digite sua pergunta: Quais os tipos de dados em Python?
```

### 6.2 Perguntas Comparativas

```bash
python main.py  
Digite sua pergunta: Qual a diferença entre lista e tupla?
```

### 6.3 Perguntas Práticas

```bash
python main.py
Digite sua pergunta: Como criar uma função em Python?
```

### 6.4 Perguntas Específicas

```bash
python main.py
Digite sua pergunta: O que é o operador ** em Python?
```

---

## 🔧 Passo 7: Personalização Básica

### 7.1 Verificar o Código

Abra `main.py` para entender como funciona:

```bash
cat main.py
```

**Partes importantes:**
```python
# Template do prompt
prompt_template = """Você é um assistente inteligente...
{pergunta}
{base_conhecimento}
...
"""

# Função de busca
resultados = db.similarity_search_with_relevance_scores(pergunta)
```

### 7.2 Mudar o Número de Resultados

Edite `main.py`:
```python
# Mudar de k=4 (padrão) para k=2
resultados = db.similarity_search_with_relevance_scores(pergunta, k=2)
```

### 7.3 Adicionar Filtro de Relevância

```python
# Filtrar apenas resultados com score > 0.7
resultados_filtrados = [(doc, score) for doc, score in resultados if score > 0.7]
```

---

## 📊 Passo 8: Analisar Performance

### 8.1 Medir Tempo de Resposta

```bash
time python main.py
Digite sua pergunta: O que é Python?
```

### 8.2 Monitorar Uso da API

- **Chamadas de embedding**: 1 por consulta
- **Chamadas de LLM**: 1 por consulta  
- **Custo estimado**: $0.0005 - $0.002 por pergunta

### 8.3 Verificar Qualidade

Avalie as respostas:
- ✅ Respondem à pergunta?
- ✅ Baseadas nos documentos?
- ✅ Linguagem natural?
- ❣️ Use feedback para melhorar prompts

---

## 🛠️ Passo 9: Troubleshooting

### Problema Comum 1: "API key não encontrada"

**Sintoma:**
```
Error: OPENAI_API_KEY not found
```

**Solução:**
```bash
# Verificar se .env existe
ls -la .env

# Verificar conteúdo
cat .env

# Testar carregamento
python -c "from dotenv import load_dotenv; load_dotenv(); import os; print(os.getenv('OPENAI_API_KEY')[:10] if os.getenv('OPENAI_API_KEY') else 'Not found')"
```

### Problema Comum 2: "Nenhum PDF encontrado"

**Sintoma:**
```
0
Salvando vetorização no disco...
```

**Solução:**
```bash
# Verificar se há PDFs
ls -la base/

# Adicionar PDFs
cp seus-pdfs/*.pdf base/
python db.py
```

### Problema Comum 3: "Respostas vazias"

**Sintoma:**
```
[]
0
Resposta da ia:
```

**Solução:**
- Verifique se o banco foi criado (`ls -la db/`)
- Tente perguntas mais simples
- Verifique se os PDFs têm conteúdo textual

### Problema Comum 4: "Respostas genéricas"

**Sintoma:**
```
Resposta da ia: Desculpe, não sei a resposta para essa pergunta.
```

**Solução:**
- Verifique se o documento contém a informação
- Tente palavras-chave diferentes
- Analise os scores de similaridade

---

## 🎓 Passo 10: Próximos Aprendizados

### 10.1 Entender os Componentes

- **📖 [RAG Explicado](../concepts/rag_explained.md)** - Teoria fundamental
- **🧠 [Embeddings](../concepts/embeddings.md)** - Como funciona a busca semântica
- **🗄️ [Bancos Vetoriais](../concepts/vector_databases.md)** - Armazenamento eficiente

### 10.2 Tutoriais Avançados

- **[📄 Adicionando Documentos](adding_documents.md)** - Múltiplos formatos
- **[📝 Personalizando Prompts](customizing_prompts.md)** - Melhorar respostas
- **[⚡ Uso Avançado](advanced_usage.md)** - Otimização e deploy

### 10.3 Referência da API

- **[📖 main.py Doc](../api_reference/main_doc.md)** - Interface de consulta
- **[📊 db.py Doc](../api_reference/db_doc.md)** - Processamento de documentos

---

## ✅ Checklist de Conclusão

Você completou o tutorial se:

- [ ] ✅ Ambiente Python configurado
- [ ] ✅ Dependências instaladas sem erros
- [ ] ✅ API key configurada e funcionando
- [ ] ✅ Documentos processados com sucesso
- [ ] ✅ Primeira consulta realizada
- [ ] ✅ Entendido a saída do sistema
- [ ] ✅ Experimentado diferentes perguntas
- [ ] ✅ Resolvido pelo menos um problema

---

## 🎉 Parabéns!

🚀 **Você construiu seu primeiro sistema RAG funcional!**

O que você aprendeu:
- 🏗️ Arquitetura RAG completa
- 📄 Processamento de PDFs automáticos
- 🧠 Busca semântica com embeddings
- 🤖 Geração aumentada de respostas
- 🛠️ Configuração e troubleshooting

**Próximos passos recomendados:**
1. 📚 Leia os conceitos teóricos
2. 🔧 Experimente com seus próprios documentos
3. 🎓 Explore os tutoriais avançados
4. 💻 Considere uma interface web

**Lembre-se:** Este é apenas o começo da sua jornada com IA baseada em conhecimento! 🌟