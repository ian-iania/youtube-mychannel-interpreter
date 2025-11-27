# 🎥 YouTube Playlist Manager

Sistema completo para gerenciar, buscar e transcrever vídeos de playlists do YouTube.

## 📋 Funcionalidades

### 1. **Exportação de Playlists**
- Exporta todas as playlists públicas de um canal
- Salva informações detalhadas de cada vídeo em JSON
- Inclui: título, descrição, URL, thumbnail, data de publicação

### 2. **Busca Avançada**
- Busca por palavras-chave com operadores AND/OR
- Busca em título, descrição ou ambos
- Exportação de resultados para Markdown

### 3. **Interface Streamlit** ⭐
- Interface visual moderna e intuitiva
- Busca interativa com múltiplas opções
- Sistema de favoritos com checkboxes
- Transcrição automática de vídeos
- Exportação de favoritos para Markdown

## 🚀 Como Usar

### Instalação

```bash
# 1. Criar ambiente virtual
python3 -m venv venv
source venv/bin/activate

# 2. Instalar dependências
pip install -r requirements.txt
```

### Configuração

1. Crie um arquivo `.env` na raiz do projeto:

```bash
# YouTube API Key
YOUTUBE_API_KEY=sua_api_key_aqui

# YouTube Channel Info
YOUTUBE_CHANNEL_ID=seu_channel_id
YOUTUBE_CHANNEL_NAME=Seu Nome
```

### Exportar Playlists

```bash
# Exporta todas as playlists do canal para JSON
python scripts/export_playlists.py
```

### Buscar Vídeos (CLI)

```bash
# Busca vídeos por palavras-chave e exporta para Markdown
python scripts/search_videos_by_keywords.py
```

### Interface Streamlit 🎨

```bash
# Inicia a aplicação web
streamlit run app.py
```

A aplicação abrirá automaticamente no navegador em `http://localhost:8501`

## 📁 Estrutura do Projeto

```
LAB/
├── .env                    # Configurações (API Key, Channel ID)
├── .gitignore              # Arquivos ignorados pelo Git
├── app.py                  # Aplicação Streamlit principal
├── requirements.txt        # Dependências Python
├── README.md               # Documentação do projeto
├── favorites.json          # Vídeos favoritos (gerado automaticamente)
├── scripts/
│   ├── export_playlists.py           # Exporta playlists para JSON
│   ├── get_playlist_info.py          # Obtém info de uma playlist
│   ├── list_youtube_playlists.py     # Lista playlists públicas
│   ├── search_videos_by_keywords.py  # Busca por keywords (CLI)
│   ├── export_to_markdown.py         # Exporta resultados para MD
│   └── testes/                       # Scripts de teste (não versionados)
│       ├── test_transcript.py
│       ├── test_direct_transcript.py
│       ├── test_youtube_api.py
│       └── test_ytdlp.py
└── playlists/
    ├── playlist1.json
    ├── playlist2.json
    └── ...
```

## 🎨 Funcionalidades da Interface Streamlit

### Busca de Vídeos
1. **Configure os critérios** na barra lateral:
   - Digite palavras-chave (uma por linha)
   - Escolha operador: AND ou OR
   - Selecione onde buscar: título, descrição ou ambos

2. **Clique em "Buscar"** para ver os resultados

### Marcar Favoritos
- ✅ Marque o checkbox ao lado de cada vídeo
- Os favoritos são salvos automaticamente em `favorites.json`
- Acesse a aba "⭐ Favoritos" para ver todos os marcados

### Obter Transcrições
1. Clique no botão "📄 Obter Transcrição" em qualquer vídeo
2. A transcrição será exibida com timestamps
3. Baixe a transcrição em formato TXT

### Exportar Favoritos
- Na aba "⭐ Favoritos", clique em "📥 Exportar Favoritos para Markdown"
- Baixe um arquivo Markdown com todos os seus vídeos favoritos

## 🔧 Scripts Disponíveis

### 1. Export Playlists
```bash
python scripts/export_playlists.py
```
Exporta todas as playlists públicas do canal configurado no `.env`

### 2. Search Videos
```bash
python scripts/search_videos_by_keywords.py
```
Busca vídeos com critérios pré-definidos (RAG + text) OR (RAG + SQL)

### 3. Export to Markdown
```bash
python scripts/export_to_markdown.py
```
Exporta resultados de busca para arquivo Markdown formatado

### 4. Get Playlist Info
```bash
python scripts/get_playlist_info.py
```
Obtém informações detalhadas de uma playlist específica

## 📊 Exemplos de Uso

### Buscar vídeos sobre RAG
```python
# Na interface Streamlit:
# 1. Digite na barra lateral:
#    RAG
#    text
# 2. Operador: OR
# 3. Buscar em: Título e Descrição
# 4. Clique em "Buscar"
```

### Buscar vídeos sobre Python e AI
```python
# Na interface Streamlit:
# 1. Digite na barra lateral:
#    Python
#    AI
# 2. Operador: AND
# 3. Buscar em: Título e Descrição
# 4. Clique em "Buscar"
```

## 🎯 Recursos Avançados

### Transcrições Automáticas
- Suporta múltiplos idiomas (PT, EN)
- Fallback automático para idiomas disponíveis
- Formato com timestamps `[MM:SS] texto`
- Download em TXT

### Sistema de Favoritos
- Persistência automática
- Exportação para Markdown
- Remoção fácil de favoritos
- Histórico de quando foi adicionado

### Busca Inteligente
- Operadores lógicos (AND/OR)
- Busca case-insensitive
- Busca em título, descrição ou ambos
- Destaque de keywords encontradas

## 🛠️ Tecnologias Utilizadas

- **Python 3.13+**
- **Streamlit** - Interface web moderna e interativa
- **Google API Client** - API do YouTube Data v3
- **yt-dlp** - Download de transcrições (robusto e confiável)
- **Pandas** - Manipulação de dados
- **python-dotenv** - Gerenciamento de variáveis de ambiente

## 📝 Notas

- A API do YouTube tem limites de quota diários
- Transcrições só estão disponíveis para vídeos que as possuem
- Os favoritos são salvos localmente em `favorites.json`
- As playlists são exportadas para o diretório `playlists/`

## 🎉 Pronto para Usar!

Execute `streamlit run app.py` e comece a explorar suas playlists!
