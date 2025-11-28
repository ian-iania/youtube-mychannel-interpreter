#!/usr/bin/env python3
"""
Script para converter os vídeos coletados para o formato da UI
Lê: newsletters/2025-11-27_videos_full.json
Gera: ui/lib/real-data.ts
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any

# Mapeamento de categorias
CATEGORY_MAPPING = {
    "Novos Modelos e Atualizações": "novos-modelos",
    "Produtos e Atualizações de Empresas": "produtos-empresas",
    "Automação e Workflows": "automacao-workflows",
    "IDEs e Agentes de Código": "ides-agentes",
    "NotebookLM": "notebooklm",
    "Arquitetura e Design": "arquitetura-design",
    "Cursos e Treinamentos": "cursos-treinamentos",
    "Ferramentas de Desenvolvimento": "ferramentas-dev",
    "Ferramentas de Mídia": "ferramentas-midia",
    "Notícias e Assuntos Gerais": "noticias",
    "Outros Temas": "outros",
    "Recursos Adicionais": "recursos",
}

def extract_video_id(url: str) -> str:
    """Extrai o ID do vídeo do YouTube da URL"""
    if "watch?v=" in url:
        return url.split("watch?v=")[1].split("&")[0]
    elif "youtu.be/" in url:
        return url.split("youtu.be/")[1].split("?")[0]
    return ""

def format_duration(duration_str: str) -> str:
    """Formata duração de PT11M30S para minutos"""
    if not duration_str or not duration_str.startswith("PT"):
        return "0"
    
    duration_str = duration_str[2:]  # Remove PT
    minutes = 0
    seconds = 0
    
    if "H" in duration_str:
        hours_str, duration_str = duration_str.split("H")
        minutes += int(hours_str) * 60
    
    if "M" in duration_str:
        minutes_str, duration_str = duration_str.split("M")
        minutes += int(minutes_str)
    
    if "S" in duration_str:
        seconds = int(duration_str.replace("S", ""))
    
    return str(minutes + (seconds / 60))

def convert_videos_to_typescript():
    """Converte o JSON dos vídeos para TypeScript"""
    
    # Caminhos
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_file = os.path.join(base_dir, "newsletters", "2025-11-27_videos_full.json")
    output_file = os.path.join(base_dir, "ui", "lib", "real-data.ts")
    
    print(f"📖 Lendo: {input_file}")
    
    # Ler JSON
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # Organizar por categoria
    categories_data: Dict[str, List[Dict[str, Any]]] = {}
    total_videos = 0
    
    # Extrair vídeos de cada canal
    channels = data.get("channels", {})
    
    for channel_id, channel_data in channels.items():
        videos = channel_data.get("videos", [])
        
        for video in videos:
            # Determinar categoria (por enquanto, vamos categorizar depois)
            # Por ora, colocar todos em "outros"
            category_id = "outros"
            
            if category_id not in categories_data:
                categories_data[category_id] = []
            
            video_id = extract_video_id(video.get("url", ""))
            channel_name = channel_data.get("channel_info", {}).get("snippet", {}).get("title", "Unknown")
            
            # Converter para formato TypeScript
            ts_video = {
                "video_id": video_id,
                "title": video.get("title", "").replace('"', '\\"'),
                "channel": channel_name.replace('"', '\\"'),
                "duration": format_duration(video.get("duration", "")),
                "views": video.get("views", "0"),
                "viewCount": int(video.get("view_count", 0)),
                "summary": "",  # Será preenchido depois
                "keyPoints": [],
                "url": video.get("url", ""),
                "publishedAt": video.get("published_at", ""),
                "likeCount": int(video.get("like_count", 0)),
                "commentCount": int(video.get("comment_count", 0)),
            }
            
            categories_data[category_id].append(ts_video)
            total_videos += 1
    
    print(f"✅ Processados {total_videos} vídeos em {len(categories_data)} categorias")
    
    # Gerar TypeScript
    ts_content = generate_typescript(categories_data, data.get("collected_at", ""))
    
    # Escrever arquivo
    print(f"💾 Salvando: {output_file}")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(ts_content)
    
    print("✨ Conversão completa!")
    
    # Estatísticas
    print("\n📊 Estatísticas:")
    for cat_id, videos in sorted(categories_data.items(), key=lambda x: len(x[1]), reverse=True):
        cat_name = [k for k, v in CATEGORY_MAPPING.items() if v == cat_id][0]
        print(f"  {cat_name}: {len(videos)} vídeos")

def generate_typescript(categories_data: Dict[str, List[Dict]], collected_at: str) -> str:
    """Gera o conteúdo do arquivo TypeScript"""
    
    ts_lines = [
        '/**',
        ' * Dados reais dos 473 vídeos coletados',
        f' * Gerado automaticamente em: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',
        ' * Fonte: newsletters/2025-11-27_videos_full.json',
        ' */',
        '',
        'import { Edition, Category, Video } from "./types";',
        'import { CATEGORY_META } from "./types";',
        '',
        '// Vídeos por categoria',
    ]
    
    # Gerar arrays de vídeos por categoria
    for cat_id, videos in sorted(categories_data.items()):
        ts_lines.append(f'\nconst {cat_id.upper().replace("-", "_")}_VIDEOS: Video[] = [')
        
        for video in videos:
            ts_lines.append('  {')
            ts_lines.append(f'    video_id: "{video["video_id"]}",')
            ts_lines.append(f'    title: "{video["title"]}",')
            ts_lines.append(f'    channel: "{video["channel"]}",')
            ts_lines.append(f'    duration: "{video["duration"]}",')
            ts_lines.append(f'    views: "{video["views"]}",')
            ts_lines.append(f'    viewCount: {video["viewCount"]},')
            ts_lines.append(f'    summary: "{video["summary"]}",')
            ts_lines.append(f'    keyPoints: [')
            for point in video["keyPoints"]:
                ts_lines.append(f'      "{point}",')
            ts_lines.append('    ],')
            ts_lines.append(f'    url: "{video["url"]}",')
            ts_lines.append(f'    publishedAt: "{video["publishedAt"]}",')
            ts_lines.append(f'    likeCount: {video["likeCount"]},')
            ts_lines.append(f'    commentCount: {video["commentCount"]},')
            ts_lines.append('  },')
        
        ts_lines.append('];')
    
    # Gerar categorias
    ts_lines.append('\n// Categorias com vídeos reais')
    ts_lines.append('const REAL_CATEGORIES: Category[] = [')
    
    for cat_id in sorted(categories_data.keys()):
        videos_count = len(categories_data[cat_id])
        cat_var = cat_id.upper().replace("-", "_")
        
        ts_lines.append('  {')
        ts_lines.append(f'    id: "{cat_id}",')
        ts_lines.append(f'    emoji: CATEGORY_META["{cat_id}"].emoji,')
        ts_lines.append(f'    name: CATEGORY_META["{cat_id}"].name || "Categoria",')
        ts_lines.append(f'    description: CATEGORY_META["{cat_id}"].description,')
        ts_lines.append(f'    videoCount: {videos_count},')
        ts_lines.append(f'    videos: {cat_var}_VIDEOS,')
        ts_lines.append(f'    imagePrompt: CATEGORY_META["{cat_id}"].imagePrompt,')
        ts_lines.append('  },')
    
    ts_lines.append('];')
    
    # Gerar edição
    total_videos = sum(len(v) for v in categories_data.values())
    
    ts_lines.extend([
        '',
        '// Edição atual com dados reais',
        'export const REAL_EDITION: Edition = {',
        '  id: "2025-11-27",',
        '  weekLabel: "Semana de 27/11/2025",',
        '  dateRange: "24–30 nov 2025",',
        '  tagline: "Sua curadoria semanal de IA e tecnologia, organizada por temas relevantes",',
        f'  collectedAt: "{collected_at}",',
        f'  totalVideos: {total_videos},',
        '  categories: REAL_CATEGORIES,',
        '  summaryHighlights: REAL_CATEGORIES.map((cat) => ({',
        '    categoryName: cat.name,',
        '    emoji: cat.emoji,',
        '    videoCount: cat.videoCount,',
        '  })),',
        '};',
        '',
        '// Helper functions',
        'export function getAllRealVideos(): Video[] {',
        '  return REAL_CATEGORIES.flatMap((cat) => cat.videos);',
        '}',
        '',
        'export function getRealCategoryById(id: string): Category | undefined {',
        '  return REAL_CATEGORIES.find((cat) => cat.id === id);',
        '}',
        '',
        'export function getRandomRealNewsItems(count: number = 5): Video[] {',
        '  const allVideos = getAllRealVideos();',
        '  const shuffled = [...allVideos].sort(() => 0.5 - Math.random());',
        '  return shuffled.slice(0, count);',
        '}',
    ])
    
    return '\n'.join(ts_lines)

if __name__ == "__main__":
    convert_videos_to_typescript()
