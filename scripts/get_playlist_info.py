#!/usr/bin/env python3
"""
Script para obter informações de uma playlist específica do YouTube
"""

import os
import sys
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

def get_playlist_info(api_key, playlist_id):
    """
    Obtém informações detalhadas de uma playlist específica
    
    Args:
        api_key: Chave da API do YouTube
        playlist_id: ID da playlist
        
    Returns:
        Informações da playlist incluindo Channel ID
    """
    try:
        youtube = build('youtube', 'v3', developerKey=api_key)
        
        print("=" * 80)
        print(f"OBTENDO INFORMAÇÕES DA PLAYLIST: {playlist_id}")
        print("=" * 80)
        print()
        
        # Buscar informações da playlist
        request = youtube.playlists().list(
            part='snippet,contentDetails',
            id=playlist_id
        )
        
        response = request.execute()
        
        if 'items' in response and len(response['items']) > 0:
            playlist = response['items'][0]
            
            playlist_info = {
                'id': playlist['id'],
                'title': playlist['snippet']['title'],
                'description': playlist['snippet']['description'],
                'channel_id': playlist['snippet']['channelId'],
                'channel_title': playlist['snippet']['channelTitle'],
                'published_at': playlist['snippet']['publishedAt'],
                'item_count': playlist['contentDetails']['itemCount']
            }
            
            print("✅ INFORMAÇÕES DA PLAYLIST:")
            print()
            print(f"📋 Título: {playlist_info['title']}")
            print(f"🆔 Playlist ID: {playlist_info['id']}")
            print(f"📺 Canal: {playlist_info['channel_title']}")
            print(f"🔑 Channel ID: {playlist_info['channel_id']}")
            print(f"📊 Número de vídeos: {playlist_info['item_count']}")
            print(f"📅 Publicada em: {playlist_info['published_at'][:10]}")
            print(f"📝 Descrição: {playlist_info['description'][:200]}{'...' if len(playlist_info['description']) > 200 else ''}")
            print()
            print("=" * 80)
            
            return playlist_info
        else:
            print("❌ Playlist não encontrada ou não é pública.")
            return None
            
    except HttpError as e:
        print(f"❌ Erro HTTP ao buscar playlist:")
        print(f"   Status: {e.resp.status}")
        print(f"   Detalhes: {e.error_details}")
        return None
    except Exception as e:
        print(f"❌ Erro inesperado: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return None


def main():
    """Função principal"""
    
    # Obter API Key do ambiente
    api_key = os.getenv('YOUTUBE_API_KEY')
    
    if not api_key:
        print("❌ ERRO: YOUTUBE_API_KEY não encontrada no arquivo .env")
        sys.exit(1)
    
    # ID da playlist wip-persival
    playlist_id = "PLr7GXSx8GpB6ZeQ2uqQT4GMAGXYZzyu5a"
    
    print("🔑 API Key carregada com sucesso!")
    print()
    
    playlist_info = get_playlist_info(api_key, playlist_id)
    
    if playlist_info:
        print("\n💡 PRÓXIMOS PASSOS:")
        print(f"   Use o Channel ID '{playlist_info['channel_id']}' para listar todas as playlists deste canal.")
        print(f"   Execute: python list_youtube_playlists.py")
        print(f"   Escolha a opção 2 e forneça o Channel ID: {playlist_info['channel_id']}")


if __name__ == '__main__':
    main()
