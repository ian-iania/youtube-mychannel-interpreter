#!/usr/bin/env python3
"""
Script para exportar resultados de busca de vídeos para Markdown
"""

import os
import json
from pathlib import Path
from datetime import datetime


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


def export_to_markdown(results, output_file='RAG.md', keyword_groups=None):
    """
    Exporta resultados para um arquivo Markdown
    
    Args:
        results: Dicionário com resultados por playlist
        output_file: Nome do arquivo de saída
        keyword_groups: Lista de grupos de palavras-chave usados na busca
    """
    total_videos = sum(r['total_matches'] for r in results.values())
    
    with open(output_file, 'w', encoding='utf-8') as f:
        # Cabeçalho
        f.write("# 🎥 Vídeos sobre RAG (Retrieval-Augmented Generation)\n\n")
        f.write(f"**Data de exportação:** {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n")
        
        # Critérios de busca
        if keyword_groups:
            f.write("## 🔍 Critérios de Busca\n\n")
            f.write("Vídeos que contêm:\n")
            for idx, group in enumerate(keyword_groups, 1):
                if idx > 1:
                    f.write("**OU**\n")
                f.write(f"- {' + '.join(group)}\n")
            f.write("\n")
        
        # Resumo
        f.write("## 📊 Resumo\n\n")
        f.write(f"- **Total de vídeos encontrados:** {total_videos}\n")
        f.write(f"- **Playlists com resultados:** {len(results)}\n\n")
        
        # Tabela de conteúdo
        f.write("## 📑 Índice por Playlist\n\n")
        for idx, (playlist_name, data) in enumerate(results.items(), 1):
            # Criar âncora segura (remover caracteres especiais)
            anchor = playlist_name.lower().replace(' ', '-').replace('/', '').replace('_', '-')
            f.write(f"{idx}. [{playlist_name}](#{anchor}) ({data['total_matches']} vídeos)\n")
        f.write("\n---\n\n")
        
        # Vídeos por playlist
        for playlist_name, data in results.items():
            # Criar âncora segura
            anchor = playlist_name.lower().replace(' ', '-').replace('/', '').replace('_', '-')
            
            f.write(f"## 📋 {playlist_name}\n\n")
            f.write(f"**Playlist URL:** [{data['playlist_info'].get('playlist_url', 'N/A')}]({data['playlist_info'].get('playlist_url', '#')})\n\n")
            f.write(f"**Total de vídeos encontrados:** {data['total_matches']}\n\n")
            
            # Lista de vídeos
            for idx, video in enumerate(data['matching_videos'], 1):
                f.write(f"### {idx}. {video['title']}\n\n")
                
                # Informações do vídeo em uma tabela
                f.write("| Campo | Informação |\n")
                f.write("|-------|------------|\n")
                f.write(f"| 🔗 **URL** | [{video['video_url']}]({video['video_url']}) |\n")
                f.write(f"| 🔑 **Keywords** | {', '.join(video['matched_keywords'])} |\n")
                f.write(f"| 📅 **Publicado em** | {video['published_at'][:10]} |\n")
                f.write(f"| 📺 **Canal** | {video['channel_title']} |\n")
                f.write(f"| 🆔 **Video ID** | `{video['video_id']}` |\n")
                
                # Descrição (primeiras 300 caracteres)
                description = video['description']
                if description:
                    description_preview = description[:300]
                    if len(description) > 300:
                        description_preview += "..."
                    f.write(f"\n**📝 Descrição:**\n\n")
                    f.write(f"> {description_preview}\n\n")
                else:
                    f.write(f"\n**📝 Descrição:** _Não disponível_\n\n")
                
                # Thumbnail
                if video.get('thumbnail_url'):
                    f.write(f"**🖼️ Thumbnail:**\n\n")
                    f.write(f"![Thumbnail]({video['thumbnail_url']})\n\n")
                
                f.write("---\n\n")
            
            f.write("\n")
        
        # Rodapé
        f.write("---\n\n")
        f.write("## 📌 Notas\n\n")
        f.write("- Este documento foi gerado automaticamente a partir das playlists públicas do YouTube.\n")
        f.write("- Os vídeos estão organizados por playlist e ordenados pela posição original.\n")
        f.write("- As descrições foram truncadas para melhor legibilidade.\n\n")
        f.write(f"**Gerado em:** {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}\n")


def main():
    """Função principal"""
    
    # Configurações de busca
    playlists_dir = 'playlists'
    output_file = 'RAG.md'
    
    # Grupos de palavras-chave
    keyword_groups = [
        ("RAG", "text"),   # RAG + text em qualquer ordem
        ("RAG", "SQL")     # RAG + SQL em qualquer ordem
    ]
    
    print("=" * 80)
    print("📝 EXPORTAÇÃO PARA MARKDOWN")
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
    
    if not results:
        print("❌ Nenhum vídeo encontrado com os critérios especificados.")
        return
    
    total_videos = sum(r['total_matches'] for r in results.values())
    print(f"✅ Encontrados {total_videos} vídeos em {len(results)} playlist(s)")
    print()
    
    # Exportar para Markdown
    print(f"📝 Exportando para {output_file}...")
    export_to_markdown(results, output_file, keyword_groups)
    
    print(f"✅ Arquivo criado com sucesso: {output_file}")
    print()
    print("=" * 80)
    print("📊 RESUMO DA EXPORTAÇÃO")
    print("=" * 80)
    print(f"📹 Total de vídeos exportados: {total_videos}")
    print(f"📋 Playlists com resultados: {len(results)}")
    print(f"📄 Arquivo gerado: {output_file}")
    print("=" * 80)


if __name__ == '__main__':
    main()
