#!/usr/bin/env python3
"""
Script para listar playlists do YouTube usando a API do YouTube Data v3
"""

import os
import sys
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

def get_my_playlists(api_key):
    """
    Lista todas as playlists do canal autenticado
    
    Args:
        api_key: Chave da API do YouTube
        
    Returns:
        Lista de playlists com informações básicas
    """
    try:
        # Criar cliente da API do YouTube
        youtube = build('youtube', 'v3', developerKey=api_key)
        
        # Buscar playlists
        # Nota: Para listar suas próprias playlists, você precisa de OAuth2
        # Com apenas API Key, podemos buscar playlists de um canal específico
        
        print("=" * 80)
        print("LISTANDO PLAYLISTS DO YOUTUBE")
        print("=" * 80)
        print()
        
        # Primeiro, vamos buscar playlists públicas populares como exemplo
        # Se você quiser suas próprias playlists, precisará usar OAuth2
        
        request = youtube.playlists().list(
            part='snippet,contentDetails',
            mine=False,  # Não pode usar mine=True com apenas API Key
            maxResults=50
        )
        
        # Esta chamada falhará porque precisa de OAuth2 para 'mine=True'
        # Vamos fazer uma busca de playlists públicas em vez disso
        
    except HttpError as e:
        if 'mine' in str(e):
            print("⚠️  Para listar SUAS playlists, é necessário autenticação OAuth2.")
            print("   Com apenas API Key, posso buscar playlists públicas de canais específicos.")
            print()
            print("Opções:")
            print("1. Forneça um Channel ID para listar playlists de um canal específico")
            print("2. Configure OAuth2 para acessar suas próprias playlists")
            return None
        else:
            print(f"❌ Erro ao acessar a API do YouTube: {e}")
            return None
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return None


def search_playlists(api_key, query="", max_results=25):
    """
    Busca playlists públicas no YouTube
    
    Args:
        api_key: Chave da API do YouTube
        query: Termo de busca (opcional)
        max_results: Número máximo de resultados
        
    Returns:
        Lista de playlists encontradas
    """
    try:
        youtube = build('youtube', 'v3', developerKey=api_key)
        
        print("=" * 80)
        print(f"BUSCANDO PLAYLISTS PÚBLICAS{' - ' + query if query else ''}")
        print("=" * 80)
        print()
        
        # Se não houver query, usar um termo padrão
        search_query = query if query else "playlist"
        
        # Para busca exata, colocar entre aspas
        if query and ' ' not in query and '-' in query:
            # Se tem hífen e não tem espaço, provavelmente quer busca exata
            search_query = f'"{query}"'
        
        request = youtube.search().list(
            part='snippet',
            type='playlist',
            q=search_query,
            maxResults=max_results
        )
        
        response = request.execute()
        
        print(f"🔍 Debug - Response keys: {response.keys()}")
        print(f"🔍 Debug - Total results: {response.get('pageInfo', {}).get('totalResults', 0)}")
        print()
        
        playlists = []
        if 'items' in response and len(response['items']) > 0:
            print(f"✅ Encontradas {len(response['items'])} playlists:\n")
            
            for idx, item in enumerate(response['items'], 1):
                playlist_info = {
                    'id': item['id']['playlistId'],
                    'title': item['snippet']['title'],
                    'description': item['snippet']['description'][:100] + '...' if len(item['snippet']['description']) > 100 else item['snippet']['description'],
                    'channel': item['snippet']['channelTitle'],
                    'published': item['snippet']['publishedAt']
                }
                playlists.append(playlist_info)
                
                print(f"{idx}. 📋 {playlist_info['title']}")
                print(f"   Canal: {playlist_info['channel']}")
                print(f"   ID: {playlist_info['id']}")
                print(f"   Descrição: {playlist_info['description']}")
                print(f"   Publicada em: {playlist_info['published'][:10]}")
                print()
            
            return playlists
        else:
            print("⚠️  Nenhuma playlist encontrada.")
            print(f"    Possíveis razões:")
            print(f"    - A API Key pode estar com quota esgotada")
            print(f"    - A API Key pode não ter permissões corretas")
            print(f"    - Termo de busca muito específico")
            return []
            
    except HttpError as e:
        print(f"❌ Erro HTTP ao buscar playlists:")
        print(f"   Status: {e.resp.status}")
        print(f"   Razão: {e.error_details}")
        return None
    except Exception as e:
        print(f"❌ Erro inesperado: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return None


def get_channel_playlists(api_key, channel_id, max_results=50):
    """
    Lista playlists de um canal específico
    
    Args:
        api_key: Chave da API do YouTube
        channel_id: ID do canal
        max_results: Número máximo de resultados
        
    Returns:
        Lista de playlists do canal
    """
    try:
        youtube = build('youtube', 'v3', developerKey=api_key)
        
        print("=" * 80)
        print(f"LISTANDO PLAYLISTS DO CANAL: {channel_id}")
        print("=" * 80)
        print()
        
        request = youtube.playlists().list(
            part='snippet,contentDetails',
            channelId=channel_id,
            maxResults=max_results
        )
        
        response = request.execute()
        
        playlists = []
        if 'items' in response:
            print(f"✅ Encontradas {len(response['items'])} playlists:\n")
            
            for idx, item in enumerate(response['items'], 1):
                playlist_info = {
                    'id': item['id'],
                    'title': item['snippet']['title'],
                    'description': item['snippet']['description'][:100] + '...' if len(item['snippet']['description']) > 100 else item['snippet']['description'],
                    'item_count': item['contentDetails']['itemCount'],
                    'published': item['snippet']['publishedAt']
                }
                playlists.append(playlist_info)
                
                print(f"{idx}. 📋 {playlist_info['title']}")
                print(f"   ID: {playlist_info['id']}")
                print(f"   Vídeos: {playlist_info['item_count']}")
                print(f"   Descrição: {playlist_info['description']}")
                print(f"   Publicada em: {playlist_info['published'][:10]}")
                print()
            
            print(f"\n📊 Total: {len(playlists)} playlists")
            return playlists
        else:
            print("⚠️  Nenhuma playlist encontrada para este canal.")
            return []
            
    except HttpError as e:
        print(f"❌ Erro ao buscar playlists do canal: {e}")
        return None
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return None


def main():
    """Função principal"""
    
    # Obter API Key do ambiente
    api_key = os.getenv('YOUTUBE_API_KEY')
    
    if not api_key:
        print("❌ ERRO: YOUTUBE_API_KEY não encontrada no arquivo .env")
        sys.exit(1)
    
    print("🔑 API Key carregada com sucesso!")
    print()
    
    # Menu de opções
    print("Escolha uma opção:")
    print("1. Buscar playlists públicas (por termo de busca)")
    print("2. Listar playlists de um canal específico (por Channel ID)")
    print()
    
    choice = input("Digite sua escolha (1 ou 2): ").strip()
    
    if choice == '1':
        query = input("\nDigite o termo de busca (ou Enter para buscar todas): ").strip()
        search_playlists(api_key, query=query)
    elif choice == '2':
        channel_id = input("\nDigite o Channel ID: ").strip()
        if channel_id:
            get_channel_playlists(api_key, channel_id)
        else:
            print("❌ Channel ID não pode estar vazio.")
    else:
        print("❌ Opção inválida.")
        sys.exit(1)


if __name__ == '__main__':
    main()
