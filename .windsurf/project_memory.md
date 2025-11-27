# 🧠 Memória do Projeto - YouTube Playlist Manager

## 📅 Última Atualização: 27 de Novembro de 2025

---

## 🎯 Visão Geral do Projeto

**Nome**: YouTube Playlist Manager  
**Versão**: 1.1.0  
**Status**: ✅ Produção  
**Repositório**: https://github.com/ian-iania/youtube-mychannel-interpreter

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

**Última Modificação**: 27 de Novembro de 2025, 08:30 UTC-03:00
