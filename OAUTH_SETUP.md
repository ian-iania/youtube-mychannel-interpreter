# 🔐 Configuração OAuth 2.0 - Acesso a Playlists Privadas

## 📋 Visão Geral

Este guia explica como configurar e usar OAuth 2.0 para acessar **playlists privadas** do YouTube. A versão padrão do projeto usa API Key e só acessa playlists públicas. Com OAuth, você pode acessar todas as suas playlists, incluindo as privadas.

---

## 🆚 Diferença entre API Key e OAuth

| Característica | API Key (Atual) | OAuth 2.0 (Novo) |
|----------------|-----------------|------------------|
| **Acesso** | Apenas playlists públicas | Todas as playlists (públicas + privadas) |
| **Autenticação** | Simples (apenas key) | Requer login do usuário |
| **Permissões** | Somente leitura pública | Acesso autorizado pelo usuário |
| **Token** | Permanente | Renovável automaticamente |
| **Uso** | `export_playlists.py` | `export_playlists_oauth.py` |

---

## ✅ Pré-requisitos

1. ✅ Credenciais OAuth já criadas (você já tem!)
2. ✅ Python 3.13+ instalado
3. ✅ Dependências instaladas

---

## 🚀 Instalação

### 1. Instalar Dependências OAuth

```bash
# Ativar ambiente virtual
source venv/bin/activate

# Instalar novas dependências
pip install google-auth-oauthlib==1.2.0 google-auth-httplib2==0.2.0
```

Ou simplesmente:

```bash
pip install -r requirements.txt
```

### 2. Verificar Credenciais no `.env`

O arquivo `.env` já deve conter:

```bash
# OAuth 2.0 Credentials (para acessar playlists privadas)
OAUTH_CLIENT_ID=31459815274-gf0tlgpi57usl9b74p6sj8p9dsg5dvml.apps.googleusercontent.com
OAUTH_CLIENT_SECRET=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
```

✅ **Já configurado!**

---

## 🎯 Como Usar

### Exportar Playlists Privadas

```bash
# Executar script OAuth
python scripts/export_playlists_oauth.py
```

### O que acontece:

1. **Primeira execução**:
   - 🌐 Uma janela do navegador será aberta
   - 🔐 Você fará login na sua conta Google
   - ✅ Autorizar o acesso às suas playlists
   - 💾 Token será salvo em `token.pickle`

2. **Execuções seguintes**:
   - 📂 Token salvo será reutilizado
   - 🚀 Não precisa fazer login novamente
   - 🔄 Token é renovado automaticamente se expirar

### Saída Esperada

```
======================================================================
🎥 YouTube Playlist Exporter - OAuth 2.0 (Playlists Privadas)
======================================================================
🔐 Iniciando autenticação OAuth 2.0...
ℹ️  Uma janela do navegador será aberta para você fazer login
✅ Autenticação concluída!
💾 Credenciais salvas em token.pickle

🔍 Buscando suas playlists (públicas e privadas)...
   Encontradas 15 playlists nesta página...
✅ Total de playlists encontradas: 15
   📊 Públicas: 8 | Privadas: 5 | Não listadas: 2

📦 Exportando 15 playlists...
----------------------------------------------------------------------

1. 🌐 Minha Playlist Pública
   ID: PLxxx...
   Status: PUBLIC
   Vídeos: 42
   📥 Baixando vídeos...
   ✅ Exportada: playlists_oauth/Minha_Playlist_Publica.json

2. 🔒 Minha Playlist Privada
   ID: PLyyy...
   Status: PRIVATE
   Vídeos: 18
   📥 Baixando vídeos...
   ✅ Exportada: playlists_oauth/Minha_Playlist_Privada.json

...

======================================================================
📊 RESUMO DA EXPORTAÇÃO
======================================================================
✅ Playlists exportadas: 15/15
🎬 Total de vídeos: 347
📁 Diretório: playlists_oauth/
======================================================================

✨ Exportação concluída com sucesso!
ℹ️  As playlists privadas agora estão acessíveis!
```

---

## 📁 Estrutura de Arquivos

```
LAB/
├── .env                           # Credenciais (API Key + OAuth)
├── token.pickle                   # Token OAuth (gerado automaticamente)
├── playlists/                     # Playlists públicas (API Key)
│   └── *.json
├── playlists_oauth/               # TODAS as playlists (OAuth)
│   └── *.json                     # Inclui privadas!
└── scripts/
    ├── export_playlists.py        # Script original (só públicas)
    └── export_playlists_oauth.py  # Novo script (públicas + privadas)
```

---

## 🔄 Usando Playlists Privadas no App

### Opção 1: Substituir Diretório (Simples)

```bash
# Backup das playlists públicas
mv playlists playlists_backup

# Usar playlists OAuth (com privadas)
mv playlists_oauth playlists

# Iniciar app
streamlit run app.py
```

### Opção 2: Configurar no App (Avançado)

Modificar `app.py` para aceitar parâmetro de diretório:

```python
# No app.py, linha 67
playlists_dir = st.sidebar.selectbox(
    "Diretório de Playlists",
    options=['playlists', 'playlists_oauth'],
    help="Escolha 'playlists_oauth' para incluir playlists privadas"
)

playlists = load_playlists(playlists_dir)
```

---

## 🔒 Segurança

### Arquivos Sensíveis (NÃO versionar)

✅ Já configurado no `.gitignore`:

```gitignore
# OAuth credentials
Oauth-client.env
token.pickle
*.pickle

# OAuth playlists
playlists_oauth/
```

### Boas Práticas

1. ✅ **Nunca compartilhe** `token.pickle`
2. ✅ **Nunca versione** credenciais OAuth
3. ✅ **Revogue tokens** se comprometidos
4. ✅ **Use .env** para credenciais

### Revogar Acesso

Se precisar revogar o acesso:

1. Acesse: https://myaccount.google.com/permissions
2. Encontre "YouTube Playlist Manager"
3. Clique em "Remover acesso"
4. Delete `token.pickle`

---

## 🐛 Troubleshooting

### Erro: "Credenciais não encontradas"

```bash
❌ Erro: OAUTH_CLIENT_ID e OAUTH_CLIENT_SECRET não encontrados no .env
```

**Solução**: Verificar se `.env` contém as credenciais OAuth.

### Erro: "Token expirado"

```bash
🔄 Renovando token expirado...
```

**Solução**: O script renova automaticamente. Se falhar, delete `token.pickle` e execute novamente.

### Erro: "Acesso negado"

```bash
❌ Erro: Access denied
```

**Solução**: 
1. Verificar se você autorizou o acesso
2. Verificar se as credenciais OAuth estão corretas
3. Tentar revogar e autorizar novamente

### Navegador não abre

**Solução**: O script mostrará uma URL. Copie e cole no navegador manualmente.

---

## 📊 Comparação de Resultados

### Antes (API Key - Só Públicas)

```bash
python scripts/export_playlists.py
# Resultado: 8 playlists públicas
```

### Depois (OAuth - Todas)

```bash
python scripts/export_playlists_oauth.py
# Resultado: 15 playlists (8 públicas + 5 privadas + 2 não listadas)
```

---

## 🎯 Próximos Passos

Após exportar com OAuth:

1. ✅ Verificar `playlists_oauth/` para confirmar playlists privadas
2. ✅ Comparar com `playlists/` para ver a diferença
3. ✅ Decidir qual diretório usar no app
4. ✅ Testar busca e transcrição de vídeos privados

---

## 📚 Referências

- [YouTube Data API - OAuth 2.0](https://developers.google.com/youtube/v3/guides/authentication)
- [Google OAuth 2.0](https://developers.google.com/identity/protocols/oauth2)
- [Python Google Auth](https://google-auth.readthedocs.io/)

---

## ✨ Benefícios do OAuth

- 🔒 **Acesso completo** às suas playlists privadas
- 🔄 **Token renovável** automaticamente
- 🛡️ **Seguro** - você controla as permissões
- 📊 **Estatísticas completas** - inclui todas as playlists
- 🎯 **Busca ampliada** - encontre vídeos em playlists privadas

---

**Pronto para usar! Execute o script e aproveite o acesso completo às suas playlists! 🚀**
