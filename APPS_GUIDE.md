# 🎥 Guia dos Apps Streamlit

## 📱 Dois Apps Disponíveis

Este projeto possui **dois apps Streamlit** para diferentes necessidades:

---

## 1️⃣ App Original (API Key) - `app.py`

### 🎯 Características:
- ✅ Acessa **apenas playlists públicas**
- ✅ Autenticação simples (API Key)
- ✅ Não requer login Google
- ✅ Mais rápido para iniciar

### 📊 Dados:
- Carrega de: `playlists/`
- Playlists: ~8-12 (apenas públicas)
- Vídeos: ~500-1000

### 🚀 Como Usar:

#### **1. Exportar playlists públicas:**
```bash
python scripts/export_playlists.py
```

#### **2. Iniciar app:**
```bash
streamlit run app.py
```

#### **3. Acessar:**
```
http://localhost:8501
```

### 💡 Quando Usar:
- ✅ Você só precisa de playlists públicas
- ✅ Quer testar rapidamente
- ✅ Não quer configurar OAuth

---

## 2️⃣ App OAuth (Completo) - `app_oauth.py` 🆕

### 🎯 Características:
- ✅ Acessa **TODAS as playlists**
  - 🌐 Públicas
  - 🔒 Privadas
  - 🔗 Não listadas
- ✅ Autenticação OAuth 2.0
- ✅ Token salvo (não precisa reautenticar sempre)
- ✅ Acesso completo ao seu canal

### 📊 Dados:
- Carrega de: `playlists_oauth/`
- Playlists: 32 (todas)
- Vídeos: 2.777

### 🚀 Como Usar:

#### **1. Exportar todas as playlists (OAuth):**
```bash
python scripts/export_playlists_oauth.py
```

**Na primeira vez:**
- Navegador abrirá automaticamente
- Faça login na sua conta Google
- Autorize o acesso
- Token será salvo em `token.pickle`

**Próximas vezes:**
- Usa o token salvo
- Não precisa autorizar novamente

#### **2. Iniciar app OAuth:**
```bash
streamlit run app_oauth.py
```

#### **3. Acessar:**
```
http://localhost:8501
```

### 💡 Quando Usar:
- ✅ Você precisa de playlists privadas
- ✅ Quer acesso completo às suas playlists
- ✅ Está usando em produção
- ✅ Quer buscar em TODOS os vídeos

---

## 🆚 Comparação Lado a Lado

| Característica | `app.py` (API Key) | `app_oauth.py` (OAuth) |
|----------------|-------------------|------------------------|
| **Ícone** | 🎥 | 🔐 |
| **Playlists Públicas** | ✅ Sim | ✅ Sim |
| **Playlists Privadas** | ❌ Não | ✅ Sim |
| **Playlists Não Listadas** | ❌ Não | ✅ Sim |
| **Autenticação** | API Key | OAuth 2.0 |
| **Login Google** | ❌ Não | ✅ Sim (primeira vez) |
| **Total de Playlists** | ~8-12 | 32 |
| **Total de Vídeos** | ~500-1000 | 2.777 |
| **Diretório** | `playlists/` | `playlists_oauth/` |
| **Script de Export** | `export_playlists.py` | `export_playlists_oauth.py` |
| **Configuração** | Simples | Moderada |
| **Tempo de Setup** | 5 min | 25-35 min |

---

## 🎨 Diferenças Visuais

### **App Original (app.py):**
```
🎥 YouTube Playlist Manager
Busque, marque e transcreva vídeos das suas playlists
```

### **App OAuth (app_oauth.py):**
```
┌─────────────────────────────────────────────────┐
│  🔐 YouTube Playlist Manager (OAuth)            │
│  Acesso completo a TODAS as playlists           │
│  (públicas + privadas + não listadas)           │
└─────────────────────────────────────────────────┘

🔍 Busque, marque e transcreva vídeos de todas as suas playlists
```

---

## 🔄 Fluxo de Trabalho Recomendado

### **Para Uso Diário:**

```bash
# 1. Atualizar playlists OAuth (quando necessário)
python scripts/export_playlists_oauth.py

# 2. Usar app OAuth
streamlit run app_oauth.py
```

### **Para Testes Rápidos:**

```bash
# 1. Exportar playlists públicas
python scripts/export_playlists.py

# 2. Usar app original
streamlit run app.py
```

---

## 📁 Estrutura de Arquivos

```
LAB/
├── app.py                              # App original (API Key)
├── app_oauth.py                        # App OAuth (completo) 🆕
│
├── scripts/
│   ├── export_playlists.py            # Exportar públicas
│   └── export_playlists_oauth.py      # Exportar todas
│
├── playlists/                         # Playlists públicas
│   └── *.json
│
├── playlists_oauth/                   # Todas as playlists
│   └── *.json
│
├── favorites.json                     # Favoritos (compartilhado)
└── token.pickle                       # Token OAuth (auto-gerado)
```

---

## 🎯 Funcionalidades (Ambos os Apps)

### ✅ Busca de Vídeos
- Busca por palavras-chave
- Operadores AND/OR
- Busca em título e/ou descrição

### ✅ Transcrições
- Obter transcrição de vídeos
- Copiar para clipboard
- Download em .txt

### ✅ Favoritos
- Marcar vídeos como favoritos
- Gerenciar favoritos
- Favoritos compartilhados entre apps

### ✅ Estatísticas
- Total de vídeos
- Total de playlists
- Vídeos favoritos

---

## 🚀 Quick Start

### **Primeira Vez (OAuth):**

```bash
# 1. Configurar OAuth (se ainda não fez)
# Veja: autenticacao/README.md

# 2. Exportar playlists OAuth
python scripts/export_playlists_oauth.py

# 3. Iniciar app OAuth
streamlit run app_oauth.py
```

### **Uso Diário:**

```bash
# Iniciar app OAuth (recomendado)
streamlit run app_oauth.py

# OU iniciar app original
streamlit run app.py
```

---

## 🔒 Segurança

### **Arquivos Protegidos:**
```gitignore
.env                    # Credenciais
token.pickle            # Token OAuth
playlists_oauth/        # Dados privados
favorites.json          # Favoritos
```

### **Boas Práticas:**
- ✅ Nunca versionar `token.pickle`
- ✅ Nunca compartilhar `.env`
- ✅ Revogar tokens se comprometidos

---

## 🐛 Troubleshooting

### **App OAuth não carrega playlists:**

**Solução:**
```bash
# Verificar se playlists foram exportadas
ls playlists_oauth/

# Se vazio, exportar novamente
python scripts/export_playlists_oauth.py
```

### **Erro de autenticação OAuth:**

**Solução:**
```bash
# Deletar token e reautenticar
rm token.pickle
python scripts/export_playlists_oauth.py
```

### **App original não carrega playlists:**

**Solução:**
```bash
# Exportar playlists públicas
python scripts/export_playlists.py
```

---

## 📚 Documentação Adicional

- **OAuth Setup:** `autenticacao/README.md`
- **OAuth Completo:** `OAUTH_SETUP.md`
- **Quick Start OAuth:** `QUICK_START_OAUTH.md`
- **Resumo OAuth:** `OAUTH_SUMMARY.md`

---

## 🎊 Recomendação

### **Para Você (Uso Pessoal):**

**Use o App OAuth (`app_oauth.py`)** porque:
- ✅ Acesso a **TODAS** as suas playlists
- ✅ **2.777 vídeos** vs ~500-1000
- ✅ **32 playlists** vs ~8-12
- ✅ Busca em vídeos privados
- ✅ Token salvo (não precisa reautenticar)

---

## 🆘 Suporte

Se precisar de ajuda:

1. Consulte este guia
2. Veja `autenticacao/README.md` para OAuth
3. Verifique `OAUTH_SETUP.md` para detalhes

---

**Criado em:** 27 de Novembro de 2025  
**Versão:** 1.0  
**Status:** ✅ Ambos os apps funcionando

---

**Aproveite seus apps! 🚀**
