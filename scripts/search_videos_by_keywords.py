#!/usr/bin/env python3
"""
Script para buscar vídeos em playlists por palavras-chave na descrição
"""

import os
import json
import re
from pathlib import Path


def load_playlist_data(playlist_file):
    """
    Carrega dados de um arquivo JSON de playlist
    
    Args:
        playlist_file: Caminho para o arquivo JSON
        
    Returns:
        Dados da playlist ou None se houver erro
    """
    try:
        with open(playlist_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Erro ao carregar {playlist_file}: {e}")
        return None


def search_videos_by_keywords(videos, keyword_groups, case_sensitive=False):
    """
    Busca vídeos que contenham grupos de palavras-chave na descrição
    
    Args:
        videos: Lista de vídeos
        keyword_groups: Lista de tuplas com palavras-chave que devem aparecer juntas
                       Ex: [("RAG", "text"), ("RAG", "SQL")]
        case_sensitive: Se a busca deve ser case-sensitive
        
    Returns:
        Lista de vídeos que correspondem aos critérios
    """
    matching_videos = []
    
    for video in videos:
        description = video.get('description', '')
        title = video.get('title', '')
        
        if not case_sensitive:
            description_lower = description.lower()
            title_lower = title.lower()
        else:
            description_lower = description
            title_lower = title
        
        # Verificar se algum grupo de palavras-chave está presente
        for keyword_group in keyword_groups:
            # Verificar se todas as palavras do grupo estão presentes
            if case_sensitive:
                keywords_present = all(keyword in description or keyword in title 
                                     for keyword in keyword_group)
            else:
                keywords_present = all(keyword.lower() in description_lower or 
                                     keyword.lower() in title_lower 
                                     for keyword in keyword_group)
            
            if keywords_present:
                # Adicionar informação sobre qual grupo de keywords foi encontrado
                video_copy = video.copy()
                video_copy['matched_keywords'] = keyword_group
                matching_videos.append(video_copy)
                break  # Não precisa verificar outros grupos para este vídeo
    
    return matching_videos


def search_in_all_playlists(playlists_dir, keyword_groups, case_sensitive=False):
    """
    Busca vídeos em todas as playlists de um diretório
    
    Args:
        playlists_dir: Diretório contendo os arquivos JSON das playlists
        keyword_groups: Lista de tuplas com palavras-chave
        case_sensitive: Se a busca deve ser case-sensitive
        
    Returns:
        Dicionário com resultados por playlist
    """
    playlists_dir = Path(playlists_dir)
    results = {}
    
    # Listar todos os arquivos JSON no diretório
    json_files = list(playlists_dir.glob('*.json'))
    
    if not json_files:
        print(f"⚠️  Nenhum arquivo JSON encontrado em {playlists_dir}")
        return results
    
    print(f"🔍 Buscando em {len(json_files)} playlists...")
    print()
    
    for json_file in json_files:
        playlist_data = load_playlist_data(json_file)
        
        if not playlist_data:
            continue
        
        playlist_name = playlist_data.get('playlist_info', {}).get('title', json_file.stem)
        videos = playlist_data.get('videos', [])
        
        if not videos:
            continue
        
        # Buscar vídeos correspondentes
        matching_videos = search_videos_by_keywords(videos, keyword_groups, case_sensitive)
        
        if matching_videos:
            results[playlist_name] = {
                'playlist_file': str(json_file),
                'playlist_info': playlist_data.get('playlist_info', {}),
                'matching_videos': matching_videos,
                'total_matches': len(matching_videos)
            }
    
    return results


def display_results(results, show_descriptions=False):
    """
    Exibe os resultados da busca no terminal
    
    Args:
        results: Dicionário com resultados por playlist
        show_descriptions: Se deve mostrar as descrições dos vídeos
    """
    if not results:
        print("❌ Nenhum vídeo encontrado com os critérios especificados.")
        return
    
    total_videos = sum(r['total_matches'] for r in results.values())
    
    print("=" * 80)
    print("📊 RESULTADOS DA BUSCA")
    print("=" * 80)
    print(f"✅ Encontrados {total_videos} vídeos em {len(results)} playlist(s)")
    print()
    
    for playlist_name, data in results.items():
        print("=" * 80)
        print(f"📋 PLAYLIST: {playlist_name}")
        print(f"🔗 URL: {data['playlist_info'].get('playlist_url', 'N/A')}")
        print(f"📊 Vídeos encontrados: {data['total_matches']}")
        print("=" * 80)
        print()
        
        for idx, video in enumerate(data['matching_videos'], 1):
            print(f"{idx}. 🎥 {video['title']}")
            print(f"   🔗 {video['video_url']}")
            print(f"   🔑 Palavras-chave encontradas: {', '.join(video['matched_keywords'])}")
            print(f"   📅 Publicado em: {video['published_at'][:10]}")
            
            if show_descriptions:
                description = video['description'][:200]
                if len(video['description']) > 200:
                    description += "..."
                print(f"   📝 Descrição: {description}")
            
            print()
    
    print("=" * 80)
    print(f"📊 RESUMO: {total_videos} vídeos encontrados em {len(results)} playlist(s)")
    print("=" * 80)


def main():
    """Função principal"""
    
    # Configurações de busca
    playlists_dir = 'playlists'
    
    # Grupos de palavras-chave (todas as palavras do grupo devem estar presentes)
    keyword_groups = [
        ("RAG", "text"),   # RAG + text em qualquer ordem
        ("RAG", "SQL")     # RAG + SQL em qualquer ordem
    ]
    
    print("=" * 80)
    print("🔍 BUSCA DE VÍDEOS POR PALAVRAS-CHAVE")
    print("=" * 80)
    print()
    print("📋 Critérios de busca:")
    print("   - (RAG + text) OU")
    print("   - (RAG + SQL)")
    print()
    print("=" * 80)
    print()
    
    # Buscar em todas as playlists
    results = search_in_all_playlists(playlists_dir, keyword_groups, case_sensitive=False)
    
    # Exibir resultados
    display_results(results, show_descriptions=False)


if __name__ == '__main__':
    main()
