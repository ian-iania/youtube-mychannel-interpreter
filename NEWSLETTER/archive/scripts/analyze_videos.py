#!/usr/bin/env python3
"""
Analisa vídeos usando Google Gemini 2.5 Flash-Lite
"""

import os
import sys
import json
import time
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Importar Gemini
try:
    import google.generativeai as genai
except ImportError:
    print("❌ Erro: google-generativeai não instalado")
    print("   Execute: pip install google-generativeai")
    sys.exit(1)


def configure_gemini():
    """
    Configura API do Gemini
    
    Returns:
        Modelo configurado
    """
    api_key = os.getenv('GEMINI_API_KEY')
    
    if not api_key:
        print("❌ Erro: GEMINI_API_KEY não encontrada no .env")
        print("   Obtenha sua chave em: https://aistudio.google.com/")
        sys.exit(1)
    
    genai.configure(api_key=api_key)
    
    # Usar Gemini 2.0 Flash-Lite (testado e aprovado)
    model = genai.GenerativeModel(
        'gemini-2.0-flash-lite-001',
        generation_config={
            'temperature': 0.7,
            'max_output_tokens': 500,
            'top_p': 0.95,
            'top_k': 40
        }
    )
    
    return model


def parse_analysis_text(text):
    """
    Parse texto de análise em estrutura
    
    Args:
        text: Texto da análise
        
    Returns:
        Dict estruturado
    """
    analysis = {
        'summary': '',
        'key_takeaways': [],
        'is_tutorial': False,
        'tutorial_steps': [],
        'topics': [],
        'difficulty': 'intermediate',
        'target_audience': 'developers'
    }
    
    # Extrair seções (parsing simples)
    lines = text.split('\n')
    current_section = None
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Detectar seções
        if 'resumo' in line.lower() or '1.' in line:
            current_section = 'summary'
        elif 'takeaway' in line.lower() or '2.' in line:
            current_section = 'takeaways'
        elif 'tutorial' in line.lower() or '3.' in line:
            current_section = 'tutorial'
        elif 'passos' in line.lower() or '4.' in line:
            current_section = 'steps'
        elif 'tópicos' in line.lower() or '5.' in line:
            current_section = 'topics'
        elif 'dificuldade' in line.lower() or '6.' in line:
            current_section = 'difficulty'
        elif 'público' in line.lower() or '7.' in line:
            current_section = 'audience'
        
        # Extrair conteúdo
        if current_section == 'summary' and not any(x in line.lower() for x in ['resumo', '1.']):
            analysis['summary'] += line + ' '
        elif current_section == 'takeaways' and line.startswith(('-', '•', '*')):
            analysis['key_takeaways'].append(line[1:].strip())
        elif current_section == 'tutorial':
            if 'sim' in line.lower():
                analysis['is_tutorial'] = True
        elif current_section == 'steps' and line.startswith(('-', '•', '*', '1', '2', '3', '4', '5')):
            analysis['tutorial_steps'].append(line.lstrip('-•*0123456789. '))
        elif current_section == 'topics' and line.startswith(('-', '•', '*')):
            analysis['topics'].append(line[1:].strip())
        elif current_section == 'difficulty':
            if 'iniciante' in line.lower():
                analysis['difficulty'] = 'beginner'
            elif 'intermediário' in line.lower():
                analysis['difficulty'] = 'intermediate'
            elif 'avançado' in line.lower():
                analysis['difficulty'] = 'advanced'
        elif current_section == 'audience':
            analysis['target_audience'] = line.lower()
    
    # Limpar
    analysis['summary'] = analysis['summary'].strip()
    
    return analysis


def analyze_video_full(model, video_data):
    """
    Análise completa de vídeo (≤15 min)
    Usa apenas título e descrição (não faz upload de vídeo)
    
    Args:
        model: Modelo Gemini
        video_data: Dados do vídeo
        
    Returns:
        Análise estruturada
    """
    title = video_data['title']
    description = video_data.get('description', 'Sem descrição')
    
    prompt = f"""Você é um assistente especializado em análise de conteúdo de IA e tecnologia.

Analise este vídeo do YouTube e forneça uma análise estruturada:

**Título:** {title}

**Descrição:** {description}

Forneça sua análise no seguinte formato (responda em português):

1. **Resumo** (2-3 frases sobre o conteúdo do vídeo)

2. **Principais Takeaways** (3-5 pontos principais que o espectador aprenderá)

3. **É Tutorial?** (Sim/Não)

4. **Passos do Tutorial** (se aplicável, liste os principais passos)

5. **Tópicos Principais** (liste 3-5 tópicos/tecnologias abordados)

6. **Nível de Dificuldade** (Iniciante/Intermediário/Avançado)

7. **Público-Alvo** (desenvolvedores/pesquisadores/entusiastas/geral)

Seja conciso mas informativo. Foque no valor prático para quem vai assistir."""
    
    try:
        response = model.generate_content(prompt)
        
        # Extrair texto
        analysis_text = response.text.strip()
        
        # Parse estruturado (extrair seções)
        analysis = parse_analysis_text(analysis_text)
        
        # Adicionar metadata
        if hasattr(response, 'usage_metadata'):
            analysis['_metadata'] = {
                'input_tokens': response.usage_metadata.prompt_token_count,
                'output_tokens': response.usage_metadata.candidates_token_count,
                'total_tokens': response.usage_metadata.total_token_count
            }
        
        return {
            'status': 'success',
            'analysis_type': 'full',
            'analysis': analysis,
            'raw_text': analysis_text
        }
        
    except Exception as e:
        print(f"   ❌ Erro na análise: {e}")
        
        # Fallback: análise mínima
        return {
            'status': 'error',
            'analysis_type': 'full',
            'analysis': {
                'summary': f"Erro ao analisar: {str(e)}",
                'key_takeaways': [],
                'is_tutorial': False,
                'tutorial_steps': [],
                'topics': [],
                'difficulty': 'unknown',
                'target_audience': 'general'
            },
            'error': str(e)
        }


def analyze_description_only(model, video_data):
    """
    Análise apenas da descrição (>15 min)
    
    Args:
        model: Modelo Gemini
        video_data: Dados do vídeo
        
    Returns:
        Análise da descrição
    """
    title = video_data['title']
    description = video_data['description']
    duration_min = video_data.get('duration_minutes', 0)
    
    prompt = f"""
Analise a descrição deste vídeo longo ({duration_min:.0f} minutos) sobre IA/tecnologia:

**Título:** {title}

**Descrição:** {description}

Forneça uma análise estruturada em JSON com:

{{
  "summary": "Resumo baseado na descrição (2-3 parágrafos, máximo 200 palavras)",
  "key_topics": ["Tópico 1", "Tópico 2", "Tópico 3"],
  "is_tutorial": true/false,
  "difficulty": "beginner/intermediate/advanced",
  "note": "Vídeo longo - análise baseada apenas na descrição"
}}

**Instruções:**
- Seja conciso
- Extraia os tópicos principais
- Identifique se parece ser um tutorial
- Avalie o nível de dificuldade
"""
    
    try:
        response = model.generate_content(prompt)
        
        # Parse JSON
        analysis_text = response.text.strip()
        
        # Remover markdown code blocks
        if analysis_text.startswith('```json'):
            analysis_text = analysis_text[7:]
        if analysis_text.startswith('```'):
            analysis_text = analysis_text[3:]
        if analysis_text.endswith('```'):
            analysis_text = analysis_text[:-3]
        
        analysis = json.loads(analysis_text.strip())
        
        return {
            'status': 'success',
            'analysis_type': 'description',
            'analysis': analysis
        }
        
    except json.JSONDecodeError as e:
        print(f"   ⚠️  Erro ao parsear JSON: {e}")
        
        # Fallback
        return {
            'status': 'partial',
            'analysis_type': 'description',
            'analysis': {
                'summary': description[:300] if description else title,
                'key_topics': [],
                'is_tutorial': False,
                'difficulty': 'unknown',
                'note': 'Vídeo longo - análise baseada apenas na descrição'
            }
        }
        
    except Exception as e:
        print(f"   ❌ Erro na análise: {e}")
        return {
            'status': 'error',
            'analysis_type': 'description',
            'error': str(e)
        }


def load_videos(videos_file):
    """
    Carrega arquivo de vídeos coletados
    
    Args:
        videos_file: Arquivo JSON
        
    Returns:
        Dados dos vídeos
    """
    file_path = Path(__file__).parent.parent / 'newsletters' / videos_file
    
    if not file_path.exists():
        print(f"❌ Erro: Arquivo {videos_file} não encontrado")
        print("   Execute primeiro: python scripts/collect_videos.py")
        sys.exit(1)
    
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def analyze_all_videos(model, data, duration_threshold=15, rate_limit_delay=4):
    """
    Analisa todos os vídeos
    
    Args:
        model: Modelo Gemini
        data: Dados dos vídeos
        duration_threshold: Limite em minutos (padrão: 15)
        rate_limit_delay: Delay entre requests (padrão: 4 seg)
        
    Returns:
        Dados com análises
    """
    channels = data['channels']
    total_videos = data['statistics']['total_videos']
    
    print(f"\n🤖 Analisando vídeos com Gemini 2.5 Flash-Lite...")
    print(f"   Total de vídeos: {total_videos}")
    print(f"   Limite de duração: {duration_threshold} min")
    print(f"   Delay entre requests: {rate_limit_delay} seg")
    print()
    
    analyzed_count = 0
    full_analysis_count = 0
    description_only_count = 0
    error_count = 0
    
    for channel_id, channel_data in channels.items():
        channel_title = channel_data['channel_info']['channel_title']
        videos = channel_data['videos']
        
        if not videos:
            continue
        
        print(f"📺 {channel_title} ({len(videos)} vídeos)")
        
        for idx, video in enumerate(videos, 1):
            title = video['title'][:60] + '...' if len(video['title']) > 60 else video['title']
            duration_min = video.get('duration_minutes', 0)
            
            print(f"   {idx}. {title} ({duration_min:.1f} min)")
            
            # Decidir tipo de análise
            if duration_min <= duration_threshold:
                print(f"      🔍 Análise completa...")
                result = analyze_video_full(model, video)
                full_analysis_count += 1
            else:
                print(f"      📝 Análise da descrição...")
                result = analyze_description_only(model, video)
                description_only_count += 1
            
            # Adicionar resultado ao vídeo
            video['gemini_analysis'] = result
            
            if result['status'] == 'success':
                print(f"      ✅ Sucesso")
            elif result['status'] == 'partial':
                print(f"      ⚠️  Parcial")
            else:
                print(f"      ❌ Erro")
                error_count += 1
            
            analyzed_count += 1
            
            # Rate limiting (15 req/min = 1 a cada 4 seg)
            if analyzed_count < total_videos:
                time.sleep(rate_limit_delay)
        
        print()
    
    print(f"📊 Análise concluída:")
    print(f"   ✅ Analisados: {analyzed_count}/{total_videos}")
    print(f"   🔍 Análise completa: {full_analysis_count}")
    print(f"   📝 Só descrição: {description_only_count}")
    print(f"   ❌ Erros: {error_count}")
    
    return data


def save_analyzed_videos(data, output_file=None):
    """
    Salva vídeos analisados
    
    Args:
        data: Dados com análises
        output_file: Nome do arquivo (opcional)
    """
    if output_file is None:
        date_str = datetime.now().strftime('%Y-%m-%d')
        output_file = f"{date_str}_analyzed.json"
    
    output_path = Path(__file__).parent.parent / 'newsletters' / output_file
    
    # Atualizar timestamp
    data['analyzed_at'] = datetime.now().isoformat()
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Análises salvas em: {output_path}")


def main():
    """Função principal"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Analisa vídeos com Google Gemini')
    parser.add_argument('--input', type=str, required=True, help='Arquivo JSON de entrada')
    parser.add_argument('--output', type=str, help='Arquivo JSON de saída (opcional)')
    parser.add_argument('--duration-threshold', type=int, default=15, help='Limite de duração em minutos (padrão: 15)')
    parser.add_argument('--rate-limit-delay', type=int, default=4, help='Delay entre requests em segundos (padrão: 4)')
    
    args = parser.parse_args()
    
    print("=" * 70)
    print("🤖 Video Analyzer with Google Gemini")
    print("=" * 70)
    
    # Configurar Gemini
    print("\n🔧 Configurando Gemini...")
    model = configure_gemini()
    print("✅ Gemini configurado!")
    
    # Carregar vídeos
    print(f"\n📂 Carregando vídeos de {args.input}...")
    data = load_videos(args.input)
    print("✅ Vídeos carregados!")
    
    # Analisar
    data = analyze_all_videos(
        model, 
        data, 
        args.duration_threshold,
        args.rate_limit_delay
    )
    
    # Salvar
    save_analyzed_videos(data, args.output)
    
    print("\n✨ Análise concluída com sucesso!")
    print("\nℹ️  Próximo passo: Execute generate_newsletter.py para gerar a newsletter")


if __name__ == '__main__':
    main()
