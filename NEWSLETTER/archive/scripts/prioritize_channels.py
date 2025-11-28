#!/usr/bin/env python3
"""
Sistema de priorização de canais
Ordena canais por relevância para processar os mais importantes primeiro
"""

import json
from pathlib import Path
from datetime import datetime


def calculate_priority_score(channel_data):
    """
    Calcula score de prioridade do canal
    
    Fatores:
    - Frequência de postagem (40%)
    - Subscriber count (30%)
    - Engagement rate (20%)
    - Recency (10%)
    
    Args:
        channel_data: Dados do canal
        
    Returns:
        Score de prioridade (0-100)
    """
    score = 0
    
    # 1. Frequência de postagem (40 pontos)
    posting_frequency = channel_data.get('posting_frequency', 'unknown')
    frequency_scores = {
        'daily': 40,
        'multiple_per_week': 35,
        'weekly': 25,
        'biweekly': 15,
        'monthly': 5,
        'unknown': 10
    }
    score += frequency_scores.get(posting_frequency, 10)
    
    # 2. Subscriber count (30 pontos)
    subscriber_count = channel_data.get('subscriber_count', 0)
    if subscriber_count >= 1_000_000:
        score += 30
    elif subscriber_count >= 500_000:
        score += 25
    elif subscriber_count >= 100_000:
        score += 20
    elif subscriber_count >= 50_000:
        score += 15
    elif subscriber_count >= 10_000:
        score += 10
    else:
        score += 5
    
    # 3. Engagement rate (20 pontos)
    # Baseado em views/subscriber ratio
    avg_views = channel_data.get('avg_views', 0)
    if subscriber_count > 0:
        engagement_rate = avg_views / subscriber_count
        if engagement_rate >= 0.1:  # 10%+
            score += 20
        elif engagement_rate >= 0.05:  # 5%+
            score += 15
        elif engagement_rate >= 0.02:  # 2%+
            score += 10
        else:
            score += 5
    else:
        score += 5
    
    # 4. Recency (10 pontos)
    # Canais com vídeos recentes têm prioridade
    last_upload = channel_data.get('last_upload_date')
    if last_upload:
        try:
            last_upload_date = datetime.fromisoformat(last_upload.replace('Z', '+00:00'))
            days_since = (datetime.now(last_upload_date.tzinfo) - last_upload_date).days
            
            if days_since <= 7:
                score += 10
            elif days_since <= 14:
                score += 7
            elif days_since <= 30:
                score += 5
            else:
                score += 2
        except:
            score += 5
    else:
        score += 5
    
    return min(score, 100)


def prioritize_channels(channels_file, output_file=None):
    """
    Prioriza canais por relevância
    
    Args:
        channels_file: Arquivo com dados dos canais
        output_file: Arquivo de saída (opcional)
        
    Returns:
        Lista de canais ordenados por prioridade
    """
    print("=" * 70)
    print("🎯 Sistema de Priorização de Canais")
    print("=" * 70)
    print()
    
    # Carregar canais
    channels_path = Path(__file__).parent.parent / channels_file
    
    with open(channels_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Suportar ambos os formatos: dict ou list
    channels_list = data.get('channels', data) if isinstance(data, dict) else data
    
    if isinstance(channels_list, dict):
        # Formato dict {channel_id: channel_data}
        channels_list = [{'channel_id': k, **v} for k, v in channels_list.items()]
    
    print(f"📊 Canais carregados: {len(channels_list)}")
    print()
    
    # Calcular prioridade para cada canal
    prioritized = []
    
    for channel_data in channels_list:
        channel_id = channel_data.get('channel_id', 'unknown')
        
        # Converter subscriber_count para int se for string
        subscriber_count = channel_data.get('subscriber_count', 0)
        if isinstance(subscriber_count, str):
            try:
                subscriber_count = int(subscriber_count)
            except:
                subscriber_count = 0
        
        # Atualizar channel_data com subscriber_count convertido
        channel_data['subscriber_count'] = subscriber_count
        
        score = calculate_priority_score(channel_data)
        
        prioritized.append({
            'channel_id': channel_id,
            'channel_title': channel_data.get('channel_title', 'Unknown'),
            'channel_type': channel_data.get('type', channel_data.get('channel_type', 'unknown')),
            'priority_score': score,
            'posting_frequency': channel_data.get('posting_frequency', 'unknown'),
            'subscriber_count': subscriber_count
        })
    
    # Ordenar por prioridade (maior primeiro)
    prioritized.sort(key=lambda x: x['priority_score'], reverse=True)
    
    # Imprimir top 10
    print("🏆 Top 10 Canais Prioritários:")
    print()
    
    for i, channel in enumerate(prioritized[:10], 1):
        print(f"{i:2d}. {channel['channel_title'][:40]:40s} "
              f"(Score: {channel['priority_score']:3d}, "
              f"Freq: {channel['posting_frequency']:20s}, "
              f"Subs: {channel['subscriber_count']:,})")
    
    # Estatísticas por tipo
    print()
    print("📊 Distribuição por Tipo:")
    
    type_counts = {}
    for channel in prioritized:
        channel_type = channel['channel_type']
        type_counts[channel_type] = type_counts.get(channel_type, 0) + 1
    
    for channel_type, count in sorted(type_counts.items()):
        print(f"   {channel_type:15s}: {count:3d} canais")
    
    # Estatísticas por score
    print()
    print("📊 Distribuição por Score:")
    
    high_priority = len([c for c in prioritized if c['priority_score'] >= 70])
    medium_priority = len([c for c in prioritized if 40 <= c['priority_score'] < 70])
    low_priority = len([c for c in prioritized if c['priority_score'] < 40])
    
    print(f"   Alta (70+):   {high_priority:3d} canais")
    print(f"   Média (40-69): {medium_priority:3d} canais")
    print(f"   Baixa (<40):  {low_priority:3d} canais")
    
    # Salvar resultado
    if output_file:
        output_path = Path(__file__).parent.parent / output_file
        
        output_data = {
            'prioritized_at': datetime.now().isoformat(),
            'total_channels': len(prioritized),
            'channels': prioritized
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
        
        print()
        print(f"💾 Lista priorizada salva em: {output_path}")
    
    return prioritized


def get_top_n_channels(channels_file, n=50):
    """
    Retorna os top N canais por prioridade
    
    Args:
        channels_file: Arquivo com dados dos canais
        n: Número de canais a retornar
        
    Returns:
        Lista de IDs dos top N canais
    """
    prioritized = prioritize_channels(channels_file)
    return [c['channel_id'] for c in prioritized[:n]]


def main():
    """Função principal"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Prioriza canais por relevância')
    parser.add_argument('--input', type=str, required=True, help='Arquivo com canais classificados')
    parser.add_argument('--output', type=str, help='Arquivo de saída')
    parser.add_argument('--top', type=int, help='Mostrar apenas top N canais')
    
    args = parser.parse_args()
    
    prioritized = prioritize_channels(args.input, args.output)
    
    if args.top:
        print()
        print(f"\n📋 Top {args.top} IDs de Canais:")
        for channel in prioritized[:args.top]:
            print(f"   {channel['channel_id']}")


if __name__ == '__main__':
    main()
