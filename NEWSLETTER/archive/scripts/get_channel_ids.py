#!/usr/bin/env python3
"""
Converte URLs ou handles de canais do YouTube em Channel IDs
"""

import os
import sys
import json
import pickle
from pathlib import Path
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
            with open(token_path, 'rb') as token:
                creds = pickle.load(token)
            break
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            client_id = os.getenv('OAUTH_CLIENT_ID')
            client_secret = os.getenv('OAUTH_CLIENT_SECRET')
            
            if not client_id or not client_secret:
                print("❌ Erro: Credenciais OAuth não encontradas")
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


def extract_handle_from_url(url):
    """
    Extrai handle de URL do YouTube
    
    Args:
        url: URL do canal (ex: https://www.youtube.com/@HuggingFace)
        
    Returns:
        Handle sem @ (ex: HuggingFace)
    """
    # Remover protocolo e domínio
    if 'youtube.com/@' in url:
        handle = url.split('/@')[-1]
    elif url.startswith('@'):
        handle = url[1:]
    else:
        handle = url
    
    # Remover trailing slash e query params
    handle = handle.split('/')[0].split('?')[0]
    
    return handle


def get_channel_id_from_handle(youtube, handle):
    """
    Busca Channel ID a partir do handle
    
    Args:
        youtube: Cliente autenticado
        handle: Handle do canal (ex: HuggingFace)
        
    Returns:
        Dicionário com informações do canal
    """
    try:
        # Buscar canal pelo handle
        request = youtube.search().list(
            part='snippet',
            q=f"@{handle}",
            type='channel',
            maxResults=1
        )
        
        response = request.execute()
        
        if 'items' in response and len(response['items']) > 0:
            item = response['items'][0]
            channel_id = item['snippet']['channelId']
            
            # Buscar detalhes completos do canal
            channel_request = youtube.channels().list(
                part='snippet,statistics,contentDetails',
                id=channel_id
            )
            
            channel_response = channel_request.execute()
            
            if 'items' in channel_response and len(channel_response['items']) > 0:
                channel = channel_response['items'][0]
                
                return {
                    'channel_id': channel_id,
                    'channel_title': channel['snippet']['title'],
                    'handle': f"@{handle}",
                    'description': channel['snippet']['description'],
                    'subscriber_count': channel['statistics'].get('subscriberCount', '0'),
                    'video_count': channel['statistics'].get('videoCount', '0'),
                    'thumbnail_url': channel['snippet']['thumbnails'].get('high', {}).get('url', ''),
                    'custom_url': channel['snippet'].get('customUrl', ''),
                    'published_at': channel['snippet']['publishedAt']
                }
        
        return None
        
    except HttpError as e:
        print(f"❌ Erro ao buscar canal: {e}")
        return None


def process_channel_list(youtube, channels_input):
    """
    Processa lista de canais (URLs ou handles)
    
    Args:
        youtube: Cliente autenticado
        channels_input: Lista de URLs ou handles
        
    Returns:
        Lista de informações de canais
    """
    results = []
    
    print(f"\n🔍 Processando {len(channels_input)} canais...")
    print()
    
    for idx, channel_input in enumerate(channels_input, 1):
        # Extrair handle
        handle = extract_handle_from_url(channel_input.strip())
        
        print(f"{idx}. @{handle}")
        
        # Buscar informações
        channel_info = get_channel_id_from_handle(youtube, handle)
        
        if channel_info:
            print(f"   ✅ {channel_info['channel_title']}")
            print(f"   📺 ID: {channel_info['channel_id']}")
            print(f"   👥 Inscritos: {int(channel_info['subscriber_count']):,}")
            print(f"   🎬 Vídeos: {int(channel_info['video_count']):,}")
            results.append(channel_info)
        else:
            print(f"   ❌ Canal não encontrado")
        
        print()
    
    return results


def save_channel_ids(channels, output_file='channel_ids.json'):
    """
    Salva Channel IDs em arquivo JSON
    
    Args:
        channels: Lista de informações de canais
        output_file: Nome do arquivo
    """
    from datetime import datetime
    
    output_path = Path(__file__).parent.parent / output_file
    
    data = {
        'generated_at': datetime.now().isoformat(),
        'total_channels': len(channels),
        'channels': channels
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"💾 Channel IDs salvos em: {output_path}")


def main():
    """Função principal"""
    from datetime import datetime
    import argparse
    
    parser = argparse.ArgumentParser(description='Converte URLs/handles em Channel IDs')
    parser.add_argument('--input', type=str, help='Arquivo com lista de URLs/handles (um por linha)')
    parser.add_argument('--channels', nargs='+', help='Lista de URLs/handles diretamente')
    parser.add_argument('--output', type=str, default='channel_ids.json', help='Arquivo de saída')
    
    args = parser.parse_args()
    
    print("=" * 70)
    print("🔍 YouTube Channel ID Finder")
    print("=" * 70)
    
    # Autenticar
    print("\n🔐 Autenticando...")
    youtube = get_authenticated_service()
    print("✅ Autenticado!")
    
    # Obter lista de canais
    channels_input = []
    
    if args.input:
        # Ler de arquivo
        input_path = Path(__file__).parent.parent / args.input
        if input_path.exists():
            with open(input_path, 'r', encoding='utf-8') as f:
                channels_input = [line.strip() for line in f if line.strip()]
        else:
            print(f"❌ Erro: Arquivo {args.input} não encontrado")
            sys.exit(1)
    elif args.channels:
        # Usar argumentos
        channels_input = args.channels
    else:
        # Modo interativo
        print("\n📝 Digite as URLs ou handles dos canais (um por linha)")
        print("   Exemplos:")
        print("   - https://www.youtube.com/@HuggingFace")
        print("   - @OpenAI")
        print("   - HuggingFace")
        print("\n   Digite 'done' quando terminar:")
        print()
        
        while True:
            line = input("Canal: ").strip()
            if line.lower() == 'done':
                break
            if line:
                channels_input.append(line)
    
    if not channels_input:
        print("❌ Nenhum canal fornecido")
        sys.exit(1)
    
    # Processar
    channels = process_channel_list(youtube, channels_input)
    
    if not channels:
        print("❌ Nenhum canal encontrado")
        return
    
    # Salvar
    save_channel_ids(channels, args.output)
    
    print(f"\n✨ Processamento concluído!")
    print(f"   ✅ Canais encontrados: {len(channels)}/{len(channels_input)}")
    
    # Exibir resumo
    print(f"\n📊 Resumo:")
    for channel in channels:
        print(f"   • {channel['channel_title']} ({channel['handle']})")
        print(f"     ID: {channel['channel_id']}")


if __name__ == '__main__':
    main()
