# 🚀 Passo 2: Acessar Playlists Privadas com OAuth 2.0

## 📋 Objetivo
Usar as credenciais OAuth 2.0 para autenticar e exportar todas as suas playlists do YouTube, incluindo as privadas.

---

## ✅ Pré-requisitos

- Credenciais OAuth 2.0 criadas (veja [01_CRIAR_CREDENCIAIS_OAUTH.md](01_CRIAR_CREDENCIAIS_OAUTH.md))
- Python 3.13+ instalado
- Dependências instaladas

---

## 🔧 Preparação

### **1. Configurar Credenciais no Projeto**

Edite o arquivo `.env` na raiz do projeto e adicione:

```bash
# OAuth 2.0 Credentials (para acessar playlists privadas)
OAUTH_CLIENT_ID=31459815274-xxxxxxxxxx.apps.googleusercontent.com
OAUTH_CLIENT_SECRET=GOCSPX-xxxxxxxxxxxxxxxxxxxxxxxx
```

**⚠️ Substitua pelos seus valores reais do `Oauth-client.env`**

---

### **2. Instalar Dependências OAuth**

```bash
# Ativar ambiente virtual
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

As seguintes bibliotecas serão instaladas:
- `google-auth-oauthlib==1.2.0`
- `google-auth-httplib2==0.2.0`

---

## 🚀 Executar Script OAuth

### **Comando:**

```bash
python scripts/export_playlists_oauth.py
```

---

## 🔐 Processo de Autenticação

### **Passo 1: Iniciar Script**

Ao executar o script, você verá:

```
======================================================================
🎥 YouTube Playlist Exporter - OAuth 2.0 (Playlists Privadas)
======================================================================
🔐 Iniciando autenticação OAuth 2.0...
ℹ️  Uma janela do navegador será aberta para você fazer login
Please visit this URL to authorize this application: https://accounts.google.com/o/oauth2/auth?...
```

---

### **Passo 2: Abrir Navegador**

**Opção A:** O navegador abrirá automaticamente

**Opção B:** Se não abrir, copie e cole o link mostrado no terminal

---

### **Passo 3: Selecionar Conta Google**

Na tela do navegador:
1. Selecione sua conta Google
2. Digite sua senha (se solicitado)

---

### **Passo 4: Lidar com Aviso de App Não Verificado**

Você verá uma tela:

```
⚠️ O Google não verificou este app

O app está solicitando acesso a informações confidenciais...
```

**Isso é NORMAL para apps em desenvolvimento!**

#### **Como Prosseguir:**

1. **Clique em "Avançado"** (canto inferior esquerdo)

2. Aparecerá um link:
   ```
   Ir para database-videos-estudos (não seguro)
   ```

3. **Clique nesse link**

**Por que é seguro?**
- ✅ Você é o desenvolvedor
- ✅ Você controla as credenciais
- ✅ O app só tem acesso de leitura
- ✅ Roda localmente no seu computador

---

### **Passo 5: Autorizar Permissões**

Você verá a tela de permissões:

```
O app database-videos-estudos quer acessar sua Conta do Google

Quando o acesso for permitido, o app database-videos-estudos poderá:

🎬 Visualize sua conta do YouTube

[Cancelar]  [Continuar]
```

**Clique em "Continuar"**

---

### **Passo 6: Confirmação**

Você verá a mensagem:

```
The authentication flow has completed. 
You may close this window.
```

**✅ Pode fechar a aba do navegador!**

---

## 📊 Exportação das Playlists

### **O que acontece no terminal:**

```
✅ Autenticação concluída!
💾 Credenciais salvas em token.pickle

🔍 Buscando suas playlists (públicas e privadas)...
   Encontradas 32 playlists nesta página...
✅ Total de playlists encontradas: 32
   📊 Públicas: 12 | Privadas: 18 | Não listadas: 2

📦 Exportando 32 playlists...
----------------------------------------------------------------------

1. 🌐 Playlist Pública 1
   ID: PLxxx...
   Status: PUBLIC
   Vídeos: 42
   📥 Baixando vídeos...
   ✅ Exportada: playlists_oauth/Playlist_Publica_1.json

2. 🔒 Playlist Privada 1
   ID: PLyyy...
   Status: PRIVATE
   Vídeos: 18
   📥 Baixando vídeos...
   ✅ Exportada: playlists_oauth/Playlist_Privada_1.json

...

======================================================================
📊 RESUMO DA EXPORTAÇÃO
======================================================================
✅ Playlists exportadas: 31/32
🎬 Total de vídeos: 2777
📁 Diretório: playlists_oauth/
======================================================================

✨ Exportação concluída com sucesso!
ℹ️  As playlists privadas agora estão acessíveis!
```

---

## 📁 Arquivos Gerados

### **Token OAuth:**
```
token.pickle
```
- Armazena suas credenciais de autenticação
- Válido por tempo indeterminado (renovado automaticamente)
- **Não versionar no Git!** (já está no `.gitignore`)

### **Playlists Exportadas:**
```
playlists_oauth/
├── Playlist_1.json
├── Playlist_2.json
├── Playlist_Privada_1.json  ← PRIVADA! 🔒
├── Playlist_Privada_2.json  ← PRIVADA! 🔒
└── ...
```

---

## 🔄 Próximas Execuções

### **Não Precisa Autorizar Novamente!**

Nas próximas vezes que executar o script:

```bash
python scripts/export_playlists_oauth.py
```

O script usará o `token.pickle` salvo e **não abrirá o navegador**!

```
======================================================================
🎥 YouTube Playlist Exporter - OAuth 2.0 (Playlists Privadas)
======================================================================
📂 Carregando credenciais salvas...
✅ Token válido encontrado!

🔍 Buscando suas playlists...
...
```

---

## 🐛 Troubleshooting

### **Erro: "invalid_client"**

**Causa:** Client Secret incorreto

**Solução:**
1. Verifique se o `OAUTH_CLIENT_SECRET` no `.env` está correto
2. Deve começar com `GOCSPX-`
3. Não deve ser igual ao `OAUTH_CLIENT_ID`

---

### **Erro: "redirect_uri_mismatch"**

**Causa:** URI de redirecionamento não configurado

**Solução:**
1. Acesse: https://console.cloud.google.com/apis/credentials
2. Edite sua credencial OAuth
3. Adicione em "URIs de redirecionamento autorizados":
   - `http://localhost`
   - `http://localhost:8080`

---

### **Erro: "access_denied" ou "Error 403"**

**Causa:** Seu email não está na lista de usuários de teste

**Solução:**
1. Acesse: https://console.cloud.google.com/apis/credentials/consent
2. Vá em "Público-alvo" ou "Test users"
3. Clique em "+ ADICIONAR USUÁRIOS"
4. Adicione seu email
5. Salve e tente novamente

---

### **Token Expirado**

**Causa:** Token OAuth expirou

**Solução:**
```bash
# Deletar token antigo
rm token.pickle

# Executar script novamente (vai pedir autorização)
python scripts/export_playlists_oauth.py
```

---

## 📊 Comparação: API Key vs OAuth

| Característica | API Key | OAuth 2.0 |
|----------------|---------|-----------|
| **Playlists Públicas** | ✅ Sim | ✅ Sim |
| **Playlists Privadas** | ❌ Não | ✅ Sim |
| **Playlists Não Listadas** | ❌ Não | ✅ Sim |
| **Autenticação** | Simples (key) | Login Google |
| **Renovação** | Não necessário | Automática |
| **Limite de Quota** | Compartilhado | Por usuário |

---

## 🎯 Usar Playlists no App Streamlit

### **Opção 1: Substituir Diretório**

```bash
# Backup das playlists públicas
mv playlists playlists_backup

# Usar playlists OAuth
mv playlists_oauth playlists

# Iniciar app
streamlit run app.py
```

### **Opção 2: Modificar app.py**

Edite `app.py` linha 67:

```python
# Antes
playlists = load_playlists('playlists')

# Depois
playlists = load_playlists('playlists_oauth')
```

---

## ✅ Checklist de Conclusão

- [ ] Credenciais configuradas no `.env`
- [ ] Dependências OAuth instaladas
- [ ] Script executado com sucesso
- [ ] Autenticação concluída no navegador
- [ ] Token salvo (`token.pickle`)
- [ ] Playlists exportadas em `playlists_oauth/`
- [ ] Playlists privadas acessíveis

---

## 🎊 Resultado Final

### **Conquistas:**

- ✅ **2.777 vídeos** exportados
- ✅ **31 playlists** (públicas + privadas)
- ✅ **Token salvo** para uso futuro
- ✅ **Acesso completo** às suas playlists

### **Próximos Passos:**

1. Explorar os arquivos JSON em `playlists_oauth/`
2. Usar no app Streamlit para buscar vídeos
3. Obter transcrições de vídeos privados
4. Marcar favoritos de todas as playlists

---

## 📚 Arquivos de Referência

- **Script OAuth:** `scripts/export_playlists_oauth.py`
- **Documentação Completa:** `OAUTH_SETUP.md`
- **Guia Rápido:** `QUICK_START_OAUTH.md`
- **Resumo:** `OAUTH_SUMMARY.md`

---

## 🔒 Segurança

### **Arquivos Protegidos (não versionar):**

```gitignore
# OAuth credentials
.env
Oauth-client.env
token.pickle
*.pickle

# OAuth playlists
playlists_oauth/
```

### **Boas Práticas:**

- ✅ Nunca compartilhe `token.pickle`
- ✅ Nunca versione credenciais no Git
- ✅ Use `.env` para configurações sensíveis
- ✅ Revogue tokens se comprometidos

---

## 🆘 Suporte

Se encontrar problemas:

1. Verifique o [Troubleshooting](#-troubleshooting) acima
2. Consulte `OAUTH_SETUP.md` para detalhes
3. Revise as credenciais no Google Cloud Console

---

**Criado em:** 27 de Novembro de 2025  
**Versão:** 1.0  
**Status:** ✅ Testado e Funcionando
