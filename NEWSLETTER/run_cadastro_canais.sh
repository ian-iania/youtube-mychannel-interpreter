#!/bin/bash

# Script para executar a UI de Cadastro de Canais

echo "🚀 Iniciando UI de Cadastro de Canais..."
echo ""

cd "$(dirname "$0")"

# Verificar se streamlit está instalado
if ! command -v streamlit &> /dev/null; then
    echo "❌ Streamlit não encontrado!"
    echo "📦 Instalando streamlit..."
    pip3 install streamlit
fi

# Executar aplicação
echo "✅ Abrindo aplicação no navegador..."
echo "🌐 URL: http://localhost:8501"
echo ""
echo "💡 Para parar: Ctrl+C"
echo ""

streamlit run ui_streamlit/cadastro_de_canais.py --server.port 8501
