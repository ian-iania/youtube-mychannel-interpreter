#!/usr/bin/env python3
"""
Coleta lista de canais que você segue (inscrições) usando OAuth 2.0
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

# Adicionar diretório pai ao path para importar funções
sys.path.append(str(Path(__file__).parent.parent.parent))

# Carregar variáveis de ambiente
load_dotenv()

# Escopos necessários
SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']

# Arquivo para armazenar credenciais OAuth
TOKEN_FILE = '../token.pickle'


def get_authenticated_service():
    """
    Autentica o usuário via OAuth 2.0 e retorna o serviço do YouTube
    Reutiliza token do projeto principal se existir
    
    Returns:
        Serviço autenticado da API do YouTube
    """
    creds = None
    
    # Verificar se já existe um token salvo (projeto principal)
    token_paths = [
        TOKEN_FILE,
        '../../token.pickle',
        '../../../token.pickle'
    ]
    
    for token_path in token_paths:
        if os.path.exists(token_path):
            print(f"📂 Carregando credenciais de {token_path}...")
            with open(token_path, 'rb') as token:
                creds = pickle.load(token)
            break
    
    # Se não há credenciais válidas, fazer login
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("🔄 Renovando token expirado...")
            creds.refresh(Request())
        else:
            print("🔐 Iniciando autenticação OAuth 2.0...")
            
            # Carregar credenciais OAuth do arquivo .env
            client_id = os.getenv('OAUTH_CLIENT_ID')
            client_secret = os.getenv('OAUTH_CLIENT_SECRET')
            
            if not client_id or not client_secret:
                print("❌ Erro: OAUTH_CLIENT_ID e OAUTH_CLIENT_SECRET não encontrados no .env")
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
        
        # Salvar credenciais
        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)
            print(f"💾 Credenciais salvas em {TOKEN_FILE}")
    
    return build('youtube', 'v3', credentials=creds)


def get_my_subscriptions(youtube, max_results=50):
    """
    Lista todos os canais que você segue
    
    Args:
        youtube: Cliente autenticado da API do YouTube
        max_results: Máximo de resultados por página (padrão: 50)
        
    Returns:
        Lista de canais com metadados
    """
    subscriptions = []
    next_page_token = None
    
    try:
        print(f"\n🔍 Buscando suas inscrições...")
        
        while True:
            request = youtube.subscriptions().list(
                part='snippet,contentDetails',
                mine=True,
                maxResults=max_results,
                pageToken=next_page_token,
                order='alphabetical'
            )
            
            response = request.execute()
            
            if 'items' in response:
                for item in response['items']:
                    channel_info = {
                        'channel_id': item['snippet']['resourceId']['channelId'],
                        'channel_title': item['snippet']['title'],
                        'description': item['snippet']['description'],
                        'thumbnail_url': item['snippet']['thumbnails'].get('high', {}).get('url', ''),
                        'published_at': item['snippet']['publishedAt'],
                        'total_videos': item['contentDetails']['totalItemCount']
                    }
                    subscriptions.append(channel_info)
                
                print(f"   Encontrados {len(response['items'])} canais nesta página...")
            
            next_page_token = response.get('nextPageToken')
            if not next_page_token:
                break
        
        print(f"✅ Total de inscrições encontradas: {len(subscriptions)}")
        return subscriptions
        
    except HttpError as e:
        print(f"❌ Erro ao buscar inscrições: {e}")
        return []


def load_channel_metadata():
    """
    Carrega metadados de canais (tipo: pessoa/empresa/comunidade)
    
    Returns:
        Dicionário com metadados
    """
    metadata_file = Path(__file__).parent.parent / 'channel_metadata.json'
    
    if metadata_file.exists():
        with open(metadata_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    return {'channels': {}, 'default_type': 'community'}


def enrich_with_metadata(subscriptions, metadata):
    """
    Enriquece dados de inscrições com metadados
    
    Args:
        subscriptions: Lista de inscrições
        metadata: Metadados de canais
        
    Returns:
        Lista enriquecida
    """
    enriched = []
    
    for sub in subscriptions:
        channel_id = sub['channel_id']
        
        # Adicionar metadados se existir
        if channel_id in metadata['channels']:
            sub['type'] = metadata['channels'][channel_id]['type']
            sub['metadata_description'] = metadata['channels'][channel_id].get('description', '')
        else:
            sub['type'] = metadata.get('default_type', 'community')
            sub['metadata_description'] = ''
        
        enriched.append(sub)
    
    return enriched


def save_subscriptions(subscriptions, output_file='subscriptions.json'):
    """
    Salva lista de inscrições em arquivo JSON
    
    Args:
        subscriptions: Lista de inscrições
        output_file: Nome do arquivo de saída
    """
    output_path = Path(__file__).parent.parent / output_file
    
    data = {
        'generated_at': datetime.now().isoformat(),
        'total_channels': len(subscriptions),
        'channels': subscriptions
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Inscrições salvas em: {output_path}")
    
    # Estatísticas por tipo
    types_count = {}
    for sub in subscriptions:
        channel_type = sub.get('type', 'unknown')
        types_count[channel_type] = types_count.get(channel_type, 0) + 1
    
    print(f"\n📊 Estatísticas:")
    for channel_type, count in sorted(types_count.items()):
        icon = {'person': '👤', 'company': '🏢', 'community': '👥'}.get(channel_type, '❓')
        print(f"   {icon} {channel_type.capitalize()}: {count}")


def main():
    """Função principal"""
    from datetime import datetime
    
    print("=" * 70)
    print("🎥 YouTube Subscriptions Collector")
    print("=" * 70)
    
    # Autenticar
    youtube = get_authenticated_service()
    
    # Buscar inscrições
    subscriptions = get_my_subscriptions(youtube)
    
    if not subscriptions:
        print("⚠️  Nenhuma inscrição encontrada")
        return
    
    # Carregar metadados
    metadata = load_channel_metadata()
    
    # Enriquecer com metadados
    subscriptions = enrich_with_metadata(subscriptions, metadata)
    
    # Salvar
    save_subscriptions(subscriptions)
    
    print("\n✨ Coleta concluída com sucesso!")
    print("\nℹ️  Próximo passo: Execute collect_videos.py para buscar vídeos recentes")


if __name__ == '__main__':
    main()
