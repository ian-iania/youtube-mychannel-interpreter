#!/usr/bin/env python3
"""
Gera newsletter em Markdown a partir dos vídeos analisados
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict

def load_analyzed_videos(input_file):
    """
    Carrega vídeos analisados
    
    Args:
        input_file: Arquivo JSON com análises
        
    Returns:
        Dados dos vídeos analisados
    """
    file_path = Path(__file__).parent.parent / 'newsletters' / input_file
    
    if not file_path.exists():
        print(f"❌ Erro: Arquivo {input_file} não encontrado")
        print("   Execute primeiro: python scripts/analyze_videos.py")
        sys.exit(1)
    
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def group_by_channel_type(data):
    """
    Agrupa vídeos por tipo de canal
    
    Args:
        data: Dados dos vídeos
        
    Returns:
        Dict com vídeos agrupados por tipo
    """
    grouped = {
        'person': [],
        'company': [],
        'community': []
    }
    
    for channel_id, channel_data in data['channels'].items():
        channel_info = channel_data['channel_info']
        channel_type = channel_info.get('channel_type', 'person')
        videos = channel_data['videos']
        
        for video in videos:
            video['_channel_info'] = channel_info
            grouped[channel_type].append(video)
    
    return grouped


def calculate_relevance_score(video):
    """
    Calcula score de relevância do vídeo
    
    Args:
        video: Dados do vídeo
        
    Returns:
        Score de relevância
    """
    views = int(video.get('view_count', 0))
    likes = int(video.get('like_count', 0))
    
    # Normalizar views (log scale)
    import math
    view_score = math.log10(views + 1) * 10 if views > 0 else 0
    
    # Engagement rate
    engagement = (likes / views * 100) if views > 0 else 0
    
    # Score final
    score = view_score * 0.7 + engagement * 0.3
    
    return score


def sort_by_relevance(videos):
    """
    Ordena vídeos por relevância
    
    Args:
        videos: Lista de vídeos
        
    Returns:
        Lista ordenada
    """
    return sorted(videos, key=calculate_relevance_score, reverse=True)


def format_number(num):
    """
    Formata número com separador de milhares
    
    Args:
        num: Número
        
    Returns:
        String formatada
    """
    num = int(num)
    if num >= 1_000_000:
        return f"{num/1_000_000:.1f}M"
    elif num >= 1_000:
        return f"{num/1_000:.1f}K"
    return str(num)


def generate_video_section(video, index):
    """
    Gera seção Markdown para um vídeo
    
    Args:
        video: Dados do vídeo
        index: Índice do vídeo
        
    Returns:
        String Markdown
    """
    title = video['title']
    video_id = video['video_id']
    video_url = f"https://youtube.com/watch?v={video_id}"
    thumbnail = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
    
    # Metadata
    duration = video.get('duration_minutes', 0)
    views = format_number(video.get('view_count', 0))
    published = video.get('published_at', '')[:10]  # YYYY-MM-DD
    
    # Channel info
    channel_info = video.get('_channel_info', {})
    channel_name = channel_info.get('channel_title', 'Unknown')
    
    # Analysis
    analysis = video.get('gemini_analysis', {}).get('analysis', {})
    summary = analysis.get('summary', 'Sem resumo disponível')
    takeaways = analysis.get('key_takeaways', [])
    topics = analysis.get('topics', [])
    difficulty = analysis.get('difficulty', 'intermediate')
    is_tutorial = analysis.get('is_tutorial', False)
    tutorial_steps = analysis.get('tutorial_steps', [])
    
    # Difficulty emoji
    difficulty_emoji = {
        'beginner': '🟢',
        'intermediate': '🟡',
        'advanced': '🔴'
    }.get(difficulty.lower(), '🟡')
    
    # Build markdown
    md = f"\n### {index}. {title}\n\n"
    md += f"[![Thumbnail]({thumbnail})]({video_url})\n\n"
    md += f"**📺 Canal:** {channel_name} | "
    md += f"**⏱️ Duração:** {duration:.0f} min | "
    md += f"**👁️ Views:** {views} | "
    md += f"**📅 Publicado:** {published}\n\n"
    md += f"**{difficulty_emoji} Nível:** {difficulty.capitalize()}"
    
    if is_tutorial:
        md += " | **📚 Tutorial**"
    
    md += "\n\n"
    
    # Summary
    md += f"**Resumo:**\n{summary}\n\n"
    
    # Takeaways
    if takeaways:
        md += "**Principais Pontos:**\n"
        for takeaway in takeaways[:5]:
            md += f"- {takeaway}\n"
        md += "\n"
    
    # Tutorial steps
    if is_tutorial and tutorial_steps:
        md += "**Passos do Tutorial:**\n"
        for i, step in enumerate(tutorial_steps[:5], 1):
            md += f"{i}. {step}\n"
        md += "\n"
    
    # Topics
    if topics:
        md += f"**Tópicos:** {', '.join(topics[:5])}\n\n"
    
    md += f"[▶️ Assistir no YouTube]({video_url})\n\n"
    md += "---\n"
    
    return md


def extract_trending_topics(grouped_videos):
    """
    Extrai tópicos em alta
    
    Args:
        grouped_videos: Vídeos agrupados
        
    Returns:
        Lista de tópicos com contagem
    """
    topic_count = defaultdict(int)
    
    for channel_type, videos in grouped_videos.items():
        for video in videos:
            analysis = video.get('gemini_analysis', {}).get('analysis', {})
            topics = analysis.get('topics', [])
            
            for topic in topics:
                topic_count[topic] += 1
    
    # Ordenar por frequência
    sorted_topics = sorted(topic_count.items(), key=lambda x: x[1], reverse=True)
    
    return sorted_topics[:10]


def generate_newsletter(data, output_file=None):
    """
    Gera newsletter completa em Markdown
    
    Args:
        data: Dados dos vídeos analisados
        output_file: Nome do arquivo de saída (opcional)
        
    Returns:
        Path do arquivo gerado
    """
    print("\n📰 Gerando newsletter...")
    
    # Agrupar por tipo
    print("   📊 Agrupando por tipo de canal...")
    grouped = group_by_channel_type(data)
    
    # Ordenar por relevância
    print("   🎯 Ordenando por relevância...")
    for channel_type in grouped:
        grouped[channel_type] = sort_by_relevance(grouped[channel_type])
    
    # Estatísticas
    total_videos = sum(len(videos) for videos in grouped.values())
    person_count = len(grouped['person'])
    company_count = len(grouped['company'])
    community_count = len(grouped['community'])
    
    # Data
    date_str = datetime.now().strftime('%d de %B de %Y')
    week_str = datetime.now().strftime('Semana de %d/%m/%Y')
    
    # Trending topics
    print("   📈 Extraindo tópicos em alta...")
    trending = extract_trending_topics(grouped)
    
    # Build newsletter
    print("   ✍️  Gerando Markdown...")
    
    md = f"""# 🤖 AI Newsletter - {week_str}

> Sua dose semanal de conteúdo sobre IA e tecnologia dos melhores criadores, empresas e comunidades

---

## 📊 Destaques da Semana

- 📺 **{total_videos} vídeos** de **9 canais**
- 👤 **{person_count} vídeos** de criadores
- 🏢 **{company_count} vídeos** de empresas
- 👥 **{community_count} vídeos** de comunidades

---

## 📑 Índice

1. [👤 Criadores de Conteúdo](#-criadores-de-conteúdo) ({person_count} vídeos)
2. [🏢 Empresas](#-empresas) ({company_count} vídeos)
3. [👥 Comunidades](#-comunidades) ({community_count} vídeos)
4. [📈 Tópicos em Alta](#-tópicos-em-alta)

---

"""
    
    # Seção: Criadores
    if person_count > 0:
        md += "## 👤 Criadores de Conteúdo\n\n"
        md += f"*{person_count} vídeos de criadores individuais*\n\n"
        
        for idx, video in enumerate(grouped['person'], 1):
            md += generate_video_section(video, idx)
    
    # Seção: Empresas
    if company_count > 0:
        md += "\n## 🏢 Empresas\n\n"
        md += f"*{company_count} vídeos de empresas de tecnologia*\n\n"
        
        for idx, video in enumerate(grouped['company'], 1):
            md += generate_video_section(video, idx)
    
    # Seção: Comunidades
    if community_count > 0:
        md += "\n## 👥 Comunidades\n\n"
        md += f"*{community_count} vídeos de comunidades e coletivos*\n\n"
        
        for idx, video in enumerate(grouped['community'], 1):
            md += generate_video_section(video, idx)
    
    # Seção: Trending Topics
    if trending:
        md += "\n## 📈 Tópicos em Alta\n\n"
        md += "Os tópicos mais mencionados esta semana:\n\n"
        
        for topic, count in trending:
            md += f"- **{topic}** ({count} vídeos)\n"
        
        md += "\n"
    
    # Footer
    md += f"""---

## 📅 Próxima Edição

A próxima newsletter será publicada em **{(datetime.now()).strftime('%d/%m/%Y')}**.

**Feedback?** Adoraríamos saber sua opinião!

---

*Gerado com ❤️ pelo AI Newsletter Generator*  
*Powered by Google Gemini 2.0 Flash-Lite*  
*Data de geração: {date_str}*
"""
    
    # Salvar
    if output_file is None:
        date_str = datetime.now().strftime('%Y-%m-%d')
        output_file = f"{date_str}_newsletter.md"
    
    output_path = Path(__file__).parent.parent / 'newsletters' / output_file
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(md)
    
    print(f"\n💾 Newsletter salva em: {output_path}")
    
    # Estatísticas
    word_count = len(md.split())
    line_count = len(md.split('\n'))
    
    print(f"\n📊 Estatísticas da Newsletter:")
    print(f"   📄 Linhas: {line_count}")
    print(f"   📝 Palavras: {word_count}")
    print(f"   🎬 Vídeos: {total_videos}")
    print(f"   📺 Canais: 9")
    print(f"   ⏰ Tempo de leitura estimado: {word_count // 200} minutos")
    
    return output_path


def main():
    """Função principal"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Gera newsletter em Markdown')
    parser.add_argument('--input', type=str, required=True, help='Arquivo JSON de entrada')
    parser.add_argument('--output', type=str, help='Arquivo Markdown de saída (opcional)')
    
    args = parser.parse_args()
    
    print("=" * 70)
    print("📰 AI Newsletter Generator")
    print("=" * 70)
    
    # Carregar vídeos analisados
    print(f"\n📂 Carregando {args.input}...")
    data = load_analyzed_videos(args.input)
    print("✅ Vídeos carregados!")
    
    # Gerar newsletter
    output_path = generate_newsletter(data, args.output)
    
    print("\n✨ Newsletter gerada com sucesso!")
    print(f"\n📖 Para visualizar:")
    print(f"   cat {output_path}")
    print(f"\n🌐 Ou abra no seu editor favorito!")


if __name__ == '__main__':
    main()
