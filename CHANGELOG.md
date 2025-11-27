# 📝 Changelog - YouTube Playlist Manager

## [1.1.0] - 2025-11-27

### ✨ Novas Funcionalidades

#### Copiar Transcrição para Clipboard
- ✅ Botão de copiar integrado no bloco de transcrição
- ✅ Uso do componente nativo `st.code()` do Streamlit
- ✅ Ícone de copiar (📋) no canto superior direito do bloco
- ✅ Interface simplificada e mais intuitiva
- ✅ Remoção de JavaScript customizado complexo

### 🔧 Melhorias Técnicas

#### Interface de Transcrição
- ✅ Simplificação da exibição de transcrições
- ✅ Remoção de componentes redundantes
- ✅ Melhor feedback visual para o usuário
- ✅ Uso de componentes nativos do Streamlit

### 📦 Dependências Atualizadas

```
pyperclip==1.9.0  # Adicionado (preparação para futuras features)
```

### 🐛 Correções

#### Funcionalidade de Cópia
- ❌ **Problema:** Botão customizado não copiava corretamente
- ✅ **Solução:** Uso do `st.code()` com botão de copiar nativo

### 📝 Commits

- `b14f2b7` - ✨ Adiciona funcionalidade de copiar transcrição para clipboard

---

## [1.0.0] - 2025-11-27

### ✨ Funcionalidades Principais

#### Interface Streamlit
- ✅ Busca avançada de vídeos com operadores AND/OR
- ✅ Sistema de favoritos com persistência
- ✅ Transcrição automática de vídeos usando yt-dlp
- ✅ Exportação de favoritos para Markdown
- ✅ Interface moderna e responsiva
- ✅ Manutenção de estado entre interações

#### Scripts CLI
- ✅ Exportação de playlists para JSON
- ✅ Busca por palavras-chave
- ✅ Exportação de resultados para Markdown
- ✅ Utilitários de gerenciamento de playlists

### 🔧 Melhorias Técnicas

#### Transcrições
- ✅ Migração de `youtube-transcript-api` para `yt-dlp`
- ✅ Suporte robusto a legendas automáticas e manuais
- ✅ Fallback inteligente entre idiomas
- ✅ Formato com timestamps `[MM:SS]`
- ✅ Download de transcrições em TXT

#### Organização do Projeto
- ✅ Scripts organizados em `scripts/`
- ✅ Scripts de teste movidos para `scripts/testes/`
- ✅ `.gitignore` atualizado com padrões Python
- ✅ Documentação completa (README.md)
- ✅ Documentação de scripts (scripts/README.md)

### 📦 Dependências

```
google-api-python-client==2.149.0
python-dotenv==1.0.1
streamlit==1.40.2
youtube-transcript-api==0.6.2
pandas==2.2.3
yt-dlp==2025.11.12
```

### 🗂️ Estrutura Final

```
LAB/
├── .env                    # Configurações (não versionado)
├── .gitignore              # Arquivos ignorados
├── app.py                  # Aplicação Streamlit
├── requirements.txt        # Dependências
├── README.md               # Documentação principal
├── CHANGELOG.md            # Este arquivo
├── AGENTS.md               # Regras de agentes (não versionado)
├── CLAUDE.md               # Regras Claude (não versionado)
├── favorites.json          # Favoritos (não versionado)
├── scripts/
│   ├── README.md                     # Documentação dos scripts
│   ├── export_playlists.py           # Exporta playlists
│   ├── get_playlist_info.py          # Info de playlist
│   ├── list_youtube_playlists.py     # Lista playlists
│   ├── search_videos_by_keywords.py  # Busca CLI
│   ├── export_to_markdown.py         # Exporta MD
│   └── testes/                       # Scripts de teste (não versionados)
│       ├── test_transcript.py
│       ├── test_direct_transcript.py
│       ├── test_youtube_api.py
│       └── test_ytdlp.py
└── playlists/
    └── *.json              # Playlists exportadas
```

### 🐛 Correções

#### Transcrições
- ❌ **Problema:** `youtube-transcript-api` falhava com erro XML parsing
- ✅ **Solução:** Migração para `yt-dlp` que é mais robusto

#### Estado da Interface
- ❌ **Problema:** Página voltava em branco ao clicar em botões
- ✅ **Solução:** Implementação de `st.session_state`

#### Chaves Duplicadas
- ❌ **Problema:** Checkboxes com chaves duplicadas
- ✅ **Solução:** Chaves únicas incluindo playlist e índice

### 📚 Documentação

- ✅ README.md principal atualizado
- ✅ README.md dos scripts criado
- ✅ CHANGELOG.md criado
- ✅ Comentários inline no código
- ✅ Docstrings em todas as funções

### 🎯 Próximos Passos (Sugestões)

- [ ] Adicionar cache de transcrições
- [ ] Implementar busca por data
- [ ] Adicionar filtros por duração de vídeo
- [ ] Exportar transcrições para PDF
- [ ] Adicionar suporte a múltiplos canais
- [ ] Implementar busca full-text nas transcrições
- [ ] Adicionar gráficos de estatísticas
- [ ] Implementar sistema de tags customizadas

### 🙏 Agradecimentos

Projeto desenvolvido com assistência de IA (Cascade/Windsurf) para gerenciamento eficiente de playlists do YouTube.

---

**Versão:** 1.0.0  
**Data:** 27 de Novembro de 2025  
**Status:** ✅ Produção
