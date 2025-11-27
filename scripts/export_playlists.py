#!/usr/bin/env python3
"""
Script para exportar todas as playlists públicas de um canal e seus vídeos
Cria um arquivo JSON para cada playlist com informações detalhadas dos vídeos
"""

import os
import sys
import json
from datetime import datetime
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()


def get_channel_playlists(youtube, channel_id):
    """
    Lista todas as playlists de um canal
    
    Args:
        youtube: Cliente da API do YouTube
        channel_id: ID do canal
        
    Returns:
        Lista de playlists do canal
    """
    playlists = []
    next_page_token = None
    
    try:
        while True:
            request = youtube.playlists().list(
                part='snippet,contentDetails',
                channelId=channel_id,
                maxResults=50,
                pageToken=next_page_token
            )
            
            response = request.execute()
            
            if 'items' in response:
                playlists.extend(response['items'])
            
            next_page_token = response.get('nextPageToken')
            if not next_page_token:
                break
        
        return playlists
        
    except HttpError as e:
        print(f"❌ Erro ao buscar playlists: {e}")
        return None


def get_playlist_videos(youtube, playlist_id):
    """
    Obtém todos os vídeos de uma playlist
    
    Args:
        youtube: Cliente da API do YouTube
        playlist_id: ID da playlist
        
    Returns:
        Lista de vídeos da playlist
    """
    videos = []
    next_page_token = None
    
    try:
        while True:
            request = youtube.playlistItems().list(
                part='snippet,contentDetails',
                playlistId=playlist_id,
                maxResults=50,
                pageToken=next_page_token
            )
            
            response = request.execute()
            
            if 'items' in response:
                for item in response['items']:
                    video_info = {
                        'video_id': item['contentDetails']['videoId'],
                        'title': item['snippet']['title'],
                        'description': item['snippet']['description'],
                        'channel_title': item['snippet']['channelTitle'],
                        'published_at': item['snippet']['publishedAt'],
                        'position': item['snippet']['position'],
                        'thumbnail_url': item['snippet']['thumbnails'].get('high', {}).get('url', ''),
                        'video_url': f"https://www.youtube.com/watch?v={item['contentDetails']['videoId']}"
                    }
                    videos.append(video_info)
            
            next_page_token = response.get('nextPageToken')
            if not next_page_token:
                break
        
        return videos
        
    except HttpError as e:
        print(f"❌ Erro ao buscar vídeos da playlist: {e}")
        return None


def sanitize_filename(filename):
    """
    Remove caracteres inválidos do nome do arquivo
    
    Args:
        filename: Nome do arquivo original
        
    Returns:
        Nome do arquivo sanitizado
    """
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename


def export_playlist_to_json(playlist_info, videos, output_dir='playlists'):
    """
    Exporta informações da playlist e vídeos para um arquivo JSON
    
    Args:
        playlist_info: Informações da playlist
        videos: Lista de vídeos
        output_dir: Diretório de saída
        
    Returns:
        Caminho do arquivo criado
    """
    try:
        # Criar diretório se não existir
        os.makedirs(output_dir, exist_ok=True)
        
        # Preparar dados para exportação
        export_data = {
            'playlist_info': {
                'id': playlist_info['id'],
                'title': playlist_info['snippet']['title'],
                'description': playlist_info['snippet']['description'],
                'channel_id': playlist_info['snippet']['channelId'],
                'channel_title': playlist_info['snippet']['channelTitle'],
                'published_at': playlist_info['snippet']['publishedAt'],
                'video_count': playlist_info['contentDetails']['itemCount'],
                'playlist_url': f"https://www.youtube.com/playlist?list={playlist_info['id']}"
            },
            'videos': videos,
            'export_date': datetime.now().isoformat(),
            'total_videos_exported': len(videos)
        }
        
        # Nome do arquivo baseado no título da playlist
        filename = sanitize_filename(playlist_info['snippet']['title'])
        filepath = os.path.join(output_dir, f"{filename}.json")
        
        # Salvar arquivo JSON
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)
        
        return filepath
        
    except Exception as e:
        print(f"❌ Erro ao exportar playlist: {e}")
        return None


def main():
    """Função principal"""
    
    # Obter configurações do ambiente
    api_key = os.getenv('YOUTUBE_API_KEY')
    channel_id = os.getenv('YOUTUBE_CHANNEL_ID')
    channel_name = os.getenv('YOUTUBE_CHANNEL_NAME', 'Unknown')
    
    if not api_key:
        print("❌ ERRO: YOUTUBE_API_KEY não encontrada no arquivo .env")
        sys.exit(1)
    
    if not channel_id:
        print("❌ ERRO: YOUTUBE_CHANNEL_ID não encontrada no arquivo .env")
        sys.exit(1)
    
    print("=" * 80)
    print("EXPORTADOR DE PLAYLISTS DO YOUTUBE")
    print("=" * 80)
    print()
    print(f"🔑 API Key: Carregada")
    print(f"📺 Canal: {channel_name}")
    print(f"🆔 Channel ID: {channel_id}")
    print()
    print("=" * 80)
    print()
    
    # Criar cliente da API
    youtube = build('youtube', 'v3', developerKey=api_key)
    
    # Buscar playlists do canal
    print("📋 Buscando playlists do canal...")
    playlists = get_channel_playlists(youtube, channel_id)
    
    if not playlists:
        print("❌ Nenhuma playlist encontrada ou erro ao buscar.")
        sys.exit(1)
    
    print(f"✅ Encontradas {len(playlists)} playlists públicas!")
    print()
    
    # Processar cada playlist
    total_videos = 0
    exported_files = []
    
    for idx, playlist in enumerate(playlists, 1):
        playlist_title = playlist['snippet']['title']
        playlist_id = playlist['id']
        video_count = playlist['contentDetails']['itemCount']
        
        print(f"[{idx}/{len(playlists)}] 📋 {playlist_title}")
        print(f"    🆔 ID: {playlist_id}")
        print(f"    📊 Vídeos: {video_count}")
        
        # Buscar vídeos da playlist
        print(f"    ⏳ Buscando vídeos...")
        videos = get_playlist_videos(youtube, playlist_id)
        
        if videos is not None:
            # Exportar para JSON
            filepath = export_playlist_to_json(playlist, videos, output_dir='playlists')
            
            if filepath:
                print(f"    ✅ Exportado: {filepath}")
                print(f"    📹 Total de vídeos exportados: {len(videos)}")
                exported_files.append(filepath)
                total_videos += len(videos)
            else:
                print(f"    ❌ Erro ao exportar playlist")
        else:
            print(f"    ❌ Erro ao buscar vídeos")
        
        print()
    
    # Resumo final
    print("=" * 80)
    print("📊 RESUMO DA EXPORTAÇÃO")
    print("=" * 80)
    print(f"✅ Playlists exportadas: {len(exported_files)}/{len(playlists)}")
    print(f"📹 Total de vídeos exportados: {total_videos}")
    print(f"📁 Diretório: ./playlists/")
    print()
    print("Arquivos criados:")
    for filepath in exported_files:
        print(f"  - {filepath}")
    print()
    print("=" * 80)


if __name__ == '__main__':
    main()
