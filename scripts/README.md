# 📜 Scripts do YouTube Playlist Manager

Esta pasta contém scripts utilitários para gerenciar playlists do YouTube.

## 🚀 Scripts Principais

### 1. `export_playlists.py`
**Função:** Exporta todas as playlists públicas de um canal para arquivos JSON.

**Como usar:**
```bash
python scripts/export_playlists.py
```

**Saída:**
- Cria arquivos JSON em `playlists/`
- Um arquivo por playlist
- Inclui todos os vídeos com metadados completos

**Dados exportados:**
- Título do vídeo
- Descrição
- URL do vídeo e thumbnail
- Data de publicação
- Duração
- Estatísticas (views, likes, etc.)

---

### 2. `search_videos_by_keywords.py`
**Função:** Busca vídeos nas playlists exportadas usando palavras-chave.

**Como usar:**
```bash
python scripts/search_videos_by_keywords.py
```

**Configuração padrão:**
- Busca por: `(RAG + text) OR (RAG + SQL)`
- Busca em: título e descrição
- Exibe resultados no terminal

**Personalização:**
Edite as variáveis no script:
```python
keywords_group1 = ['RAG', 'text']
keywords_group2 = ['RAG', 'SQL']
```

---

### 3. `export_to_markdown.py`
**Função:** Exporta resultados de busca para arquivo Markdown formatado.

**Como usar:**
```bash
python scripts/export_to_markdown.py
```

**Saída:**
- Arquivo `RAG.md` na raiz do projeto
- Formatação profissional com:
  - Cabeçalho e resumo
  - Índice navegável
  - Detalhes de cada vídeo
  - Links diretos

---

### 4. `get_playlist_info.py`
**Função:** Obtém informações detalhadas de uma playlist específica.

**Como usar:**
```bash
python scripts/get_playlist_info.py
```

**Funcionalidades:**
- Extrai Channel ID de uma playlist
- Mostra metadados da playlist
- Útil para configuração inicial

---

### 5. `list_youtube_playlists.py`
**Função:** Lista playlists públicas de um canal ou busca por termo.

**Como usar:**
```bash
python scripts/list_youtube_playlists.py
```

**Funcionalidades:**
- Lista todas as playlists de um canal
- Busca playlists por termo
- Mostra informações básicas

---

## 🧪 Pasta `testes/`

Contém scripts de teste e desenvolvimento (não versionados no Git):

- `test_transcript.py` - Testes com youtube-transcript-api
- `test_direct_transcript.py` - Testes de scraping direto
- `test_youtube_api.py` - Testes da YouTube Data API v3
- `test_ytdlp.py` - Testes com yt-dlp (solução final)

**Nota:** Estes scripts foram usados durante o desenvolvimento para testar diferentes abordagens de obtenção de transcrições.

---

## 📋 Pré-requisitos

Todos os scripts requerem:

1. **Arquivo `.env` configurado:**
```bash
YOUTUBE_API_KEY=sua_api_key_aqui
YOUTUBE_CHANNEL_ID=seu_channel_id
YOUTUBE_CHANNEL_NAME=Seu Nome
```

2. **Dependências instaladas:**
```bash
pip install -r requirements.txt
```

3. **Ambiente virtual ativado:**
```bash
source venv/bin/activate
```

---

## 🎯 Fluxo de Trabalho Recomendado

1. **Exportar playlists:**
   ```bash
   python scripts/export_playlists.py
   ```

2. **Usar a interface Streamlit** (recomendado):
   ```bash
   streamlit run app.py
   ```
   
   OU

3. **Buscar via CLI:**
   ```bash
   python scripts/search_videos_by_keywords.py
   python scripts/export_to_markdown.py
   ```

---

## 💡 Dicas

- Use a interface Streamlit para uma experiência mais rica
- Os scripts CLI são úteis para automação e batch processing
- Mantenha os arquivos JSON das playlists atualizados
- A API do YouTube tem limites de quota - use com moderação

---

## 🔧 Troubleshooting

**Erro de API Key:**
- Verifique se o arquivo `.env` existe
- Confirme que a API Key está correta
- Verifique se a YouTube Data API v3 está habilitada no Google Cloud Console

**Playlists não encontradas:**
- Confirme que o Channel ID está correto
- Verifique se as playlists são públicas
- Execute `get_playlist_info.py` para debug

**Transcrições não disponíveis:**
- Nem todos os vídeos têm transcrições
- Use a interface Streamlit que usa yt-dlp (mais robusto)
- Verifique se o vídeo tem legendas no YouTube
