#!/usr/bin/env python3
"""
Gera newsletter temática em Markdown a partir dos vídeos analisados
Versão 2.0 - Organização por temas relevantes
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict

def load_analyzed_videos(input_file):
    """Carrega vídeos analisados"""
    file_path = Path(__file__).parent.parent / 'newsletters' / input_file
    
    if not file_path.exists():
        print(f"❌ Erro: Arquivo {input_file} não encontrado")
        sys.exit(1)
    
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def classify_video_by_theme(video, channel_name, channel_type):
    """
    Classifica vídeo por tema
    
    Returns:
        Lista de temas aplicáveis
    """
    title = video['title'].lower()
    description = video.get('description', '').lower()
    analysis = video.get('gemini_analysis', {}).get('analysis', {})
    topics = [str(t).lower() for t in analysis.get('topics', [])]
    
    themes = []
    
    # 1. Novos Modelos / Atualizações de Modelos
    model_keywords = ['gemini', 'gpt', 'claude', 'llama', 'mistral', 'anthropic', 
                      'openai', 'deepmind', 'model', 'llm']
    if any(kw in title or kw in description for kw in model_keywords):
        themes.append('models')
    
    # 2. Produtos e Atualizações de Empresas
    if channel_type == 'company' or any(kw in title for kw in ['launch', 'release', 'update', 'new feature']):
        themes.append('company_updates')
    
    # 3. Ferramentas de Automação (n8n, Make, Zapier)
    automation_keywords = ['n8n', 'make', 'zapier', 'automation', 'workflow', 'automat']
    if any(kw in title or kw in description for kw in automation_keywords):
        themes.append('automation')
    
    # 4. IDEs e Agentes de Código
    ide_keywords = ['cursor', 'vscode', 'ide', 'copilot', 'cline', 'windsurf', 
                    'coder', 'coding assistant', 'code editor']
    if any(kw in title or kw in description for kw in ide_keywords):
        themes.append('ides')
    
    # 5. Arquitetura e Design de Software
    arch_keywords = ['architecture', 'design pattern', 'arquitetura', 'design de software',
                     'system design', 'rag', 'agent architecture']
    if any(kw in title or kw in description for kw in arch_keywords):
        themes.append('architecture')
    
    # 6. Cursos e Treinamentos
    course_keywords = ['course', 'tutorial', 'training', 'curso', 'treinamento', 
                       'learn', 'deeplearning.ai', 'andrew ng']
    if any(kw in title or kw in description for kw in course_keywords) or analysis.get('is_tutorial'):
        themes.append('courses')
    
    # 7. Ferramentas de Mídia (Vídeo, Imagem, Áudio)
    media_keywords = ['video', 'image', 'audio', 'generation', 'sora', 'midjourney', 
                      'stable diffusion', 'dall-e', 'imagen', 'vídeo', 'imagem']
    if any(kw in title or kw in description for kw in media_keywords):
        themes.append('media_tools')
    
    # 8. NotebookLM (tema muito presente)
    if 'notebooklm' in title or 'notebooklm' in description:
        themes.append('notebooklm')
    
    # 9. GitHub e Ferramentas de Desenvolvimento
    if 'github' in title or channel_name == 'Github Awesome':
        themes.append('github_tools')
    
    # 10. Notícias e Assuntos Gerais de IA
    news_channels = ['tecmundo', 'argonauta', 'inteligência mil grau', 'ai labs']
    if any(ch in channel_name.lower() for ch in news_channels):
        themes.append('news')
    
    # Se não tem tema específico, vai para "outros"
    if not themes:
        themes.append('other')
    
    return themes


def organize_by_themes(data):
    """
    Organiza vídeos por temas
    
    Returns:
        Dict com vídeos agrupados por tema
    """
    themes = defaultdict(list)
    
    for channel_id, channel_data in data['channels'].items():
        channel_info = channel_data['channel_info']
        channel_name = channel_info['channel_title']
        channel_type = channel_info.get('channel_type', 'person')
        
        for video in channel_data['videos']:
            video['_channel_info'] = channel_info
            video_themes = classify_video_by_theme(video, channel_name, channel_type)
            
            # Adicionar vídeo a todos os temas aplicáveis
            for theme in video_themes:
                themes[theme].append(video)
    
    return themes


def deduplicate_videos(videos):
    """
    Remove vídeos duplicados (mesmo título ou muito similar)
    Mantém o com maior relevância
    """
    seen_titles = {}
    unique_videos = []
    
    for video in videos:
        title = video['title'].lower()
        
        # Normalizar título (remover pontuação extra)
        import re
        normalized = re.sub(r'[^\w\s]', '', title)
        
        # Verificar se já vimos título similar
        is_duplicate = False
        for seen_title in seen_titles:
            # Similaridade simples (palavras em comum)
            words1 = set(normalized.split())
            words2 = set(seen_title.split())
            
            if len(words1 & words2) / max(len(words1), len(words2)) > 0.7:
                is_duplicate = True
                break
        
        if not is_duplicate:
            seen_titles[normalized] = video
            unique_videos.append(video)
    
    return unique_videos


def format_number(num):
    """Formata número com separador de milhares"""
    num = int(num)
    if num >= 1_000_000:
        return f"{num/1_000_000:.1f}M"
    elif num >= 1_000:
        return f"{num/1_000:.1f}K"
    return str(num)


def generate_video_card(video, show_channel=True):
    """
    Gera card Markdown para um vídeo (versão compacta)
    """
    title = video['title']
    video_id = video['video_id']
    video_url = f"https://youtube.com/watch?v={video_id}"
    thumbnail = f"https://img.youtube.com/vi/{video_id}/mqdefault.jpg"  # Thumbnail menor
    
    # Metadata
    duration = video.get('duration_minutes', 0)
    views = format_number(video.get('view_count', 0))
    
    # Channel info
    channel_info = video.get('_channel_info', {})
    channel_name = channel_info.get('channel_title', 'Unknown')
    
    # Analysis
    analysis = video.get('gemini_analysis', {}).get('analysis', {})
    summary = analysis.get('summary', 'Sem resumo disponível')
    takeaways = analysis.get('key_takeaways', [])
    
    # Build markdown (versão compacta)
    md = f"\n#### {title}\n\n"
    
    if show_channel:
        md += f"**📺 {channel_name}** | "
    
    md += f"⏱️ {duration:.0f} min | 👁️ {views} views\n\n"
    md += f"{summary}\n\n"
    
    if takeaways:
        md += "**Principais pontos:**\n"
        for takeaway in takeaways[:3]:  # Máximo 3
            md += f"- {takeaway}\n"
        md += "\n"
    
    md += f"[▶️ Assistir]({video_url})\n\n"
    
    return md


def generate_newsletter_v2(data, output_file=None):
    """
    Gera newsletter temática
    """
    print("\n📰 Gerando newsletter temática...")
    
    # Organizar por temas
    print("   🎯 Classificando vídeos por tema...")
    themes = organize_by_themes(data)
    
    # Remover duplicatas em cada tema
    print("   🔍 Removendo duplicatas...")
    for theme in themes:
        themes[theme] = deduplicate_videos(themes[theme])
    
    # Estatísticas
    total_videos = sum(len(videos) for videos in themes.values())
    
    # Data
    week_str = datetime.now().strftime('Semana de %d/%m/%Y')
    date_str = datetime.now().strftime('%d de %B de %Y')
    
    # Build newsletter
    print("   ✍️  Gerando Markdown...")
    
    md = f"""# 🤖 AI Newsletter - {week_str}

> Sua curadoria semanal de IA e tecnologia, organizada por temas relevantes

---

## 📊 Nesta Edição

"""
    
    # Índice dinâmico
    section_order = [
        ('models', '🚀 Novos Modelos e Atualizações', 'Últimas novidades em modelos de IA'),
        ('company_updates', '🏢 Produtos e Atualizações de Empresas', 'Lançamentos e features de empresas de IA'),
        ('automation', '⚙️ Automação e Workflows', 'n8n, Make, Zapier e ferramentas de automação'),
        ('ides', '💻 IDEs e Agentes de Código', 'Ferramentas para desenvolvimento com IA'),
        ('notebooklm', '📓 NotebookLM', 'Novidades e tutoriais do NotebookLM'),
        ('architecture', '🏗️ Arquitetura e Design', 'Padrões, RAG, e design de sistemas com IA'),
        ('courses', '🎓 Cursos e Treinamentos', 'Tutoriais e conteúdo educacional'),
        ('github_tools', '🔧 Ferramentas de Desenvolvimento', 'Projetos e ferramentas do GitHub'),
        ('media_tools', '🎨 Ferramentas de Mídia', 'Geração de vídeo, imagem e áudio'),
        ('news', '📰 Notícias e Assuntos Gerais', 'Novidades e tendências em IA'),
        ('other', '📌 Outros Temas', 'Conteúdo diverso e interessante')
    ]
    
    # Contar vídeos por seção
    sections_with_content = []
    for theme_key, title, desc in section_order:
        count = len(themes.get(theme_key, []))
        if count > 0:
            sections_with_content.append((theme_key, title, desc, count))
            md += f"- **{title}** ({count} vídeos)\n"
    
    md += f"\n**Total: {total_videos} vídeos curados**\n\n"
    md += "---\n\n"
    
    # Gerar seções
    for theme_key, title, description, count in sections_with_content:
        videos = themes[theme_key]
        
        md += f"## {title}\n\n"
        md += f"*{description}*\n\n"
        md += f"**{count} vídeo{'s' if count > 1 else ''}**\n\n"
        
        # Ordenar por relevância (views)
        videos_sorted = sorted(videos, 
                              key=lambda v: int(v.get('view_count', 0)), 
                              reverse=True)
        
        # Gerar cards
        for video in videos_sorted:
            md += generate_video_card(video, show_channel=True)
        
        md += "---\n\n"
    
    # Footer
    md += f"""## 💡 Sobre Esta Newsletter

Esta newsletter é gerada automaticamente a partir de uma curadoria de **103 canais** de IA e tecnologia, 
incluindo criadores individuais, empresas e comunidades.

**Próxima edição:** {(datetime.now()).strftime('%d/%m/%Y')}

---

*Gerado com ❤️ pelo AI Newsletter Generator*  
*Powered by Google Gemini 2.0 Flash-Lite*  
*Data: {date_str}*
"""
    
    # Salvar
    if output_file is None:
        date_str = datetime.now().strftime('%Y-%m-%d')
        output_file = f"{date_str}_newsletter_v2.md"
    
    output_path = Path(__file__).parent.parent / 'newsletters' / output_file
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(md)
    
    print(f"\n💾 Newsletter salva em: {output_path}")
    
    # Estatísticas
    word_count = len(md.split())
    line_count = len(md.split('\n'))
    
    print(f"\n📊 Estatísticas:")
    print(f"   📄 Linhas: {line_count}")
    print(f"   📝 Palavras: {word_count}")
    print(f"   🎬 Vídeos: {total_videos}")
    print(f"   📑 Seções: {len(sections_with_content)}")
    print(f"   ⏰ Tempo de leitura: ~{word_count // 200} minutos")
    
    print(f"\n📋 Distribuição por tema:")
    for theme_key, title, _, count in sections_with_content:
        print(f"   • {title}: {count} vídeos")
    
    return output_path


def main():
    """Função principal"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Gera newsletter temática')
    parser.add_argument('--input', type=str, required=True, help='Arquivo JSON de entrada')
    parser.add_argument('--output', type=str, help='Arquivo Markdown de saída (opcional)')
    
    args = parser.parse_args()
    
    print("=" * 70)
    print("📰 AI Newsletter Generator v2.0 - Organização Temática")
    print("=" * 70)
    
    # Carregar vídeos analisados
    print(f"\n📂 Carregando {args.input}...")
    data = load_analyzed_videos(args.input)
    print("✅ Vídeos carregados!")
    
    # Gerar newsletter
    output_path = generate_newsletter_v2(data, args.output)
    
    print("\n✨ Newsletter temática gerada com sucesso!")
    print(f"\n📖 Para visualizar:")
    print(f"   cat {output_path}")


if __name__ == '__main__':
    main()
