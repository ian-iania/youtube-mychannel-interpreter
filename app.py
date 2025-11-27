#!/usr/bin/env python3
"""
Streamlit App - YouTube Playlist Video Search & Transcript
Interface para buscar vídeos em playlists, marcar favoritos e obter transcrições
"""

import streamlit as st
import json
import os
from pathlib import Path
from datetime import datetime
import yt_dlp
import requests
import pandas as pd

# Configuração da página
st.set_page_config(
    page_title="YouTube Playlist Manager",
    page_icon="🎥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado para deixar bonito como o markdown
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
    }
    .video-card {
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        background-color: #f9f9f9;
    }
    .video-title {
        font-size: 1.2rem;
        font-weight: bold;
        color: #1f77b4;
    }
    .keyword-badge {
        background-color: #ff6b6b;
        color: white;
        padding: 0.2rem 0.5rem;
        border-radius: 4px;
        font-size: 0.8rem;
        margin: 0.2rem;
        display: inline-block;
    }
    .playlist-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)


# Funções auxiliares
@st.cache_data
def load_playlists(playlists_dir='playlists'):
    """Carrega todas as playlists do diretório"""
    playlists_dir = Path(playlists_dir)
    playlists = {}
    
    for json_file in playlists_dir.glob('*.json'):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                playlist_name = data.get('playlist_info', {}).get('title', json_file.stem)
                playlists[playlist_name] = data
        except Exception as e:
            st.error(f"Erro ao carregar {json_file}: {e}")
    
    return playlists


def search_videos(playlists, keywords, operator='AND', search_in='both'):
    """
    Busca vídeos nas playlists
    
    Args:
        playlists: Dicionário com playlists
        keywords: Lista de palavras-chave
        operator: 'AND' ou 'OR'
        search_in: 'title', 'description', ou 'both'
    """
    results = {}
    
    for playlist_name, playlist_data in playlists.items():
        videos = playlist_data.get('videos', [])
        matching_videos = []
        
        for video in videos:
            title = video.get('title', '').lower()
            description = video.get('description', '').lower()
            
            # Determinar onde buscar
            search_text = ''
            if search_in == 'title':
                search_text = title
            elif search_in == 'description':
                search_text = description
            else:  # both
                search_text = f"{title} {description}"
            
            # Verificar keywords com operador
            keywords_lower = [k.lower() for k in keywords]
            
            if operator == 'AND':
                if all(keyword in search_text for keyword in keywords_lower):
                    video_copy = video.copy()
                    video_copy['matched_keywords'] = keywords
                    matching_videos.append(video_copy)
            else:  # OR
                if any(keyword in search_text for keyword in keywords_lower):
                    matched = [k for k in keywords if k.lower() in search_text]
                    video_copy = video.copy()
                    video_copy['matched_keywords'] = matched
                    matching_videos.append(video_copy)
        
        if matching_videos:
            results[playlist_name] = {
                'playlist_info': playlist_data.get('playlist_info', {}),
                'videos': matching_videos
            }
    
    return results


def load_favorites():
    """Carrega vídeos favoritos do arquivo"""
    favorites_file = 'favorites.json'
    if os.path.exists(favorites_file):
        try:
            with open(favorites_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}


def save_favorites(favorites):
    """Salva vídeos favoritos no arquivo"""
    favorites_file = 'favorites.json'
    with open(favorites_file, 'w', encoding='utf-8') as f:
        json.dump(favorites, f, ensure_ascii=False, indent=2)


def get_transcript(video_id, languages=['pt', 'en']):
    """
    Obtém a transcrição de um vídeo do YouTube usando yt-dlp
    
    Args:
        video_id: ID do vídeo
        languages: Lista de idiomas preferidos
    """
    try:
        video_url = f'https://www.youtube.com/watch?v={video_id}'
        
        ydl_opts = {
            'skip_download': True,
            'writesubtitles': True,
            'writeautomaticsub': True,
            'subtitleslangs': languages + ['en-orig', 'en'],
            'quiet': True,
            'no_warnings': True
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            
            # Verificar legendas automáticas primeiro
            if 'automatic_captions' in info and info['automatic_captions']:
                # Tentar idiomas preferidos
                for lang in languages + ['en-orig', 'en']:
                    if lang in info['automatic_captions']:
                        subs = info['automatic_captions'][lang]
                        
                        # Procurar formato json3
                        for sub in subs:
                            if sub.get('ext') == 'json3':
                                # Baixar o conteúdo
                                response = requests.get(sub['url'])
                                if response.status_code == 200:
                                    data = response.json()
                                    
                                    # Extrair texto
                                    transcript = []
                                    if 'events' in data:
                                        for event in data['events']:
                                            if 'segs' in event:
                                                text = ''.join([seg.get('utf8', '') for seg in event['segs']])
                                                if text.strip():
                                                    start = event.get('tStartMs', 0) / 1000
                                                    transcript.append({
                                                        'start': start,
                                                        'text': text.strip()
                                                    })
                                    
                                    if transcript:
                                        return transcript, lang
                                break
            
            # Verificar legendas manuais
            if 'subtitles' in info and info['subtitles']:
                for lang in languages + ['en']:
                    if lang in info['subtitles']:
                        subs = info['subtitles'][lang]
                        
                        for sub in subs:
                            if sub.get('ext') == 'json3':
                                response = requests.get(sub['url'])
                                if response.status_code == 200:
                                    data = response.json()
                                    
                                    transcript = []
                                    if 'events' in data:
                                        for event in data['events']:
                                            if 'segs' in event:
                                                text = ''.join([seg.get('utf8', '') for seg in event['segs']])
                                                if text.strip():
                                                    start = event.get('tStartMs', 0) / 1000
                                                    transcript.append({
                                                        'start': start,
                                                        'text': text.strip()
                                                    })
                                    
                                    if transcript:
                                        return transcript, lang
                                break
        
        return None, "Nenhuma transcrição encontrada"
        
    except Exception as e:
        return None, f"Erro ao obter transcrição: {str(e)}"


def format_transcript(transcript_data):
    """Formata a transcrição para exibição"""
    if not transcript_data:
        return ""
    
    formatted = []
    for entry in transcript_data:
        start_time = int(entry['start'])
        minutes = start_time // 60
        seconds = start_time % 60
        timestamp = f"[{minutes:02d}:{seconds:02d}]"
        text = entry['text']
        formatted.append(f"{timestamp} {text}")
    
    return "\n".join(formatted)


# Interface principal
def main():
    st.title("🎥 YouTube Playlist Manager")
    st.markdown("### Busque, marque e transcreva vídeos das suas playlists")
    
    # Carregar playlists
    playlists = load_playlists()
    
    if not playlists:
        st.error("❌ Nenhuma playlist encontrada no diretório 'playlists/'")
        st.info("Execute o script export_playlists.py primeiro para exportar suas playlists.")
        return
    
    st.success(f"✅ {len(playlists)} playlists carregadas")
    
    # Sidebar - Configurações de busca
    with st.sidebar:
        st.header("🔍 Configurações de Busca")
        
        # Input de keywords
        keywords_input = st.text_area(
            "Palavras-chave (uma por linha)",
            value="RAG\ntext",
            height=100,
            help="Digite uma palavra-chave por linha"
        )
        keywords = [k.strip() for k in keywords_input.split('\n') if k.strip()]
        
        # Operador
        operator = st.radio(
            "Operador lógico",
            options=['AND', 'OR'],
            help="AND: todas as palavras devem estar presentes\nOR: pelo menos uma palavra deve estar presente"
        )
        
        # Onde buscar
        search_in = st.selectbox(
            "Buscar em",
            options=['both', 'title', 'description'],
            format_func=lambda x: {
                'both': '📝 Título e Descrição',
                'title': '📌 Apenas Título',
                'description': '📄 Apenas Descrição'
            }[x]
        )
        
        # Botão de busca
        search_button = st.button("🔍 Buscar", type="primary")
        
        st.divider()
        
        # Estatísticas
        st.header("📊 Estatísticas")
        total_videos = sum(len(p.get('videos', [])) for p in playlists.values())
        st.metric("Total de vídeos", total_videos)
        st.metric("Total de playlists", len(playlists))
        
        # Favoritos
        favorites = load_favorites()
        st.metric("Vídeos favoritos", len(favorites))
    
    # Inicializar session state para manter resultados
    if 'search_results' not in st.session_state:
        st.session_state.search_results = None
    if 'search_keywords' not in st.session_state:
        st.session_state.search_keywords = None
    
    # Área principal
    if search_button and keywords:
        with st.spinner("🔍 Buscando vídeos..."):
            results = search_videos(playlists, keywords, operator, search_in)
            st.session_state.search_results = results
            st.session_state.search_keywords = keywords
    
    # Usar resultados do session state se existirem
    results = st.session_state.search_results
    
    if search_button and keywords and not results:
        st.warning("⚠️ Nenhum vídeo encontrado com os critérios especificados.")
        return
    
    if not results:
        st.info("👈 Configure os critérios de busca na barra lateral e clique em 'Buscar'")
        return
    
    # Resumo dos resultados
    total_found = sum(len(r['videos']) for r in results.values())
    st.success(f"✅ Encontrados **{total_found}** vídeos em **{len(results)}** playlist(s)")
    
    # Tabs para organizar
    tab1, tab2 = st.tabs(["📋 Resultados", "⭐ Favoritos"])
    
    with tab1:
        # Exibir resultados por playlist
        for playlist_name, data in results.items():
            with st.expander(f"📋 {playlist_name} ({len(data['videos'])} vídeos)", expanded=True):
                playlist_url = data['playlist_info'].get('playlist_url', '')
                if playlist_url:
                    st.markdown(f"[🔗 Abrir playlist no YouTube]({playlist_url})")
                
                # Exibir vídeos
                for idx, video in enumerate(data['videos']):
                    video_id = video['video_id']
                    
                    # Card do vídeo
                    col1, col2 = st.columns([0.05, 0.95])
                    
                    with col1:
                        # Checkbox para favoritar
                        is_favorite = video_id in favorites
                        # Criar chave única incluindo playlist e índice
                        unique_key = f"fav_{playlist_name}_{video_id}_{idx}"
                        if st.checkbox("", value=is_favorite, key=unique_key):
                            favorites[video_id] = {
                                'video': video,
                                'playlist': playlist_name,
                                'added_at': datetime.now().isoformat()
                            }
                            save_favorites(favorites)
                        else:
                            if video_id in favorites:
                                del favorites[video_id]
                                save_favorites(favorites)
                    
                    with col2:
                        st.markdown(f"### {idx + 1}. {video['title']}")
                        
                        # Informações em colunas
                        info_col1, info_col2, info_col3 = st.columns(3)
                        
                        with info_col1:
                            st.markdown(f"**📅 Publicado:** {video['published_at'][:10]}")
                        
                        with info_col2:
                            keywords_html = " ".join([
                                f'<span class="keyword-badge">{k}</span>' 
                                for k in video.get('matched_keywords', [])
                            ])
                            st.markdown(f"**🔑 Keywords:** {keywords_html}", unsafe_allow_html=True)
                        
                        with info_col3:
                            st.markdown(f"[🔗 Abrir vídeo]({video['video_url']})")
                        
                        # Descrição
                        with st.expander("📝 Ver descrição"):
                            st.text(video.get('description', 'Sem descrição'))
                        
                        # Botão de transcrição
                        trans_key = f"trans_{playlist_name}_{video_id}_{idx}"
                        if st.button(f"📄 Obter Transcrição", key=trans_key):
                            with st.spinner("Obtendo transcrição..."):
                                transcript_data, lang_or_error = get_transcript(video_id)
                                
                                if transcript_data:
                                    st.success(f"✅ Transcrição obtida (idioma: {lang_or_error})")
                                    formatted_transcript = format_transcript(transcript_data)
                                    
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
                                else:
                                    st.error(f"❌ {lang_or_error}")
                        
                        # Thumbnail
                        if video.get('thumbnail_url'):
                            st.image(video['thumbnail_url'], width=300)
                        
                        st.divider()
        
        with tab2:
            st.header("⭐ Vídeos Favoritos")
            
            if not favorites:
                st.info("Nenhum vídeo favorito ainda. Marque os checkboxes ao lado dos vídeos para adicioná-los aos favoritos.")
            else:
                st.success(f"✅ {len(favorites)} vídeos favoritos")
                
                # Botão para exportar favoritos
                if st.button("📥 Exportar Favoritos para Markdown"):
                    # Criar markdown dos favoritos
                    md_content = f"# ⭐ Vídeos Favoritos\n\n"
                    md_content += f"**Exportado em:** {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n"
                    md_content += f"**Total:** {len(favorites)} vídeos\n\n---\n\n"
                    
                    for video_id, fav_data in favorites.items():
                        video = fav_data['video']
                        playlist = fav_data['playlist']
                        
                        md_content += f"## {video['title']}\n\n"
                        md_content += f"- **Playlist:** {playlist}\n"
                        md_content += f"- **URL:** {video['video_url']}\n"
                        md_content += f"- **Publicado em:** {video['published_at'][:10]}\n"
                        md_content += f"- **Adicionado aos favoritos em:** {fav_data['added_at'][:10]}\n\n"
                        
                        if video.get('description'):
                            md_content += f"**Descrição:**\n\n> {video['description'][:200]}...\n\n"
                        
                        md_content += "---\n\n"
                    
                    st.download_button(
                        label="💾 Baixar Favoritos.md",
                        data=md_content,
                        file_name="Favoritos.md",
                        mime="text/markdown"
                    )
                
                st.divider()
                
                # Listar favoritos
                for video_id, fav_data in favorites.items():
                    video = fav_data['video']
                    playlist = fav_data['playlist']
                    
                    with st.container():
                        col1, col2 = st.columns([0.05, 0.95])
                        
                        with col1:
                            if st.button("❌", key=f"remove_fav_{video_id}"):
                                del favorites[video_id]
                                save_favorites(favorites)
                                st.rerun()
                        
                        with col2:
                            st.markdown(f"### {video['title']}")
                            st.markdown(f"**📋 Playlist:** {playlist}")
                            st.markdown(f"**📅 Publicado:** {video['published_at'][:10]}")
                            st.markdown(f"[🔗 Abrir vídeo]({video['video_url']})")
                            
                            if video.get('thumbnail_url'):
                                st.image(video['thumbnail_url'], width=200)
                        
                        st.divider()


if __name__ == '__main__':
    main()
