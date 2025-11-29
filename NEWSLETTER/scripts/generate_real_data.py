#!/usr/bin/env python3
"""
Gera o arquivo real-data.ts a partir da edição mais recente
Este arquivo é usado pela UI para exibir os dados

Uso:
    python generate_real_data.py                    # Usa edição mais recente
    python generate_real_data.py --edition 2025-11-29  # Usa edição específica
"""

import json
import argparse
from pathlib import Path
from datetime import datetime

# Diretórios
SCRIPT_DIR = Path(__file__).parent
PROJECT_DIR = SCRIPT_DIR.parent
EDITIONS_DIR = PROJECT_DIR / 'ui' / 'public' / 'editions'
OUTPUT_FILE = PROJECT_DIR / 'ui' / 'lib' / 'real-data.ts'


# Mapeamento de categorias para metadados
CATEGORY_META = {
    'novos-modelos': {'emoji': '🚀', 'name': 'Novos Modelos', 'description': 'Lançamentos e atualizações de modelos de IA'},
    'agentes-ia': {'emoji': '🤖', 'name': 'Agentes de IA', 'description': 'Agentes autônomos e sistemas multi-agente'},
    'ferramentas-dev': {'emoji': '💻', 'name': 'Ferramentas para Devs', 'description': 'IDEs, copilots e ferramentas de desenvolvimento'},
    'tutoriais': {'emoji': '📚', 'name': 'Tutoriais', 'description': 'Guias e tutoriais práticos'},
    'noticias': {'emoji': '📰', 'name': 'Notícias', 'description': 'Notícias e atualizações do mundo da IA'},
    'pesquisa': {'emoji': '🔬', 'name': 'Pesquisa', 'description': 'Papers e pesquisas acadêmicas'},
    'automacao': {'emoji': '⚙️', 'name': 'Automação', 'description': 'Workflows e automação com IA'},
    'produtividade': {'emoji': '📈', 'name': 'Produtividade', 'description': 'Dicas e ferramentas de produtividade'},
    'negocios': {'emoji': '💼', 'name': 'Negócios & Startups', 'description': 'IA para negócios e empreendedorismo'},
    'hardware': {'emoji': '🖥️', 'name': 'Hardware & Infra', 'description': 'GPUs, chips e infraestrutura'},
    'outros': {'emoji': '📌', 'name': 'Outros', 'description': 'Outros tópicos relevantes'},
}


def format_views(count: int) -> str:
    """Formata contagem de views para exibição"""
    if count >= 1_000_000:
        return f"{count / 1_000_000:.1f}M"
    elif count >= 1_000:
        return f"{count / 1_000:.1f}K"
    return str(count)


def load_edition(edition_date: str = None) -> dict:
    """Carrega uma edição específica ou a mais recente"""
    if edition_date:
        edition_path = EDITIONS_DIR / f"{edition_date}.json"
    else:
        # Carregar índice e pegar a mais recente
        index_path = EDITIONS_DIR / 'index.json'
        with open(index_path, 'r', encoding='utf-8') as f:
            index = json.load(f)
        edition_date = index['latest']
        edition_path = EDITIONS_DIR / f"{edition_date}.json"
    
    with open(edition_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def generate_typescript(edition: dict) -> str:
    """Gera o conteúdo TypeScript"""
    
    # Header
    ts_content = f'''/**
 * Dados reais dos {edition['totalVideos']} vídeos coletados e categorizados
 * Gerado automaticamente em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
 * Edição: {edition['date']}
 * Fonte: ui/public/editions/{edition['date']}.json
 */

import {{ Edition, Category, Video }} from "./types";
import {{ CATEGORY_META }} from "./types";

// Vídeos por categoria

'''
    
    # Gerar arrays de vídeos por categoria
    category_vars = []
    
    for category in edition['categories']:
        cat_id = category['id']
        var_name = cat_id.upper().replace('-', '_') + '_VIDEOS'
        category_vars.append((cat_id, var_name, category))
        
        ts_content += f"const {var_name}: Video[] = [\n"
        
        for video in category['videos']:
            views_formatted = format_views(video.get('viewCount', 0))
            
            # Escapar strings
            title = video.get('title', '').replace('"', '\\"').replace('\n', ' ')
            channel = video.get('channel', '').replace('"', '\\"')
            summary = video.get('summary', '').replace('"', '\\"').replace('\n', ' ')
            
            # Key points
            key_points = video.get('keyPoints', [])
            key_points_str = json.dumps(key_points, ensure_ascii=False)
            
            ts_content += f'''  {{
    video_id: "{video.get('video_id', '')}",
    title: "{title}",
    channel: "{channel}",
    duration: "{video.get('duration', '0')}",
    views: "{views_formatted}",
    viewCount: {video.get('viewCount', 0)},
    summary: "{summary}",
    keyPoints: {key_points_str},
    url: "{video.get('url', '')}",
    publishedAt: "{video.get('publishedAt', '')}",
    likeCount: {video.get('likeCount', 0)},
    commentCount: {video.get('commentCount', 0)},
  }},
'''
        
        ts_content += "];\n\n"
    
    # Gerar categorias
    ts_content += "// Categorias com metadados\n\n"
    
    for cat_id, var_name, category in category_vars:
        meta = CATEGORY_META.get(cat_id, {'emoji': '📌', 'name': category['name'], 'description': ''})
        
        ts_content += f'''const {cat_id.upper().replace('-', '_')}_CATEGORY: Category = {{
  id: "{cat_id}",
  name: "{meta['name']}",
  emoji: "{meta['emoji']}",
  description: "{meta['description']}",
  videoCount: {category['videoCount']},
  videos: {var_name},
}};

'''
    
    # Gerar REAL_EDITION
    category_refs = [f"  {cat_id.upper().replace('-', '_')}_CATEGORY," for cat_id, _, _ in category_vars]
    
    ts_content += f'''// Edição completa
export const REAL_EDITION: Edition = {{
  date: "{edition['date']}",
  title: "{edition['title']}",
  generatedAt: "{edition['generatedAt']}",
  collectedAt: "{edition['collectedAt']}",
  totalVideos: {edition['totalVideos']},
  categories: [
{chr(10).join(category_refs)}
  ],
}};

// Helper para obter todos os vídeos
export function getAllRealVideos(): Video[] {{
  return REAL_EDITION.categories.flatMap(c => c.videos);
}}
'''
    
    return ts_content


def main():
    parser = argparse.ArgumentParser(description='Gera real-data.ts a partir da edição')
    parser.add_argument('--edition', type=str, help='Data da edição (YYYY-MM-DD). Padrão: mais recente')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("📰 Gerador de real-data.ts - IANIA AI News")
    print("=" * 60)
    
    # Carregar edição
    edition = load_edition(args.edition)
    print(f"\n📅 Edição: {edition['date']}")
    print(f"🎬 Vídeos: {edition['totalVideos']}")
    print(f"📑 Categorias: {len(edition['categories'])}")
    
    # Gerar TypeScript
    print("\n🔄 Gerando TypeScript...")
    ts_content = generate_typescript(edition)
    
    # Salvar
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(ts_content)
    
    print(f"💾 Salvo em: {OUTPUT_FILE}")
    print(f"📄 Tamanho: {len(ts_content):,} caracteres")
    
    print("\n✅ Concluído! Reinicie o servidor Next.js para ver as mudanças.")


if __name__ == '__main__':
    main()
