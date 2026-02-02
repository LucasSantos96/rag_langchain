#!/usr/bin/env python3
"""
Script de teste para verificar a integração com Groq
Simula o que a aplicação Streamlit faz ao processar uma pergunta
"""

import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()


def testar_groq():
    """Testa a API do Groq com uma pergunta simples"""

    print("🧪 Testando integração com Groq...")
    print("=" * 60)

    # Verificar configurações
    groq_api_key = os.getenv("GROQ_API_KEY")
    groq_model = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

    if not groq_api_key:
        print("❌ Erro: GROQ_API_KEY não configurada no .env")
        return False

    print(f"✅ API Key configurada: {groq_api_key[:15]}...")
    print(f"✅ Modelo: {groq_model}")
    print()

    # Testar importação
    try:
        from langchain_groq import ChatGroq
        from langchain_core.prompts import ChatPromptTemplate

        print("✅ Imports realizados com sucesso")
    except ImportError as e:
        print(f"❌ Erro ao importar: {e}")
        print("💡 Execute: source venv/bin/activate")
        return False

    # Criar prompt simples
    prompt_template = """Você é um assistente útil. Responda de forma clara e objetiva.

Pergunta: {pergunta}

Resposta:"""

    try:
        prompt = ChatPromptTemplate.from_template(prompt_template)

        # Configurar modelo Groq
        print("🔄 Configurando modelo Groq...")
        chat = ChatGroq(
            temperature=0.1,
            model=groq_model,
            api_key=groq_api_key,
        )

        # Criar chain
        chain = prompt | chat

        # Fazer pergunta de teste
        pergunta_teste = "O que é Python em 2 frases?"
        print(f"❓ Pergunta de teste: '{pergunta_teste}'")
        print("⏳ Processando... (isso pode levar alguns segundos)")
        print()

        # Invocar
        response = chain.invoke({"pergunta": pergunta_teste})

        # Mostrar resultado
        print("=" * 60)
        print("✅ RESPOSTA DO MODELO:")
        print("=" * 60)
        print(response.content)
        print("=" * 60)
        print()
        print("🎉 Teste concluído com SUCESSO!")
        print("🚀 A API do Groq está funcionando perfeitamente!")
        print()
        print("💡 Agora você pode usar a aplicação Streamlit em:")
        print("   http://localhost:8501")
        print()
        print("📝 Faça uma pergunta como:")
        print('   "O que é Python?"')
        print('   "Como criar uma função em Python?"')
        print('   "O que são listas em Python?"')

        return True

    except Exception as e:
        print(f"❌ Erro ao processar: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    sucesso = testar_groq()
    exit(0 if sucesso else 1)
