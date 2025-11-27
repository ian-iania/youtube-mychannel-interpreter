#!/usr/bin/env python3
"""
Processa arquivo channels_to_classify.txt e gera lista final de canais
"""

import json
from pathlib import Path
from datetime import datetime


def parse_classification_file(file_path):
    """
    Parse arquivo de classificação
    
    Args:
        file_path: Caminho do arquivo
        
    Returns:
        Lista de canais classificados
    """
    classified_channels = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            # Ignorar comentários e linhas vazias
            if line.strip().startswith('#') or line.strip() == '' or '=' in line:
                continue
            
            # Parse linha: "Nome do Canal | tipo # info"
            if '|' not in line:
                continue
            
            parts = line.split('|')
            if len(parts) < 2:
                continue
            
            channel_name = parts[0].strip()
            classification = parts[1].strip().split('#')[0].strip()
            
            # Se não tem classificação, pular (excluir)
            if not classification or classification == '':
                continue
            
            # Validar tipo
            if classification not in ['person', 'company', 'community']:
                print(f"⚠️  Linha {line_num}: Tipo inválido '{classification}' para '{channel_name}'")
                print(f"   Use: person | company | community")
                continue
            
            classified_channels.append({
                'channel_name': channel_name,
                'type': classification
            })
    
    return classified_channels


def match_with_subscriptions(classified, subscriptions_file):
    """
    Combina classificação com dados completos das inscrições
    
    Args:
        classified: Lista de canais classificados
        subscriptions_file: Arquivo all_subscriptions.json
        
    Returns:
        Lista de canais com dados completos
    """
    # Carregar dados completos
    with open(subscriptions_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    all_channels = data['channels']
    
    # Criar mapa por nome
    channels_map = {c['channel_title']: c for c in all_channels}
    
    # Combinar
    final_channels = []
    not_found = []
    
    for item in classified:
        channel_name = item['channel_name']
        channel_type = item['type']
        
        if channel_name in channels_map:
            channel_data = channels_map[channel_name].copy()
            channel_data['type'] = channel_type
            final_channels.append(channel_data)
        else:
            not_found.append(channel_name)
    
    if not_found:
        print(f"\n⚠️  {len(not_found)} canais não encontrados:")
        for name in not_found[:10]:
            print(f"   - {name}")
        if len(not_found) > 10:
            print(f"   ... e mais {len(not_found) - 10}")
    
    return final_channels


def save_newsletter_channels(channels, output_file='newsletter_channels.json'):
    """
    Salva lista final de canais para newsletter
    
    Args:
        channels: Lista de canais
        output_file: Nome do arquivo
    """
    output_path = Path(__file__).parent.parent / output_file
    
    # Estatísticas por tipo
    type_stats = {
        'person': len([c for c in channels if c['type'] == 'person']),
        'company': len([c for c in channels if c['type'] == 'company']),
        'community': len([c for c in channels if c['type'] == 'community'])
    }
    
    data = {
        'generated_at': datetime.now().isoformat(),
        'total_channels': len(channels),
        'type_distribution': type_stats,
        'channels': sorted(channels, key=lambda x: x['channel_title'])
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Canais salvos em: {output_path}")
    
    # Exibir estatísticas
    print(f"\n📊 Canais Selecionados para Newsletter:")
    print(f"   📺 Total: {len(channels)}")
    print(f"   👤 Pessoas: {type_stats['person']}")
    print(f"   🏢 Empresas: {type_stats['company']}")
    print(f"   👥 Comunidades: {type_stats['community']}")
    
    # Listar por tipo
    print(f"\n📋 Lista por Tipo:")
    
    for channel_type in ['person', 'company', 'community']:
        icon = {'person': '👤', 'company': '🏢', 'community': '👥'}[channel_type]
        type_channels = [c for c in channels if c['type'] == channel_type]
        
        if type_channels:
            print(f"\n{icon} {channel_type.upper()} ({len(type_channels)} canais):")
            for channel in sorted(type_channels, key=lambda x: int(x['subscriber_count']), reverse=True)[:10]:
                subs = int(channel['subscriber_count'])
                print(f"   • {channel['channel_title'][:50]:50s} - {subs:,} subs")
            
            if len(type_channels) > 10:
                print(f"   ... e mais {len(type_channels) - 10} canais")


def main():
    """Função principal"""
    print("=" * 70)
    print("📋 Channel Classification Processor")
    print("=" * 70)
    
    # Caminhos
    base_path = Path(__file__).parent.parent
    classification_file = base_path / 'channels_to_classify.txt'
    subscriptions_file = base_path / 'all_subscriptions.json'
    
    # Verificar arquivos
    if not classification_file.exists():
        print(f"❌ Erro: {classification_file} não encontrado")
        return
    
    if not subscriptions_file.exists():
        print(f"❌ Erro: {subscriptions_file} não encontrado")
        return
    
    # Parse classificação
    print(f"\n📂 Lendo classificações de {classification_file.name}...")
    classified = parse_classification_file(classification_file)
    print(f"✅ {len(classified)} canais classificados")
    
    # Combinar com dados completos
    print(f"\n🔗 Combinando com dados completos...")
    final_channels = match_with_subscriptions(classified, subscriptions_file)
    print(f"✅ {len(final_channels)} canais com dados completos")
    
    if not final_channels:
        print("❌ Nenhum canal selecionado")
        return
    
    # Salvar
    save_newsletter_channels(final_channels)
    
    print("\n✨ Processamento concluído!")
    print("\n📋 Próximo passo:")
    print("   Execute: python scripts/collect_videos.py")


if __name__ == '__main__':
    main()
