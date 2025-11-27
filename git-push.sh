#!/bin/bash
# Script helper para fazer push no GitHub
# Usa as credenciais do arquivo .env.git

# Cores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 GitHub Push Helper${NC}"
echo "================================"

# Verificar se .env.git existe
if [ ! -f .env.git ]; then
    echo -e "${RED}❌ Arquivo .env.git não encontrado!${NC}"
    exit 1
fi

# Carregar credenciais
source .env.git

# Verificar se as variáveis foram carregadas
if [ -z "$GITHUB_USER" ] || [ -z "$GITHUB_TOKEN" ]; then
    echo -e "${RED}❌ Credenciais não encontradas no .env.git${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Credenciais carregadas${NC}"
echo "   Usuário: $GITHUB_USER"
echo ""

# Configurar remote com token
echo -e "${BLUE}📡 Configurando remote...${NC}"
git remote set-url origin "https://${GITHUB_USER}:${GITHUB_TOKEN}@github.com/ian-iania/youtube-mychannel-interpreter.git"

# Fazer push
echo -e "${BLUE}📤 Fazendo push...${NC}"
git push origin main

# Limpar token da URL por segurança
echo -e "${BLUE}🔒 Removendo token da URL...${NC}"
git remote set-url origin "https://github.com/ian-iania/youtube-mychannel-interpreter.git"

echo ""
echo -e "${GREEN}✅ Push concluído com sucesso!${NC}"
echo -e "${BLUE}🌐 Acesse: https://github.com/ian-iania/youtube-mychannel-interpreter${NC}"
