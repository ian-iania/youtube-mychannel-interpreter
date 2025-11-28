#!/usr/bin/env python3
"""
Script para atualizar ui/lib/real-data.ts com vídeos categorizados
Lê: newsletters/2025-11-27_videos_categorized.json
Gera: ui/lib/real-data.ts (atualizado)
"""

import json
import os
from datetime import datetime
from typing import Dict, List

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

def update_ui_data():
    """Atualiza o arquivo TypeScript com vídeos categorizados"""
    
    # Caminhos
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Tentar usar dados enriquecidos primeiro, senão usar categorizados
    enriched_file = os.path.join(base_dir, "newsletters", "2025-11-27_videos_enriched.json")
    categorized_file = os.path.join(base_dir, "newsletters", "2025-11-27_videos_categorized.json")
    
    if os.path.exists(enriched_file):
        input_file = enriched_file
        print("📖 Usando dados enriquecidos (com summaries e key points)")
    else:
        input_file = categorized_file
        print("📖 Usando dados categorizados (sem summaries)")
    
    output_file = os.path.join(base_dir, "ui", "lib", "real-data.ts")
    
    print(f"📖 Lendo: {input_file}")
    
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    categories_data = data.get("categories", {})
    total_videos = data.get("total_videos", 0)
    collected_at = data.get("collected_at", "")
    
    print(f"✅ {total_videos} vídeos em {len(categories_data)} categorias")
    
    # Gerar TypeScript
    ts_content = generate_typescript(categories_data, collected_at)
    
    # Salvar
    print(f"💾 Salvando: {output_file}")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(ts_content)
    
    print("✨ Atualização completa!")
    
    # Estatísticas
    print("\n📊 Estatísticas:")
    for cat_id, videos in sorted(categories_data.items(), key=lambda x: len(x[1]), reverse=True):
        if videos:
            print(f"  {cat_id:25} {len(videos):3} vídeos")

def generate_typescript(categories_data: Dict, collected_at: str) -> str:
    """Gera o conteúdo do arquivo TypeScript"""
    
    ts_lines = [
        '/**',
        ' * Dados reais dos 473 vídeos coletados e categorizados',
        f' * Gerado automaticamente em: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',
        ' * Categorizado com: GPT-4o-mini',
        ' * Fonte: newsletters/2025-11-27_videos_categorized.json',
        ' */',
        '',
        'import { Edition, Category, Video } from "./types";',
        'import { CATEGORY_META } from "./types";',
        '',
        '// Vídeos por categoria',
    ]
    
    # Gerar arrays de vídeos por categoria
    for cat_id, videos in sorted(categories_data.items()):
        if not videos:
            continue
            
        ts_lines.append(f'\nconst {cat_id.upper().replace("-", "_")}_VIDEOS: Video[] = [')
        
        for video in videos:
            video_id = extract_video_id(video.get("url", ""))
            
            # Escapar strings para TypeScript
            def escape_ts(s):
                return s.replace('\\', '\\\\').replace('"', '\\"').replace('\n', ' ').replace('\r', '')
            
            summary = escape_ts(video.get("summary", ""))
            key_points = video.get("keyPoints", [])
            key_points_ts = ', '.join([f'"{escape_ts(kp)}"' for kp in key_points])
            
            ts_lines.append('  {')
            ts_lines.append(f'    video_id: "{video_id}",')
            ts_lines.append(f'    title: "{escape_ts(video.get("title", ""))}",')
            ts_lines.append(f'    channel: "{escape_ts(video.get("channel", ""))}",')
            ts_lines.append(f'    duration: "{format_duration(video.get("duration", ""))}",')
            ts_lines.append(f'    views: "{video.get("views", "0")}",')
            ts_lines.append(f'    viewCount: {int(video.get("view_count", 0))},')
            ts_lines.append(f'    summary: "{summary}",')
            ts_lines.append(f'    keyPoints: [{key_points_ts}],')
            ts_lines.append(f'    url: "{video.get("url", "")}",')
            ts_lines.append(f'    publishedAt: "{video.get("published_at", "")}",')
            ts_lines.append(f'    likeCount: {int(video.get("like_count", 0))},')
            ts_lines.append(f'    commentCount: {int(video.get("comment_count", 0))},')
            ts_lines.append('  },')
        
        ts_lines.append('];')
    
    # Gerar categorias
    ts_lines.append('\n// Categorias com vídeos reais')
    ts_lines.append('const REAL_CATEGORIES: Category[] = [')
    
    for cat_id in sorted(categories_data.keys()):
        videos = categories_data[cat_id]
        if not videos:
            continue
            
        videos_count = len(videos)
        cat_var = cat_id.upper().replace("-", "_")
        
        ts_lines.append('  {')
        ts_lines.append(f'    id: "{cat_id}",')
        ts_lines.append(f'    emoji: CATEGORY_META["{cat_id}"]?.emoji || "📁",')
        ts_lines.append(f'    name: CATEGORY_META["{cat_id}"]?.name || "Categoria",')
        ts_lines.append(f'    description: CATEGORY_META["{cat_id}"]?.description || "",')
        ts_lines.append(f'    videoCount: {videos_count},')
        ts_lines.append(f'    videos: {cat_var}_VIDEOS,')
        ts_lines.append(f'    imagePrompt: CATEGORY_META["{cat_id}"]?.imagePrompt,')
        ts_lines.append('  },')
    
    ts_lines.append('];')
    
    # Gerar edição
    total_videos = sum(len(v) for v in categories_data.values())
    
    ts_lines.extend([
        '',
        '// Edição atual com dados reais categorizados',
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
    update_ui_data()
