#!/usr/bin/env python3
"""
Script para salvar uma nova edição da newsletter
Converte os dados do pipeline para o formato de edição e atualiza o índice

Uso:
    python save_edition.py                    # Usa a data de hoje
    python save_edition.py --date 2025-11-29  # Usa data específica
    python save_edition.py --input newsletters/2025-11-27_videos_categorized.json
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime


# Diretórios
SCRIPT_DIR = Path(__file__).parent
PROJECT_DIR = SCRIPT_DIR.parent
NEWSLETTERS_DIR = PROJECT_DIR / 'newsletters'
EDITIONS_DIR = PROJECT_DIR / 'ui' / 'public' / 'editions'


def load_categorized_videos(input_file: str = None, date: str = None) -> dict:
    """
    Carrega os vídeos categorizados do pipeline
    """
    if input_file:
        file_path = Path(input_file)
        if not file_path.is_absolute():
            file_path = PROJECT_DIR / input_file
    elif date:
        file_path = NEWSLETTERS_DIR / f"{date}_videos_categorized.json"
    else:
        # Buscar arquivo mais recente
        categorized_files = list(NEWSLETTERS_DIR.glob('*_videos_categorized.json'))
        if not categorized_files:
            raise FileNotFoundError("Nenhum arquivo de vídeos categorizados encontrado")
        file_path = max(categorized_files, key=lambda f: f.stat().st_mtime)
    
    print(f"📂 Carregando: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def convert_to_edition_format(data: dict, edition_date: str) -> dict:
    """
    Converte dados do pipeline para formato de edição
    """
    categories = []
    
    # Mapeamento de IDs para nomes amigáveis
    category_names = {
        'novos-modelos': 'Novos Modelos',
        'agentes-ia': 'Agentes de IA',
        'ferramentas-dev': 'Ferramentas para Devs',
        'tutoriais': 'Tutoriais',
        'noticias': 'Notícias',
        'pesquisa': 'Pesquisa',
        'automacao': 'Automação',
        'produtividade': 'Produtividade',
        'negocios': 'Negócios & Startups',
        'hardware': 'Hardware & Infraestrutura',
        'outros': 'Outros'
    }
    
    for cat_id, videos in data.get('categories', {}).items():
        edition_videos = []
        
        for video in videos:
            edition_video = {
                'video_id': video.get('video_id', ''),
                'title': video.get('title', ''),
                'channel': video.get('channel', ''),
                'duration': str(video.get('duration_minutes', 0)),
                'viewCount': int(video.get('view_count', 0)),
                'summary': video.get('summary', ''),
                'keyPoints': video.get('key_points', []),
                'url': f"https://www.youtube.com/watch?v={video.get('video_id', '')}",
                'publishedAt': video.get('published_at', ''),
                'likeCount': int(video.get('like_count', 0)),
                'commentCount': int(video.get('comment_count', 0)),
                'thumbnail': video.get('thumbnail', '')
            }
            edition_videos.append(edition_video)
        
        category = {
            'id': cat_id,
            'name': category_names.get(cat_id, cat_id.replace('-', ' ').title()),
            'videoCount': len(edition_videos),
            'videos': edition_videos
        }
        categories.append(category)
    
    # Ordenar categorias por número de vídeos (decrescente)
    categories.sort(key=lambda c: c['videoCount'], reverse=True)
    
    # Calcular total de vídeos
    total_videos = sum(c['videoCount'] for c in categories)
    
    # Formatar data para título
    parts = edition_date.split('-')
    title = f"Edição {parts[2]}/{parts[1]}/{parts[0]}"
    
    edition = {
        'date': edition_date,
        'title': title,
        'generatedAt': data.get('categorized_at', datetime.now().isoformat()),
        'collectedAt': data.get('collected_at', datetime.now().isoformat()),
        'totalVideos': total_videos,
        'categories': categories
    }
    
    return edition


def load_editions_index() -> dict:
    """
    Carrega o índice de edições existente
    """
    index_path = EDITIONS_DIR / 'index.json'
    
    if index_path.exists():
        with open(index_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    return {'latest': None, 'editions': []}


def update_editions_index(index: dict, edition: dict) -> dict:
    """
    Atualiza o índice com a nova edição
    """
    edition_date = edition['date']
    
    edition_summary = {
        'date': edition_date,
        'title': edition['title'],
        'videoCount': edition['totalVideos'],
        'categoryCount': len(edition['categories']),
        'generatedAt': edition['generatedAt']
    }
    
    existing_dates = [e['date'] for e in index['editions']]
    
    if edition_date in existing_dates:
        for i, e in enumerate(index['editions']):
            if e['date'] == edition_date:
                index['editions'][i] = edition_summary
                print(f"📝 Edição {edition_date} atualizada")
                break
    else:
        index['editions'].append(edition_summary)
        print(f"✨ Nova edição {edition_date} adicionada")
    
    # Ordenar por data (mais recente primeiro)
    index['editions'].sort(key=lambda e: e['date'], reverse=True)
    
    if index['editions']:
        index['latest'] = index['editions'][0]['date']
    
    return index


def save_edition(edition: dict, index: dict):
    """
    Salva a edição e o índice atualizado
    """
    EDITIONS_DIR.mkdir(parents=True, exist_ok=True)
    
    edition_path = EDITIONS_DIR / f"{edition['date']}.json"
    with open(edition_path, 'w', encoding='utf-8') as f:
        json.dump(edition, f, ensure_ascii=False, indent=2)
    print(f"💾 Edição salva: {edition_path}")
    
    index_path = EDITIONS_DIR / 'index.json'
    with open(index_path, 'w', encoding='utf-8') as f:
        json.dump(index, f, ensure_ascii=False, indent=2)
    print(f"📋 Índice atualizado: {index_path}")


def main():
    parser = argparse.ArgumentParser(description='Salva uma nova edição da newsletter')
    parser.add_argument('--date', type=str, help='Data da edição (YYYY-MM-DD). Padrão: hoje')
    parser.add_argument('--input', type=str, help='Arquivo de entrada (videos_categorized.json)')
    parser.add_argument('--dry-run', action='store_true', help='Simular sem salvar')
    
    args = parser.parse_args()
    
    edition_date = args.date or datetime.now().strftime('%Y-%m-%d')
    
    print("=" * 60)
    print("📰 Gerador de Edições - IANIA AI News")
    print("=" * 60)
    print(f"\n📅 Data da edição: {edition_date}")
    
    try:
        # 1. Carregar dados categorizados
        data = load_categorized_videos(args.input, args.date)
        print(f"   ✅ {data.get('total_videos', 0)} vídeos carregados")
        print(f"   ✅ {len(data.get('categories', {}))} categorias")
        
        # 2. Converter para formato de edição
        print("\n🔄 Convertendo para formato de edição...")
        edition = convert_to_edition_format(data, edition_date)
        print(f"   ✅ {edition['totalVideos']} vídeos")
        print(f"   ✅ {len(edition['categories'])} categorias")
        
        # 3. Carregar e atualizar índice
        print("\n📋 Atualizando índice de edições...")
        index = load_editions_index()
        index = update_editions_index(index, edition)
        
        # 4. Salvar
        if args.dry_run:
            print("\n🔍 [DRY RUN] Nenhum arquivo foi salvo")
        else:
            print("\n💾 Salvando arquivos...")
            save_edition(edition, index)
        
        # 5. Mostrar estatísticas
        print("\n" + "=" * 60)
        print("📊 Estatísticas do Índice")
        print("=" * 60)
        print(f"\n📰 Total de edições: {len(index['editions'])}")
        print(f"🆕 Edição mais recente: {index['latest']}")
        
        print("\n📅 Histórico de edições:")
        for e in index['editions'][:5]:
            print(f"   • {e['date']}: {e['videoCount']} vídeos, {e['categoryCount']} categorias")
        
        print("\n✅ Concluído!")
        
    except FileNotFoundError as e:
        print(f"\n❌ Erro: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
