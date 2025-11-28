#!/usr/bin/env python3
"""
Exporta TODAS as suas inscrições do YouTube com informações completas
Script one-shot para setup inicial
"""

import os
import sys
import json
import pickle
from pathlib import Path
from datetime import datetime
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Escopos necessários
SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']
TOKEN_FILE = '../token.pickle'


def get_authenticated_service():
    """Autentica via OAuth 2.0"""
    creds = None
    
    token_paths = [TOKEN_FILE, '../../token.pickle', '../../../token.pickle']
    
    for token_path in token_paths:
        if os.path.exists(token_path):
            print(f"📂 Carregando credenciais de {token_path}...")
            with open(token_path, 'rb') as token:
                creds = pickle.load(token)
            break
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("🔄 Renovando token expirado...")
            creds.refresh(Request())
        else:
            print("🔐 Iniciando autenticação OAuth 2.0...")
            
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
            
            print("✅ Autenticação concluída!")
        
        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)
            print(f"💾 Credenciais salvas em {TOKEN_FILE}")
    
    return build('youtube', 'v3', credentials=creds)


def get_all_subscriptions(youtube):
    """
    Busca TODAS as inscrições do usuário
    
    Args:
        youtube: Cliente autenticado
        
    Returns:
        Lista de channel IDs
    """
    subscriptions = []
    next_page_token = None
    page = 1
    
    print("\n🔍 Buscando suas inscrições...")
    
    try:
        while True:
            request = youtube.subscriptions().list(
                part='snippet',
                mine=True,
                maxResults=50,
                pageToken=next_page_token,
                order='alphabetical'
            )
            
            response = request.execute()
            
            if 'items' in response:
                for item in response['items']:
                    channel_id = item['snippet']['resourceId']['channelId']
                    channel_title = item['snippet']['title']
                    subscriptions.append({
                        'channel_id': channel_id,
                        'channel_title': channel_title
                    })
                
                print(f"   Página {page}: {len(response['items'])} canais encontrados...")
                page += 1
            
            next_page_token = response.get('nextPageToken')
            if not next_page_token:
                break
        
        print(f"\n✅ Total de inscrições encontradas: {len(subscriptions)}")
        return subscriptions
        
    except HttpError as e:
        print(f"❌ Erro ao buscar inscrições: {e}")
        return []


def get_channel_details(youtube, channel_ids):
    """
    Busca detalhes completos de múltiplos canais
    
    Args:
        youtube: Cliente autenticado
        channel_ids: Lista de channel IDs
        
    Returns:
        Lista de informações completas dos canais
    """
    channels_info = []
    
    print(f"\n📊 Buscando detalhes de {len(channel_ids)} canais...")
    
    try:
        # API permite até 50 canais por chamada
        for i in range(0, len(channel_ids), 50):
            batch = channel_ids[i:i+50]
            
            print(f"   Processando lote {i//50 + 1} ({len(batch)} canais)...")
            
            request = youtube.channels().list(
                part='snippet,statistics,contentDetails,brandingSettings',
                id=','.join(batch)
            )
            
            response = request.execute()
            
            if 'items' in response:
                for channel in response['items']:
                    # Extrair informações
                    snippet = channel['snippet']
                    statistics = channel.get('statistics', {})
                    branding = channel.get('brandingSettings', {}).get('channel', {})
                    
                    channel_info = {
                        # Identificação
                        'channel_id': channel['id'],
                        'channel_title': snippet['title'],
                        'handle': snippet.get('customUrl', ''),
                        
                        # Descrição
                        'description': snippet.get('description', ''),
                        
                        # Estatísticas
                        'subscriber_count': statistics.get('subscriberCount', '0'),
                        'video_count': statistics.get('videoCount', '0'),
                        'view_count': statistics.get('viewCount', '0'),
                        
                        # Mídia
                        'thumbnail_url': snippet['thumbnails'].get('high', {}).get('url', ''),
                        'banner_url': branding.get('bannerExternalUrl', ''),
                        
                        # Datas
                        'published_at': snippet['publishedAt'],
                        'created_date': snippet['publishedAt'][:10],
                        
                        # Extras
                        'country': snippet.get('country', ''),
                        'keywords': branding.get('keywords', ''),
                        
                        # Para classificação manual posterior
                        'type': 'unknown',  # Será classificado manualmente
                        'category': ''       # Categoria de conteúdo
                    }
                    
                    channels_info.append(channel_info)
        
        print(f"✅ Detalhes coletados: {len(channels_info)} canais")
        return channels_info
        
    except HttpError as e:
        print(f"❌ Erro ao buscar detalhes: {e}")
        return []


def classify_channels_by_size(channels):
    """
    Classifica canais por tamanho (inscritos)
    
    Args:
        channels: Lista de canais
        
    Returns:
        Canais classificados
    """
    for channel in channels:
        subs = int(channel['subscriber_count'])
        
        if subs >= 1000000:
            channel['size_category'] = 'mega'  # 1M+
        elif subs >= 100000:
            channel['size_category'] = 'large'  # 100K+
        elif subs >= 10000:
            channel['size_category'] = 'medium'  # 10K+
        else:
            channel['size_category'] = 'small'  # <10K
    
    return channels


def save_subscriptions(channels, output_file='all_subscriptions.json'):
    """
    Salva todas as inscrições em arquivo JSON
    
    Args:
        channels: Lista de canais
        output_file: Nome do arquivo
    """
    output_path = Path(__file__).parent.parent / output_file
    
    # Estatísticas
    total_subs = sum(int(c['subscriber_count']) for c in channels)
    total_videos = sum(int(c['video_count']) for c in channels)
    
    size_stats = {
        'mega': len([c for c in channels if c['size_category'] == 'mega']),
        'large': len([c for c in channels if c['size_category'] == 'large']),
        'medium': len([c for c in channels if c['size_category'] == 'medium']),
        'small': len([c for c in channels if c['size_category'] == 'small'])
    }
    
    data = {
        'exported_at': datetime.now().isoformat(),
        'total_channels': len(channels),
        'statistics': {
            'total_subscribers': total_subs,
            'total_videos': total_videos,
            'avg_subscribers_per_channel': total_subs // len(channels) if channels else 0,
            'size_distribution': size_stats
        },
        'channels': sorted(channels, key=lambda x: int(x['subscriber_count']), reverse=True)
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Inscrições salvas em: {output_path}")
    
    # Exibir estatísticas
    print(f"\n📊 Estatísticas Gerais:")
    print(f"   📺 Total de canais: {len(channels)}")
    print(f"   👥 Total de inscritos (todos os canais): {total_subs:,}")
    print(f"   🎬 Total de vídeos (todos os canais): {total_videos:,}")
    print(f"   📈 Média de inscritos por canal: {total_subs // len(channels):,}")
    
    print(f"\n📊 Distribuição por Tamanho:")
    print(f"   🏆 Mega (1M+): {size_stats['mega']} canais")
    print(f"   🥇 Large (100K+): {size_stats['large']} canais")
    print(f"   🥈 Medium (10K+): {size_stats['medium']} canais")
    print(f"   🥉 Small (<10K): {size_stats['small']} canais")
    
    # Top 10
    print(f"\n🏆 Top 10 Canais (por inscritos):")
    for idx, channel in enumerate(channels[:10], 1):
        subs = int(channel['subscriber_count'])
        print(f"   {idx:2d}. {channel['channel_title'][:50]:50s} - {subs:,} inscritos")


def create_manual_classification_template(channels, output_file='channels_to_classify.txt'):
    """
    Cria arquivo de texto para classificação manual
    
    Args:
        channels: Lista de canais
        output_file: Nome do arquivo
    """
    output_path = Path(__file__).parent.parent / output_file
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# Classificação Manual de Canais\n")
        f.write("# Edite o tipo de cada canal: person | company | community\n")
        f.write("# Formato: channel_id | tipo | categoria (opcional)\n")
        f.write("#\n")
        f.write("# Exemplos:\n")
        f.write("# UCxX9wt5FWQUAAz4UrysqK9A | person | AI tutorials\n")
        f.write("# UCaiL2GDNpLYH6Wokkk1VNcg | company | AI research\n")
        f.write("# UCbfYPyITQ-7l4upoX8nvctg | community | paper reviews\n")
        f.write("#\n\n")
        
        for channel in sorted(channels, key=lambda x: x['channel_title']):
            subs = int(channel['subscriber_count'])
            f.write(f"{channel['channel_id']} | unknown | # {channel['channel_title']} ({subs:,} subs)\n")
    
    print(f"\n📝 Template de classificação criado: {output_path}")
    print(f"   Edite este arquivo para classificar os canais manualmente")


def main():
    """Função principal"""
    print("=" * 70)
    print("📺 YouTube Subscriptions Exporter")
    print("   Export completo de TODAS as suas inscrições")
    print("=" * 70)
    
    # Autenticar
    youtube = get_authenticated_service()
    
    # Buscar inscrições
    subscriptions = get_all_subscriptions(youtube)
    
    if not subscriptions:
        print("⚠️  Nenhuma inscrição encontrada")
        return
    
    # Extrair channel IDs
    channel_ids = [sub['channel_id'] for sub in subscriptions]
    
    # Buscar detalhes completos
    channels = get_channel_details(youtube, channel_ids)
    
    if not channels:
        print("❌ Erro ao buscar detalhes dos canais")
        return
    
    # Classificar por tamanho
    channels = classify_channels_by_size(channels)
    
    # Salvar
    save_subscriptions(channels)
    
    # Criar template para classificação manual
    create_manual_classification_template(channels)
    
    print("\n✨ Exportação concluída com sucesso!")
    print("\n📋 Próximos passos:")
    print("   1. Revise o arquivo all_subscriptions.json")
    print("   2. (Opcional) Classifique os canais editando channels_to_classify.txt")
    print("   3. Execute collect_videos.py para buscar vídeos recentes")


if __name__ == '__main__':
    main()
