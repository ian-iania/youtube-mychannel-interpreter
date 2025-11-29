#!/usr/bin/env python3
"""
Categoriza vídeos por tema e gera JSON para o sistema de edições

Uso:
    python categorize_videos.py --input 2025-11-29_videos.json --output 2025-11-29_videos_categorized.json
"""

import os
import sys
import json
import re
import argparse
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# Diretórios
SCRIPT_DIR = Path(__file__).parent
PROJECT_DIR = SCRIPT_DIR.parent
NEWSLETTERS_DIR = PROJECT_DIR / 'newsletters'


# Mapeamento de categorias
CATEGORY_MAPPING = {
    'novos-modelos': {
        'name': 'Novos Modelos',
        'keywords': ['gpt', 'claude', 'gemini', 'llama', 'mistral', 'opus', 'sonnet', 'model', 'release', 'launch', 'benchmark', 'arena']
    },
    'agentes-ia': {
        'name': 'Agentes de IA',
        'keywords': ['agent', 'agente', 'autonomous', 'autônomo', 'mcp', 'tool use', 'function call']
    },
    'ferramentas-dev': {
        'name': 'Ferramentas para Devs',
        'keywords': ['cursor', 'copilot', 'windsurf', 'cline', 'vscode', 'ide', 'coding', 'code', 'developer', 'dev tool']
    },
    'tutoriais': {
        'name': 'Tutoriais',
        'keywords': ['tutorial', 'how to', 'como', 'guide', 'guia', 'learn', 'aprenda', 'course', 'curso', 'step by step']
    },
    'noticias': {
        'name': 'Notícias',
        'keywords': ['news', 'notícia', 'announcement', 'anúncio', 'update', 'atualização', 'breaking']
    },
    'pesquisa': {
        'name': 'Pesquisa',
        'keywords': ['research', 'pesquisa', 'paper', 'arxiv', 'study', 'estudo', 'scientific']
    },
    'automacao': {
        'name': 'Automação',
        'keywords': ['automation', 'automação', 'workflow', 'n8n', 'make', 'zapier', 'pipeline']
    },
    'produtividade': {
        'name': 'Produtividade',
        'keywords': ['productivity', 'produtividade', 'efficiency', 'eficiência', 'tips', 'dicas', 'hack']
    },
    'negocios': {
        'name': 'Negócios & Startups',
        'keywords': ['business', 'negócio', 'startup', 'enterprise', 'empresa', 'money', 'revenue', 'saas']
    },
    'hardware': {
        'name': 'Hardware & Infraestrutura',
        'keywords': ['hardware', 'gpu', 'nvidia', 'chip', 'server', 'cloud', 'infrastructure', 'infraestrutura']
    },
    'outros': {
        'name': 'Outros',
        'keywords': []
    }
}


def classify_video(video: dict) -> str:
    """
    Classifica um vídeo em uma categoria baseado no título e descrição
    """
    title = video.get('title', '').lower()
    description = video.get('description', '').lower()
    text = f"{title} {description}"
    
    scores = {}
    
    for cat_id, cat_info in CATEGORY_MAPPING.items():
        if cat_id == 'outros':
            continue
        
        score = 0
        for keyword in cat_info['keywords']:
            if keyword.lower() in text:
                # Peso maior para título
                if keyword.lower() in title:
                    score += 3
                else:
                    score += 1
        
        scores[cat_id] = score
    
    # Retornar categoria com maior score, ou 'outros' se nenhuma
    if scores:
        best_cat = max(scores, key=scores.get)
        if scores[best_cat] > 0:
            return best_cat
    
    return 'outros'


def deduplicate_videos(videos: list) -> list:
    """
    Remove vídeos duplicados por video_id e título similar
    """
    seen_ids = set()
    seen_titles = {}
    unique_videos = []
    
    for video in videos:
        video_id = video.get('video_id', '')
        
        # Verificar duplicata por ID
        if video_id in seen_ids:
            continue
        
        # Verificar duplicata por título similar
        title = video.get('title', '').lower()
        normalized = re.sub(r'[^\w\s]', '', title)
        
        is_duplicate = False
        for seen_title in seen_titles:
            words1 = set(normalized.split())
            words2 = set(seen_title.split())
            
            if len(words1) > 0 and len(words2) > 0:
                similarity = len(words1 & words2) / max(len(words1), len(words2))
                if similarity > 0.7:
                    is_duplicate = True
                    break
        
        if not is_duplicate:
            seen_ids.add(video_id)
            seen_titles[normalized] = video
            unique_videos.append(video)
    
    return unique_videos


def categorize_videos(data: dict) -> dict:
    """
    Categoriza todos os vídeos e retorna estrutura para edição
    """
    categories = defaultdict(list)
    
    for channel_id, channel_data in data.get('channels', {}).items():
        channel_info = channel_data.get('channel_info', {})
        
        # Extrair nome do canal
        if 'snippet' in channel_info:
            channel_name = channel_info['snippet']['title']
        else:
            channel_name = channel_info.get('channel_title', 'Unknown')
        
        for video in channel_data.get('videos', []):
            # Classificar vídeo
            category = classify_video(video)
            
            # Criar estrutura do vídeo para edição
            categorized_video = {
                'video_id': video.get('video_id', ''),
                'title': video.get('title', ''),
                'description': video.get('description', ''),
                'published_at': video.get('published_at', ''),
                'thumbnail': video.get('thumbnail', video.get('thumbnail_url', '')),
                'duration_minutes': video.get('duration_minutes', 0),
                'view_count': int(video.get('view_count', 0)),
                'like_count': int(video.get('like_count', 0)),
                'comment_count': int(video.get('comment_count', 0)),
                'channel': channel_name,
                'category': category
            }
            
            categories[category].append(categorized_video)
    
    # Deduplicar cada categoria
    for cat_id in categories:
        categories[cat_id] = deduplicate_videos(categories[cat_id])
    
    return dict(categories)


def main():
    parser = argparse.ArgumentParser(description='Categoriza vídeos para edição')
    parser.add_argument('--input', type=str, required=True, help='Arquivo de entrada (videos.json)')
    parser.add_argument('--output', type=str, help='Arquivo de saída')
    
    args = parser.parse_args()
    
    # Carregar dados
    input_path = NEWSLETTERS_DIR / args.input
    
    print("=" * 60)
    print("📰 Categorizador de Vídeos - IANIA AI News")
    print("=" * 60)
    print(f"\n📂 Carregando: {input_path}")
    
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Contar vídeos de entrada
    total_input = sum(
        len(ch.get('videos', [])) 
        for ch in data.get('channels', {}).values()
    )
    print(f"   ✅ {total_input} vídeos carregados")
    
    # Categorizar
    print("\n🔄 Categorizando vídeos...")
    categories = categorize_videos(data)
    
    # Calcular estatísticas
    total_output = sum(len(videos) for videos in categories.values())
    
    # Criar estrutura de saída
    output_data = {
        'collected_at': data.get('collected_at', data.get('generated_at', datetime.now().isoformat())),
        'categorized_at': datetime.now().isoformat(),
        'total_videos': total_output,
        'categories': categories
    }
    
    # Salvar
    output_file = args.output or f"{datetime.now().strftime('%Y-%m-%d')}_videos_categorized.json"
    output_path = NEWSLETTERS_DIR / output_file
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Salvo em: {output_path}")
    
    # Estatísticas
    print("\n" + "=" * 60)
    print("📊 Estatísticas")
    print("=" * 60)
    print(f"\n📥 Vídeos de entrada: {total_input}")
    print(f"📤 Vídeos categorizados: {total_output}")
    print(f"🔄 Duplicatas removidas: {total_input - total_output}")
    
    print("\n📋 Distribuição por categoria:")
    for cat_id, videos in sorted(categories.items(), key=lambda x: -len(x[1])):
        cat_name = CATEGORY_MAPPING.get(cat_id, {}).get('name', cat_id)
        print(f"   • {cat_name}: {len(videos)} vídeos")
    
    print("\n✅ Concluído!")


if __name__ == '__main__':
    main()
