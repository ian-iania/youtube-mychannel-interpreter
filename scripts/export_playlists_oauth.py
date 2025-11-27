#!/usr/bin/env python3
"""
Script para exportar TODAS as playlists (públicas e privadas) usando OAuth 2.0
Requer autenticação do usuário para acessar playlists privadas
"""

import os
import sys
import json
import pickle
from datetime import datetime
from pathlib import Path
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Escopos necessários para acessar playlists privadas
SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']

# Arquivo para armazenar credenciais OAuth
TOKEN_FILE = 'token.pickle'


def get_authenticated_service():
    """
    Autentica o usuário via OAuth 2.0 e retorna o serviço do YouTube
    
    Returns:
        Serviço autenticado da API do YouTube
    """
    creds = None
    
    # Verificar se já existe um token salvo
    if os.path.exists(TOKEN_FILE):
        print("📂 Carregando credenciais salvas...")
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)
    
    # Se não há credenciais válidas, fazer login
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("🔄 Renovando token expirado...")
            creds.refresh(Request())
        else:
            print("🔐 Iniciando autenticação OAuth 2.0...")
            print("ℹ️  Uma janela do navegador será aberta para você fazer login")
            
            # Carregar credenciais OAuth do arquivo .env
            client_id = os.getenv('OAUTH_CLIENT_ID')
            client_secret = os.getenv('OAUTH_CLIENT_SECRET')
            
            if not client_id or not client_secret:
                print("❌ Erro: OAUTH_CLIENT_ID e OAUTH_CLIENT_SECRET não encontrados no .env")
                print("ℹ️  Adicione as seguintes linhas ao arquivo .env:")
                print("   OAUTH_CLIENT_ID=seu_client_id")
                print("   OAUTH_CLIENT_SECRET=seu_client_secret")
                sys.exit(1)
            
            # Criar configuração do cliente OAuth
            client_config = {
                "installed": {
                    "client_id": client_id,
                    "client_secret": client_secret,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "redirect_uris": ["http://localhost"]
                }
            }
            
            flow = InstalledAppFlow.from_client_config(
                client_config,
                SCOPES
            )
            creds = flow.run_local_server(port=0)
            
            print("✅ Autenticação concluída!")
        
        # Salvar credenciais para próxima execução
        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)
            print(f"💾 Credenciais salvas em {TOKEN_FILE}")
    
    return build('youtube', 'v3', credentials=creds)


def get_my_playlists(youtube):
    """
    Lista TODAS as playlists do usuário autenticado (públicas e privadas)
    
    Args:
        youtube: Cliente autenticado da API do YouTube
        
    Returns:
        Lista de playlists do usuário
    """
    playlists = []
    next_page_token = None
    
    try:
        print("\n🔍 Buscando suas playlists (públicas e privadas)...")
        
        while True:
            request = youtube.playlists().list(
                part='snippet,contentDetails,status',
                mine=True,  # Busca playlists do usuário autenticado
                maxResults=50,
                pageToken=next_page_token
            )
            
            response = request.execute()
            
            if 'items' in response:
                playlists.extend(response['items'])
                print(f"   Encontradas {len(response['items'])} playlists nesta página...")
            
            next_page_token = response.get('nextPageToken')
            if not next_page_token:
                break
        
        print(f"✅ Total de playlists encontradas: {len(playlists)}")
        
        # Mostrar estatísticas de privacidade
        public_count = sum(1 for p in playlists if p['status']['privacyStatus'] == 'public')
        private_count = sum(1 for p in playlists if p['status']['privacyStatus'] == 'private')
        unlisted_count = sum(1 for p in playlists if p['status']['privacyStatus'] == 'unlisted')
        
        print(f"   📊 Públicas: {public_count} | Privadas: {private_count} | Não listadas: {unlisted_count}")
        
        return playlists
        
    except HttpError as e:
        print(f"❌ Erro ao buscar playlists: {e}")
        return None


def get_video_durations(youtube, video_ids):
    """
    Obtém a duração de múltiplos vídeos em uma única chamada
    
    Args:
        youtube: Cliente autenticado da API do YouTube
        video_ids: Lista de IDs de vídeos
        
    Returns:
        Dicionário {video_id: duration_string}
    """
    durations = {}
    
    try:
        # API permite até 50 vídeos por chamada
        for i in range(0, len(video_ids), 50):
            batch = video_ids[i:i+50]
            
            request = youtube.videos().list(
                part='contentDetails',
                id=','.join(batch)
            )
            
            response = request.execute()
            
            if 'items' in response:
                for item in response['items']:
                    video_id = item['id']
                    duration = item['contentDetails']['duration']
                    durations[video_id] = duration
        
        return durations
        
    except HttpError as e:
        print(f"   ⚠️  Erro ao buscar durações: {e}")
        return {}


def get_playlist_videos(youtube, playlist_id):
    """
    Obtém todos os vídeos de uma playlist (pública ou privada)
    
    Args:
        youtube: Cliente autenticado da API do YouTube
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
        
        # Buscar durações de todos os vídeos
        if videos:
            print(f"   📊 Buscando durações de {len(videos)} vídeos...")
            video_ids = [v['video_id'] for v in videos]
            durations = get_video_durations(youtube, video_ids)
            
            # Adicionar duração a cada vídeo
            for video in videos:
                video['duration'] = durations.get(video['video_id'], 'PT0S')
        
        return videos
        
    except HttpError as e:
        print(f"   ⚠️  Erro ao buscar vídeos: {e}")
        return []


def export_playlist_to_json(playlist_data, output_dir='playlists_oauth'):
    """
    Exporta dados de uma playlist para arquivo JSON
    
    Args:
        playlist_data: Dicionário com dados da playlist
        output_dir: Diretório de saída
    """
    # Criar diretório se não existir
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    # Nome do arquivo (sanitizado)
    playlist_name = playlist_data['playlist_info']['title']
    safe_name = "".join(c for c in playlist_name if c.isalnum() or c in (' ', '-', '_')).strip()
    safe_name = safe_name.replace(' ', '_')
    filename = f"{safe_name}.json"
    
    # Caminho completo
    filepath = output_path / filename
    
    # Salvar JSON
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(playlist_data, f, ensure_ascii=False, indent=2)
    
    return filepath


def main():
    """Função principal"""
    print("=" * 70)
    print("🎥 YouTube Playlist Exporter - OAuth 2.0 (Playlists Privadas)")
    print("=" * 70)
    
    # Autenticar usuário
    try:
        youtube = get_authenticated_service()
    except Exception as e:
        print(f"❌ Erro na autenticação: {e}")
        sys.exit(1)
    
    # Buscar playlists do usuário
    playlists = get_my_playlists(youtube)
    
    if not playlists:
        print("❌ Nenhuma playlist encontrada ou erro ao buscar")
        sys.exit(1)
    
    # Processar cada playlist
    print(f"\n📦 Exportando {len(playlists)} playlists...")
    print("-" * 70)
    
    exported_count = 0
    total_videos = 0
    
    for idx, playlist in enumerate(playlists, 1):
        playlist_id = playlist['id']
        playlist_title = playlist['snippet']['title']
        privacy_status = playlist['status']['privacyStatus']
        video_count = playlist['contentDetails']['itemCount']
        
        # Ícone baseado na privacidade
        privacy_icon = {
            'public': '🌐',
            'private': '🔒',
            'unlisted': '🔗'
        }.get(privacy_status, '❓')
        
        print(f"\n{idx}. {privacy_icon} {playlist_title}")
        print(f"   ID: {playlist_id}")
        print(f"   Status: {privacy_status.upper()}")
        print(f"   Vídeos: {video_count}")
        
        # Buscar vídeos da playlist
        print(f"   📥 Baixando vídeos...")
        videos = get_playlist_videos(youtube, playlist_id)
        
        if videos:
            # Preparar dados para exportação
            playlist_data = {
                'playlist_info': {
                    'id': playlist_id,
                    'title': playlist_title,
                    'description': playlist['snippet'].get('description', ''),
                    'privacy_status': privacy_status,
                    'published_at': playlist['snippet']['publishedAt'],
                    'channel_id': playlist['snippet']['channelId'],
                    'channel_title': playlist['snippet']['channelTitle'],
                    'video_count': len(videos),
                    'playlist_url': f"https://www.youtube.com/playlist?list={playlist_id}",
                    'exported_at': datetime.now().isoformat()
                },
                'videos': videos
            }
            
            # Exportar para JSON
            filepath = export_playlist_to_json(playlist_data)
            print(f"   ✅ Exportada: {filepath}")
            
            exported_count += 1
            total_videos += len(videos)
        else:
            print(f"   ⚠️  Nenhum vídeo encontrado ou erro ao buscar")
    
    # Resumo final
    print("\n" + "=" * 70)
    print("📊 RESUMO DA EXPORTAÇÃO")
    print("=" * 70)
    print(f"✅ Playlists exportadas: {exported_count}/{len(playlists)}")
    print(f"🎬 Total de vídeos: {total_videos}")
    print(f"📁 Diretório: playlists_oauth/")
    print("=" * 70)
    print("\n✨ Exportação concluída com sucesso!")
    print("ℹ️  As playlists privadas agora estão acessíveis!")


if __name__ == '__main__':
    main()
