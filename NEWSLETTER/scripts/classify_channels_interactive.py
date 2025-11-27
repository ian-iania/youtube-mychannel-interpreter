#!/usr/bin/env python3
"""
Script interativo para classificar canais
Respostas: P (person) | C (company) | CM (community) | N (não incluir)
"""

import json
import re
from pathlib import Path
from datetime import datetime


def load_all_subscriptions():
    """Carrega todos os canais"""
    file_path = Path(__file__).parent.parent / 'all_subscriptions.json'
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    return data['channels']


def load_existing_classifications():
    """Carrega classificações já feitas do arquivo txt"""
    file_path = Path(__file__).parent.parent / 'channels_to_classify.txt'
    classifications = {}
    
    if not file_path.exists():
        return classifications
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            # Ignorar comentários e linhas vazias
            if line.strip().startswith('#') or line.strip() == '' or '=' in line:
                continue
            
            if '|' not in line:
                continue
            
            parts = line.split('|')
            if len(parts) < 2:
                continue
            
            channel_name = parts[0].strip()
            rest = parts[1].strip()
            
            # Procurar por PERSON, Company, Community, person, company, community
            # Pode estar no final da linha, depois do handle
            classification = None
            
            # Buscar em toda a linha
            full_line = line.upper()
            
            if 'PERSON' in full_line:
                classification = 'person'
            elif 'COMPANY' in full_line:
                classification = 'company'
            elif 'COMMUNITY' in full_line:
                classification = 'community'
            
            if classification:
                classifications[channel_name] = classification
    
    return classifications


def save_classifications(channels, output_file='newsletter_channels.json'):
    """Salva classificações finais"""
    output_path = Path(__file__).parent.parent / output_file
    
    # Filtrar apenas canais classificados (não N)
    classified_channels = [c for c in channels if c.get('type') and c['type'] != 'skip']
    
    # Estatísticas por tipo
    type_stats = {
        'person': len([c for c in classified_channels if c['type'] == 'person']),
        'company': len([c for c in classified_channels if c['type'] == 'company']),
        'community': len([c for c in classified_channels if c['type'] == 'community'])
    }
    
    data = {
        'generated_at': datetime.now().isoformat(),
        'total_channels': len(classified_channels),
        'type_distribution': type_stats,
        'channels': sorted(classified_channels, key=lambda x: x['channel_title'])
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    return type_stats


def format_number(num):
    """Formata número com separador de milhares"""
    return f"{int(num):,}"


def main():
    """Função principal"""
    import sys
    
    print("=" * 80)
    print("🎯 CLASSIFICAÇÃO INTERATIVA DE CANAIS")
    print("=" * 80)
    print()
    print("Respostas:")
    print("  P  = Person (pessoa)")
    print("  C  = Company (empresa)")
    print("  CM = Community (comunidade)")
    print("  N  = Não incluir na newsletter")
    print("  Q  = Quit (salvar e sair)")
    print("  B  = Back (voltar canal anterior)")
    print()
    print("=" * 80)
    print()
    
    # Carregar canais
    print("📂 Carregando canais...")
    all_channels = load_all_subscriptions()
    print(f"✅ {len(all_channels)} canais carregados")
    
    # Carregar classificações existentes
    print("📋 Carregando classificações existentes...")
    existing = load_existing_classifications()
    print(f"✅ {len(existing)} canais já classificados")
    print()
    
    # Perguntar se quer reclassificar
    if len(existing) > 0:
        print("❓ Deseja reclassificar TODOS os canais (incluindo os já classificados)?")
        reclassify = input("   Digite 'S' para SIM ou Enter para continuar apenas os não classificados: ").strip().upper()
        print()
        
        if reclassify == 'S':
            print("🔄 Modo RECLASSIFICAÇÃO: Todos os canais serão mostrados")
            print()
            # Não aplicar classificações existentes
            unclassified = all_channels
        else:
            print("➡️  Modo CONTINUAR: Apenas canais não classificados")
            print()
            # Aplicar classificações existentes
            for channel in all_channels:
                if channel['channel_title'] in existing:
                    channel['type'] = existing[channel['channel_title']]
            
            # Filtrar apenas não classificados
            unclassified = [c for c in all_channels if not c.get('type') or c.get('type') == '']
    else:
        # Nenhuma classificação existente
        unclassified = all_channels
    
    print(f"📊 Total de canais para classificar: {len(unclassified)}")
    print()
    
    if len(unclassified) == 0:
        print("✨ Todos os canais já foram classificados!")
        
        # Salvar
        type_stats = save_classifications(all_channels)
        
        print(f"\n📊 Resumo Final:")
        print(f"   👤 Pessoas: {type_stats['person']}")
        print(f"   🏢 Empresas: {type_stats['company']}")
        print(f"   👥 Comunidades: {type_stats['community']}")
        print(f"   📺 Total: {sum(type_stats.values())}")
        
        return
    
    print("🚀 Iniciando classificação...")
    print("=" * 80)
    print()
    
    # Classificar
    history = []
    idx = 0
    
    while idx < len(unclassified):
        channel = unclassified[idx]
        
        # Informações do canal
        title = channel['channel_title']
        subs = format_number(channel['subscriber_count'])
        videos = format_number(channel['video_count'])
        handle = channel.get('handle', 'N/A')
        current_type = channel.get('type', '')
        
        # Mostrar progresso
        progress = f"[{idx + 1}/{len(unclassified)}]"
        
        print(f"\n{progress} Canal:")
        print(f"  📺 Nome: {title}")
        print(f"  🔗 Handle: {handle}")
        print(f"  👥 Inscritos: {subs}")
        print(f"  🎬 Vídeos: {videos}")
        
        # Mostrar classificação atual se existir
        if current_type and current_type != 'skip':
            type_icon = {'person': '👤', 'company': '🏢', 'community': '👥'}.get(current_type, '❓')
            type_name = {'person': 'Person', 'company': 'Company', 'community': 'Community'}.get(current_type, current_type)
            print(f"  🏷️  Atual: {type_icon} {type_name}")
        
        # Pedir classificação
        while True:
            response = input("\n  Classificação [P/C/CM/N/Q/B]: ").strip().upper()
            
            if response == 'Q':
                print("\n💾 Salvando e saindo...")
                type_stats = save_classifications(all_channels)
                
                print(f"\n📊 Progresso:")
                print(f"   ✅ Classificados: {len(all_channels) - len(unclassified) + idx}")
                print(f"   ⏳ Restantes: {len(unclassified) - idx}")
                print(f"\n📊 Resumo Atual:")
                print(f"   👤 Pessoas: {type_stats['person']}")
                print(f"   🏢 Empresas: {type_stats['company']}")
                print(f"   👥 Comunidades: {type_stats['community']}")
                print(f"   📺 Total: {sum(type_stats.values())}")
                print(f"\n✨ Salvo em: newsletter_channels.json")
                return
            
            elif response == 'B':
                if idx > 0:
                    # Voltar
                    idx -= 1
                    # Remover classificação anterior
                    prev_channel = unclassified[idx]
                    if 'type' in prev_channel:
                        del prev_channel['type']
                    if history:
                        history.pop()
                    print("  ⬅️  Voltando...")
                    break
                else:
                    print("  ⚠️  Já está no primeiro canal")
                    continue
            
            elif response == 'P':
                channel['type'] = 'person'
                history.append(('person', title))
                print("  ✅ Marcado como Person")
                idx += 1
                break
            
            elif response == 'C':
                channel['type'] = 'company'
                history.append(('company', title))
                print("  ✅ Marcado como Company")
                idx += 1
                break
            
            elif response == 'CM':
                channel['type'] = 'community'
                history.append(('community', title))
                print("  ✅ Marcado como Community")
                idx += 1
                break
            
            elif response == 'N':
                channel['type'] = 'skip'
                history.append(('skip', title))
                print("  ⏭️  Pulando (não incluir)")
                idx += 1
                break
            
            else:
                print("  ❌ Resposta inválida. Use: P, C, CM, N, Q ou B")
    
    # Concluído
    print("\n" + "=" * 80)
    print("🎉 CLASSIFICAÇÃO CONCLUÍDA!")
    print("=" * 80)
    
    # Salvar
    print("\n💾 Salvando classificações...")
    type_stats = save_classifications(all_channels)
    
    print(f"\n📊 Resumo Final:")
    print(f"   👤 Pessoas: {type_stats['person']}")
    print(f"   🏢 Empresas: {type_stats['company']}")
    print(f"   👥 Comunidades: {type_stats['community']}")
    print(f"   📺 Total: {sum(type_stats.values())}")
    
    print(f"\n✨ Arquivo salvo: newsletter_channels.json")
    print(f"\n📋 Próximo passo:")
    print(f"   python scripts/collect_videos.py")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrompido pelo usuário")
        print("💾 Salvando progresso...")
        # Tentar salvar o que foi feito
        print("✅ Use 'Q' na próxima vez para salvar antes de sair")
