# 🧠 Memória do Projeto - YouTube Playlist Manager

## 📅 Última Atualização: 27 de Novembro de 2025

---

## 🎯 Visão Geral do Projeto


### Descrição
Aplicação Streamlit completa para gerenciar, buscar e transcrever vídeos de playlists do YouTube com interface moderna e intuitiva.

---

## ✨ Funcionalidades Implementadas

### 1. Busca Inteligente
- Operadores lógicos AND/OR
- Busca em título e/ou descrição
- Case-insensitive com destaque de keywords
- Persistência de resultados via `st.session_state`

### 2. Sistema de Favoritos
- Marcar vídeos com checkbox
- Persistência automática em `favorites.json`
- Exportação para Markdown
- Remoção fácil de favoritos

### 3. Transcrições Automáticas
- **Engine**: yt-dlp (robusto e confiável)
- Suporte multi-idioma (PT/EN)
- Timestamps formatados `[MM:SS]`
- Download em TXT
- **NOVO v1.1.0**: Botão de copiar para clipboard integrado

### 4. Exportação de Dados
- Playlists completas em JSON
- Resultados de busca em Markdown
- Favoritos em Markdown
- Metadados completos

---

## 🔧 Implementação Recente (v1.1.0)

### Funcionalidade: Copiar Transcrição para Clipboard

**Data**: 27/11/2025  
**Commit**: `b14f2b7`

#### Problema Original
- Tentativa inicial com JavaScript customizado não funcionava
- Código JavaScript aparecia na caixa de texto em vez da transcrição
- Interface confusa com múltiplos botões

#### Solução Final
Uso do componente nativo `st.code()` do Streamlit:

```python
# Exibir transcrição em bloco de código com botão de copiar nativo
st.markdown("**Transcrição:**")
st.code(formatted_transcript, language=None)
st.caption("💡 Use o ícone 📋 no canto superior direito do bloco acima para copiar a transcrição")

# Botão para download
st.download_button(
    label="💾 Baixar Transcrição",
    data=formatted_transcript,
    file_name=f"transcript_{video_id}.txt",
    mime="text/plain",
    key=f"download_{playlist_name}_{video_id}_{idx}",
    use_container_width=True
)
```

#### Vantagens da Solução
- ✅ Componente nativo do Streamlit (mais confiável)
- ✅ Sem JavaScript customizado
- ✅ Interface limpa e intuitiva
- ✅ Funciona em todos os navegadores modernos
- ✅ Botão de copiar (📋) integrado no canto superior direito

#### Localização
- **Arquivo**: `app.py`
- **Linhas**: 419-439

---

## 🏗️ Arquitetura do Sistema

### Stack Tecnológico
- **Python**: 3.13+
- **Framework UI**: Streamlit 1.40.2
- **Transcrições**: yt-dlp 2025.11.12
- **API**: YouTube Data API v3
- **Dados**: Pandas 2.2.3

### Estrutura de Arquivos
```
LAB/
├── app.py                  # Aplicação Streamlit principal
├── requirements.txt        # Dependências
├── .env                    # Configurações (API Key)
├── favorites.json          # Vídeos favoritos
├── CHANGELOG.md            # Histórico de versões
├── README.md               # Documentação
├── scripts/                # Scripts utilitários
│   ├── export_playlists.py
│   ├── search_videos_by_keywords.py
│   └── testes/            # Scripts de teste
└── playlists/             # Playlists exportadas (JSON)
```

### Fluxo de Dados
```
Frontend (Streamlit) → Backend (app.py) → APIs Externas
                              ↓
                    Camada de Dados (JSON)
```

---

## 📦 Dependências

```txt
google-api-python-client==2.149.0
python-dotenv==1.0.1
streamlit==1.40.2
youtube-transcript-api==0.6.2
pandas==2.2.3
yt-dlp==2025.11.12
pyperclip==1.9.0
```

---

## 🔑 Configuração

### Arquivo `.env`
```bash
YOUTUBE_API_KEY=sua_api_key_aqui
YOUTUBE_CHANNEL_ID=seu_channel_id
YOUTUBE_CHANNEL_NAME=Seu Nome
```

### Arquivo `.env.git` (para push automático)
```bash
GITHUB_USER=ian-iania
GITHUB_TOKEN=seu_token_aqui
```

---

## 🚀 Como Usar

### Instalação
```bash
# Criar ambiente virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

### Exportar Playlists
```bash
python scripts/export_playlists.py
```

### Iniciar Aplicação
```bash
streamlit run app.py
```

### Push para GitHub
```bash
./git-push.sh
```

---

## 🐛 Problemas Resolvidos

### 1. Transcrições Falhando
- **Problema**: `youtube-transcript-api` com erro XML parsing
- **Solução**: Migração para `yt-dlp`

### 2. Estado da Interface
- **Problema**: Página voltava em branco ao clicar em botões
- **Solução**: Implementação de `st.session_state`

### 3. Chaves Duplicadas
- **Problema**: Checkboxes com chaves duplicadas
- **Solução**: Chaves únicas incluindo playlist e índice

### 4. Copiar para Clipboard
- **Problema**: JavaScript customizado não funcionava
- **Solução**: Uso de `st.code()` nativo

---

## 📝 Lições Aprendidas

### Streamlit Best Practices
1. **Componentes Nativos**: Sempre preferir componentes nativos do Streamlit
2. **Simplicidade**: Evitar JavaScript customizado quando há alternativas nativas
3. **Estado**: Usar `st.session_state` para manter dados entre interações
4. **Chaves Únicas**: Garantir chaves únicas para widgets dinâmicos

### Transcrições
1. **yt-dlp > youtube-transcript-api**: Mais robusto e confiável
2. **Fallback**: Sempre implementar fallback entre idiomas
3. **Formato**: Timestamps melhoram legibilidade

### Git Workflow
1. **Tokens**: Usar Personal Access Tokens para HTTPS
2. **Scripts**: Automatizar push com scripts bash
3. **Segurança**: Nunca versionar tokens (.env.git no .gitignore)

---

## 🎯 Roadmap Futuro

### Versão 1.2.0 (Planejado)
- [ ] Cache de transcrições
- [ ] Busca full-text nas transcrições
- [ ] Filtros por data e duração
- [ ] Dashboard com estatísticas

### Versão 2.0.0 (Futuro)
- [ ] Suporte a múltiplos canais
- [ ] Sistema de tags customizadas
- [ ] Exportação para PDF
- [ ] GitHub Actions para CI/CD

---

## 📊 Métricas do Projeto

- **Total de Vídeos**: 2279
- **Total de Playlists**: 13
- **Linhas de Código**: ~520 (app.py)
- **Commits**: 3+
- **Versão Atual**: 1.1.0

---

## 🙏 Créditos

- **Desenvolvedor**: Persival Balleste (ian-iania)
- **Assistente IA**: Cascade/Windsurf
- **Frameworks**: Streamlit, yt-dlp
- **APIs**: YouTube Data API v3

---

## 🔐 Implementação OAuth 2.0 (NOVO - 27/11/2025)

### Visão Geral
Sistema completo de autenticação OAuth 2.0 para acessar playlists privadas do YouTube.

### Dois Apps Disponíveis

**1. app.py (Original - API Key)**
- Porta: 8501
- Playlists: ~8-12 (apenas públicas)
- Diretório: `playlists/`
- Ícone: 🎥

**2. app_oauth.py (Novo - OAuth 2.0)** 🆕
- Porta: 8503
- Playlists: 32 (públicas + privadas + não listadas)
- Vídeos: 2.777
- Diretório: `playlists_oauth/`
- Ícone: 🔐

### Melhorias Recentes (app_oauth.py)

**Ordenação por Data** (Commit: `ad0849f`)
```python
# Vídeos ordenados do mais recente para mais antigo
matching_videos.sort(key=lambda v: v.get('publishedAt', ''), reverse=True)
```

**Indicador de Privacidade** (Commit: `ad0849f`)
- 🌐 Pública
- 🔒 Privada
- 🔗 Não listada

### Estatísticas Reais
- **32 playlists** exportadas
- **2.777 vídeos** totais
- **18 playlists privadas** (56%)
- **12 playlists públicas** (38%)
- **2 playlists não listadas** (6%)

### Arquivos Criados

**Scripts:**
- `scripts/export_playlists_oauth.py` - Exportar com OAuth

**Apps:**
- `app_oauth.py` - App Streamlit OAuth

**Documentação:**
- `autenticacao/README.md` - Índice geral
- `autenticacao/01_CRIAR_CREDENCIAIS_OAUTH.md` - Como criar OAuth
- `autenticacao/02_ACESSAR_PLAYLISTS_PRIVADAS.md` - Como usar OAuth
- `OAUTH_SETUP.md` - Documentação completa
- `QUICK_START_OAUTH.md` - Guia rápido
- `OAUTH_SUMMARY.md` - Resumo executivo
- `APPS_GUIDE.md` - Comparação dos dois apps
- `WATCH_LATER_INFO.md` - Info sobre playlists especiais

### Comandos Úteis

```bash
# Exportar todas as playlists (OAuth)
python scripts/export_playlists_oauth.py

# Iniciar app OAuth
streamlit run app_oauth.py  # porta 8503

# Iniciar app original
streamlit run app.py  # porta 8501
```

### Credenciais (.env)
```bash
# API Key (públicas)
YOUTUBE_API_KEY=AIzaSyC-o9_DwuR74hBXw_og7TMANcPkFI8FY4k

# OAuth 2.0 (todas)
OAUTH_CLIENT_ID=31459815274-uh2tdjce3sg7eh8pctsev8khl25o9g3l.apps.googleusercontent.com
OAUTH_CLIENT_SECRET=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
```

### Troubleshooting OAuth

**Erro: redirect_uri_mismatch**
- Adicionar URIs no Google Cloud Console: `http://localhost`

**Erro: access_denied (403)**
- Adicionar email como usuário de teste

**Erro: invalid_client**
- Verificar OAUTH_CLIENT_SECRET (deve começar com `GOCSPX-`)

**Token expirado**
```bash
rm token.pickle
python scripts/export_playlists_oauth.py
```

### Playlists Especiais

**Watch Later** (`list=WL`)
- Não exportável pela API normal
- Solução: Criar playlist normal ou script específico

### Commits Importantes
- `27dbaef` - ✨ Adiciona suporte OAuth 2.0
- `d32cb3a` - 📝 Resumo executivo OAuth
- `93c8383` - 📚 Documentação OAuth completa
- `f8a130c` - 🚀 App OAuth criado
- `ad0849f` - ✨ Ordenação e privacidade
- `43426d4` - 📝 Doc Watch Later

---

**Última Modificação**: 27 de Novembro de 2025, 10:45 UTC-03:00
