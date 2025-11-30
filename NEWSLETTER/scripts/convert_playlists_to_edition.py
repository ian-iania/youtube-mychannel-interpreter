#!/usr/bin/env python3
"""
Converte playlists/*.json para o formato de edição do site (ui/public/editions/)
Permite usar os mesmos dados tanto no app.py quanto no site Next.js

Uso:
    python convert_playlists_to_edition.py                    # Converte todas as playlists
    python convert_playlists_to_edition.py --playlist AI      # Converte apenas AI.json
    python convert_playlists_to_edition.py --generate-ts      # Também gera real-data.ts
"""

import json
import argparse
from pathlib import Path
from datetime import datetime
import subprocess
import sys

# Diretórios
SCRIPT_DIR = Path(__file__).parent
PROJECT_DIR = SCRIPT_DIR.parent
LAB_DIR = PROJECT_DIR.parent  # /Users/.../LAB
PLAYLISTS_DIR = LAB_DIR / 'playlists'
EDITIONS_DIR = PROJECT_DIR / 'ui' / 'public' / 'editions'

# Mapeamento de playlists para categorias
PLAYLIST_TO_CATEGORY = {
    'AI': 'novos-modelos',
    'LABs': 'ferramentas-dev',
    'Estudos': 'tutoriais',
    '__@Fazer_aula': 'tutoriais',
    'Lanchain': 'agentes-ia',
    'PowerBI': 'ferramentas-dev',
    'Gestão': 'negocios',
    'Casa': 'outros',
    'Física': 'pesquisa',
    'Musica': 'outros',
    'Very Pop SYnth Pop': 'outros',
    'OmniJus interno': 'outros',
    'wip-persival': 'outros',
}

# Metadados das categorias
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


def parse_duration(duration_str: str) -> float:
    """Converte duração ISO 8601 (PT1H2M3S) para minutos"""
    if not duration_str:
        return 0.0
    
    import re
    pattern = r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?'
    match = re.match(pattern, duration_str)
    
    if not match:
        return 0.0
    
    hours = int(match.group(1) or 0)
    minutes = int(match.group(2) or 0)
    seconds = int(match.group(3) or 0)
    
    return hours * 60 + minutes + seconds / 60


def convert_video(video: dict, playlist_name: str) -> dict:
    """Converte um vídeo do formato playlist para o formato do site"""
    
    # Extrair view count se disponível
    view_count = video.get('view_count', 0)
    if isinstance(view_count, str):
        view_count = int(view_count.replace(',', '')) if view_count else 0
    
    # Extrair like count
    like_count = video.get('like_count', 0)
    if isinstance(like_count, str):
        like_count = int(like_count.replace(',', '')) if like_count else 0
    
    # Extrair comment count
    comment_count = video.get('comment_count', 0)
    if isinstance(comment_count, str):
        comment_count = int(comment_count.replace(',', '')) if comment_count else 0
    
    # Duração
    duration_str = video.get('duration', '')
    duration_minutes = parse_duration(duration_str) if duration_str else 0.0
    
    return {
        'video_id': video.get('video_id', ''),
        'title': video.get('title', ''),
        'channel': video.get('channel_title', playlist_name),
        'duration': f"{duration_minutes:.1f}",
        'views': format_views(view_count),
        'viewCount': view_count,
        'summary': video.get('description', '')[:200] + '...' if len(video.get('description', '')) > 200 else video.get('description', ''),
        'keyPoints': [],  # Não temos key points nas playlists
        'publishedAt': video.get('published_at', ''),
        'thumbnail': video.get('thumbnail_url', ''),
        'likeCount': like_count,
        'commentCount': comment_count,
    }


def load_playlists(playlist_filter: str = None) -> dict:
    """Carrega playlists do diretório"""
    playlists = {}
    
    if not PLAYLISTS_DIR.exists():
        print(f"❌ Diretório de playlists não encontrado: {PLAYLISTS_DIR}")
        return playlists
    
    for json_file in PLAYLISTS_DIR.glob('*.json'):
        playlist_name = json_file.stem
        
        # Filtrar se especificado
        if playlist_filter and playlist_name != playlist_filter:
            continue
        
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                playlists[playlist_name] = data
                print(f"  ✓ {playlist_name}: {len(data.get('videos', []))} vídeos")
        except Exception as e:
            print(f"  ✗ Erro ao carregar {json_file}: {e}")
    
    return playlists


def convert_to_edition(playlists: dict) -> dict:
    """Converte playlists para o formato de edição"""
    
    # Agrupar vídeos por categoria
    categories_data = {}
    total_videos = 0
    
    for playlist_name, playlist_data in playlists.items():
        category_id = PLAYLIST_TO_CATEGORY.get(playlist_name, 'outros')
        
        if category_id not in categories_data:
            categories_data[category_id] = []
        
        videos = playlist_data.get('videos', [])
        for video in videos:
            converted = convert_video(video, playlist_name)
            categories_data[category_id].append(converted)
            total_videos += 1
    
    # Construir estrutura de categorias
    categories = []
    for cat_id, videos in categories_data.items():
        if not videos:
            continue
        
        meta = CATEGORY_META.get(cat_id, {'emoji': '📌', 'name': cat_id, 'description': ''})
        
        # Ordenar por data de publicação (mais recentes primeiro)
        videos.sort(key=lambda v: v.get('publishedAt', ''), reverse=True)
        
        categories.append({
            'id': cat_id,
            'name': meta['name'],
            'emoji': meta['emoji'],
            'description': meta['description'],
            'videoCount': len(videos),
            'videos': videos,
        })
    
    # Ordenar categorias por quantidade de vídeos
    categories.sort(key=lambda c: c['videoCount'], reverse=True)
    
    # Construir edição
    today = datetime.now()
    edition = {
        'date': today.strftime('%Y-%m-%d'),
        'title': f'Playlists - {today.strftime("%d/%m/%Y")}',
        'generatedAt': today.isoformat(),
        'collectedAt': today.isoformat(),
        'totalVideos': total_videos,
        'categories': categories,
    }
    
    return edition


def save_edition(edition: dict, output_name: str = None) -> Path:
    """Salva a edição no diretório de edições"""
    
    EDITIONS_DIR.mkdir(parents=True, exist_ok=True)
    
    if output_name:
        output_path = EDITIONS_DIR / f"{output_name}.json"
    else:
        output_path = EDITIONS_DIR / f"playlists-{edition['date']}.json"
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(edition, f, ensure_ascii=False, indent=2)
    
    return output_path


def update_index(edition_path: Path, edition: dict):
    """Atualiza o índice de edições"""
    index_path = EDITIONS_DIR / 'index.json'
    
    # Carregar índice existente
    if index_path.exists():
        with open(index_path, 'r', encoding='utf-8') as f:
            index = json.load(f)
    else:
        index = {'latest': '', 'editions': []}
    
    # Adicionar nova edição se não existir
    edition_date = edition['date']
    existing_dates = [e.get('date', e.get('id', '')) for e in index['editions']]
    
    if edition_date not in existing_dates:
        index['editions'].insert(0, {
            'date': edition['date'],
            'title': edition['title'],
            'videoCount': edition['totalVideos'],
            'categoryCount': len(edition['categories']),
            'generatedAt': edition['generatedAt'],
        })
        
        # Atualizar latest
        index['latest'] = edition['date']
        
        # Salvar índice atualizado
        with open(index_path, 'w', encoding='utf-8') as f:
            json.dump(index, f, ensure_ascii=False, indent=2)


def main():
    parser = argparse.ArgumentParser(description='Converte playlists para formato de edição')
    parser.add_argument('--playlist', type=str, help='Nome da playlist específica (sem .json)')
    parser.add_argument('--output', type=str, help='Nome do arquivo de saída (sem .json)')
    parser.add_argument('--generate-ts', action='store_true', help='Também gera real-data.ts')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("🔄 Conversor de Playlists para Edição")
    print("=" * 60)
    
    # Carregar playlists
    print(f"\n📂 Carregando playlists de: {PLAYLISTS_DIR}")
    playlists = load_playlists(args.playlist)
    
    if not playlists:
        print("❌ Nenhuma playlist encontrada!")
        return
    
    print(f"\n📊 Total: {len(playlists)} playlists")
    
    # Converter para edição
    print("\n🔄 Convertendo para formato de edição...")
    edition = convert_to_edition(playlists)
    
    print(f"  ✓ {edition['totalVideos']} vídeos")
    print(f"  ✓ {len(edition['categories'])} categorias")
    
    # Salvar edição
    print("\n💾 Salvando edição...")
    output_path = save_edition(edition, args.output)
    print(f"  ✓ Salvo em: {output_path}")
    
    # Atualizar índice
    update_index(output_path, edition)
    print("  ✓ Índice atualizado")
    
    # Gerar real-data.ts se solicitado
    if args.generate_ts:
        print("\n🔄 Gerando real-data.ts...")
        result = subprocess.run(
            [sys.executable, str(SCRIPT_DIR / 'generate_real_data.py'), '--edition', output_path.stem],
            cwd=str(SCRIPT_DIR),
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print("  ✓ real-data.ts gerado com sucesso")
        else:
            print(f"  ✗ Erro ao gerar real-data.ts: {result.stderr}")
    
    print("\n✅ Conversão concluída!")
    print(f"   Edição: {output_path.name}")
    print(f"   Vídeos: {edition['totalVideos']}")
    print(f"   Categorias: {len(edition['categories'])}")


if __name__ == '__main__':
    main()
