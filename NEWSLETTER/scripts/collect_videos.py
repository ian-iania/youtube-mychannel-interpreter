#!/usr/bin/env python3
"""
Coleta vídeos recentes dos canais seguidos
"""

import os
import sys
import json
import pickle
from pathlib import Path
from datetime import datetime, timedelta
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from dotenv import load_dotenv

# Adicionar diretório pai ao path
sys.path.append(str(Path(__file__).parent.parent.parent))

# Carregar variáveis de ambiente
load_dotenv()

# Escopos necessários
SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']

# Arquivo de token
TOKEN_FILE = '../token.pickle'


def get_authenticated_service():
    """
    Autentica o usuário via OAuth 2.0
    Reutiliza token do projeto principal
    
    Returns:
        Serviço autenticado da API do YouTube
    """
    creds = None
    
    # Verificar token existente
    token_paths = [TOKEN_FILE, '../../token.pickle', '../../../token.pickle']
    
    for token_path in token_paths:
        if os.path.exists(token_path):
            with open(token_path, 'rb') as token:
                creds = pickle.load(token)
            break
    
    # Renovar se necessário
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            client_id = os.getenv('OAUTH_CLIENT_ID')
            client_secret = os.getenv('OAUTH_CLIENT_SECRET')
            
            if not client_id or not client_secret:
                print("❌ Erro: Credenciais OAuth não encontradas no .env")
                sys.exit(1)
            
            client_config = {
                "installed": {
                    "client_id": client_id,
                    "client_secret": client_secret,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "redirect_uris": ["http://localhost"]
                }
            }
            
            flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)
    
    return build('youtube', 'v3', credentials=creds)


def get_channel_recent_videos(youtube, channel_id, days=7, max_results=50):
    """
    Busca vídeos recentes de um canal
    
    Args:
        youtube: Cliente autenticado
        channel_id: ID do canal
        days: Número de dias para trás (padrão: 7)
        max_results: Máximo de vídeos (padrão: 50)
        
    Returns:
        Lista de vídeos
    """
    videos = []
    
    try:
        # Calcular data de início
        published_after = (datetime.now() - timedelta(days=days)).isoformat() + 'Z'
        
        # Buscar vídeos
        request = youtube.search().list(
            part='snippet',
            channelId=channel_id,
            publishedAfter=published_after,
            order='date',
            type='video',
            maxResults=max_results
        )
        
        response = request.execute()
        
        if 'items' in response:
            for item in response['items']:
                video_info = {
                    'video_id': item['id']['videoId'],
                    'title': item['snippet']['title'],
                    'description': item['snippet']['description'],
                    'channel_id': item['snippet']['channelId'],
                    'channel_title': item['snippet']['channelTitle'],
                    'published_at': item['snippet']['publishedAt'],
                    'thumbnail_url': item['snippet']['thumbnails'].get('high', {}).get('url', ''),
                    'video_url': f"https://www.youtube.com/watch?v={item['id']['videoId']}"
                }
                videos.append(video_info)
        
        return videos
        
    except HttpError as e:
        print(f"   ⚠️  Erro ao buscar vídeos: {e}")
        return []


def get_video_durations(youtube, video_ids):
    """
    Busca durações de múltiplos vídeos em lote
    Reutilizado do projeto principal
    
    Args:
        youtube: Cliente autenticado
        video_ids: Lista de IDs de vídeos
        
    Returns:
        Dicionário {video_id: duration}
    """
    durations = {}
    
    try:
        # API permite até 50 vídeos por chamada
        for i in range(0, len(video_ids), 50):
            batch = video_ids[i:i+50]
            
            request = youtube.videos().list(
                part='contentDetails,statistics',
                id=','.join(batch)
            )
            
            response = request.execute()
            
            if 'items' in response:
                for item in response['items']:
                    video_id = item['id']
                    duration = item['contentDetails']['duration']
                    
                    # Adicionar também estatísticas
                    stats = item.get('statistics', {})
                    
                    durations[video_id] = {
                        'duration': duration,
                        'view_count': stats.get('viewCount', '0'),
                        'like_count': stats.get('likeCount', '0'),
                        'comment_count': stats.get('commentCount', '0')
                    }
        
        return durations
        
    except HttpError as e:
        print(f"   ⚠️  Erro ao buscar durações: {e}")
        return {}


def parse_duration_to_minutes(duration_iso):
    """
    Converte duração ISO 8601 para minutos
    
    Args:
        duration_iso: String ISO 8601 (ex: PT12M43S)
        
    Returns:
        Duração em minutos (float)
    """
    import re
    
    if not duration_iso or duration_iso == 'PT0S':
        return 0
    
    hours = 0
    minutes = 0
    seconds = 0
    
    hour_match = re.search(r'(\d+)H', duration_iso)
    minute_match = re.search(r'(\d+)M', duration_iso)
    second_match = re.search(r'(\d+)S', duration_iso)
    
    if hour_match:
        hours = int(hour_match.group(1))
    if minute_match:
        minutes = int(minute_match.group(1))
    if second_match:
        seconds = int(second_match.group(1))
    
    return hours * 60 + minutes + seconds / 60


def load_subscriptions(subscriptions_file='subscriptions.json'):
    """
    Carrega lista de inscrições
    
    Args:
        subscriptions_file: Arquivo JSON com inscrições
        
    Returns:
        Lista de canais
    """
    file_path = Path(__file__).parent.parent / subscriptions_file
    
    if not file_path.exists():
        print(f"❌ Erro: Arquivo {subscriptions_file} não encontrado")
        print("   Execute primeiro: python scripts/collect_subscriptions.py")
        sys.exit(1)
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    return data.get('channels', [])


def collect_all_videos(youtube, channels, days=7, max_per_channel=50):
    """
    Coleta vídeos de todos os canais
    
    Args:
        youtube: Cliente autenticado
        channels: Lista de canais
        days: Número de dias para trás
        max_per_channel: Máximo de vídeos por canal
        
    Returns:
        Dicionário com vídeos organizados por canal
    """
    all_videos = {}
    total_videos = 0
    
    print(f"\n🎬 Coletando vídeos dos últimos {days} dias...")
    print(f"   Canais: {len(channels)}")
    print(f"   Máximo por canal: {max_per_channel}")
    print()
    
    for idx, channel in enumerate(channels, 1):
        channel_id = channel['channel_id']
        channel_title = channel['channel_title']
        channel_type = channel.get('type', 'community')
        
        # Ícone por tipo
        icon = {'person': '👤', 'company': '🏢', 'community': '👥'}.get(channel_type, '❓')
        
        print(f"{idx}. {icon} {channel_title}")
        print(f"   ID: {channel_id}")
        
        # Buscar vídeos
        videos = get_channel_recent_videos(youtube, channel_id, days, max_per_channel)
        
        if videos:
            print(f"   📹 Encontrados: {len(videos)} vídeos")
            
            # Buscar durações
            video_ids = [v['video_id'] for v in videos]
            durations = get_video_durations(youtube, video_ids)
            
            # Adicionar durações aos vídeos
            for video in videos:
                video_id = video['video_id']
                if video_id in durations:
                    video['duration'] = durations[video_id]['duration']
                    video['duration_minutes'] = parse_duration_to_minutes(durations[video_id]['duration'])
                    video['view_count'] = durations[video_id]['view_count']
                    video['like_count'] = durations[video_id]['like_count']
                    video['comment_count'] = durations[video_id]['comment_count']
                else:
                    video['duration'] = 'PT0S'
                    video['duration_minutes'] = 0
                    video['view_count'] = '0'
                    video['like_count'] = '0'
                    video['comment_count'] = '0'
            
            # Adicionar tipo de canal
            for video in videos:
                video['channel_type'] = channel_type
            
            all_videos[channel_id] = {
                'channel_info': {
                    'channel_id': channel_id,
                    'channel_title': channel_title,
                    'channel_type': channel_type,
                    'description': channel.get('description', ''),
                    'thumbnail_url': channel.get('thumbnail_url', '')
                },
                'videos': videos
            }
            
            total_videos += len(videos)
            print(f"   ✅ Coletados com durações")
        else:
            print(f"   ℹ️  Nenhum vídeo novo")
        
        print()
    
    print(f"📊 Total de vídeos coletados: {total_videos}")
    
    return all_videos


def categorize_videos(all_videos, duration_threshold=15):
    """
    Categoriza vídeos por duração
    
    Args:
        all_videos: Dicionário com todos os vídeos
        duration_threshold: Limite em minutos (padrão: 15)
        
    Returns:
        Estatísticas e vídeos categorizados
    """
    stats = {
        'total_videos': 0,
        'short_videos': 0,  # ≤15 min
        'long_videos': 0,   # >15 min
        'total_duration_minutes': 0,
        'channels_with_videos': 0
    }
    
    for channel_id, data in all_videos.items():
        videos = data['videos']
        
        if videos:
            stats['channels_with_videos'] += 1
        
        for video in videos:
            stats['total_videos'] += 1
            duration_min = video.get('duration_minutes', 0)
            stats['total_duration_minutes'] += duration_min
            
            if duration_min <= duration_threshold:
                stats['short_videos'] += 1
                video['analysis_type'] = 'full'  # Análise completa
            else:
                stats['long_videos'] += 1
                video['analysis_type'] = 'description'  # Só descrição
    
    return stats


def save_videos(all_videos, stats, days=7, output_file=None):
    """
    Salva vídeos coletados em arquivo JSON
    
    Args:
        all_videos: Dicionário com vídeos
        stats: Estatísticas
        days: Período em dias
        output_file: Nome do arquivo (opcional)
    """
    if output_file is None:
        date_str = datetime.now().strftime('%Y-%m-%d')
        output_file = f"{date_str}_videos.json"
    
    output_path = Path(__file__).parent.parent / 'newsletters' / output_file
    output_path.parent.mkdir(exist_ok=True)
    
    data = {
        'generated_at': datetime.now().isoformat(),
        'period_days': days,
        'statistics': stats,
        'channels': all_videos
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Vídeos salvos em: {output_path}")
    
    # Exibir estatísticas
    print(f"\n📊 Estatísticas:")
    print(f"   📺 Canais com vídeos: {stats['channels_with_videos']}")
    print(f"   🎬 Total de vídeos: {stats['total_videos']}")
    print(f"   ✅ Vídeos curtos (≤15 min): {stats['short_videos']} ({stats['short_videos']/stats['total_videos']*100:.1f}%)")
    print(f"   ⏱️  Vídeos longos (>15 min): {stats['long_videos']} ({stats['long_videos']/stats['total_videos']*100:.1f}%)")
    print(f"   ⏰ Duração total: {stats['total_duration_minutes']:.0f} min ({stats['total_duration_minutes']/60:.1f}h)")


def main():
    """Função principal"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Coleta vídeos recentes dos canais seguidos')
    parser.add_argument('--days', type=int, default=7, help='Número de dias para trás (padrão: 7)')
    parser.add_argument('--max-per-channel', type=int, default=50, help='Máximo de vídeos por canal (padrão: 50)')
    parser.add_argument('--output', type=str, help='Nome do arquivo de saída (opcional)')
    
    args = parser.parse_args()
    
    print("=" * 70)
    print("🎥 YouTube Recent Videos Collector")
    print("=" * 70)
    
    # Autenticar
    print("\n🔐 Autenticando...")
    youtube = get_authenticated_service()
    print("✅ Autenticado!")
    
    # Carregar inscrições
    print("\n📂 Carregando inscrições...")
    channels = load_subscriptions()
    print(f"✅ {len(channels)} canais carregados")
    
    # Coletar vídeos
    all_videos = collect_all_videos(youtube, channels, args.days, args.max_per_channel)
    
    if not all_videos:
        print("⚠️  Nenhum vídeo encontrado no período")
        return
    
    # Categorizar vídeos
    stats = categorize_videos(all_videos)
    
    # Salvar
    save_videos(all_videos, stats, args.days, args.output)
    
    print("\n✨ Coleta concluída com sucesso!")
    print("\nℹ️  Próximo passo: Execute analyze_videos.py para analisar com Gemini")


if __name__ == '__main__':
    main()
