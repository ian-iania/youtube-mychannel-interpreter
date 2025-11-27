#!/usr/bin/env python3
"""
Teste simples de transcrição
"""

import yt_dlp
import requests

video_id = "lfnJXlgpJT0"  # TOON Just Replaced JSON
video_url = f"https://www.youtube.com/watch?v={video_id}"

print(f"🎬 Testando transcrição para: {video_id}")
print("=" * 60)

try:
    ydl_opts = {
        'skip_download': True,
        'writesubtitles': True,
        'writeautomaticsub': True,
        'subtitleslangs': ['pt', 'pt-PT', 'pt-BR', 'en'],
        'quiet': False,  # Mostrar mensagens
        'no_warnings': False,
    }
    
    print("\n📥 Extraindo informações do vídeo...")
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=False)
        
        print(f"\n✅ Título: {info.get('title', 'N/A')}")
        print(f"✅ Duração: {info.get('duration', 0)} segundos")
        
        # Verificar legendas automáticas
        if 'automatic_captions' in info and info['automatic_captions']:
            print(f"\n✅ Legendas automáticas disponíveis: {len(info['automatic_captions'])} idiomas")
            
            # Tentar português
            for lang in ['pt', 'pt-PT', 'pt-BR']:
                if lang in info['automatic_captions']:
                    print(f"\n🎯 Encontrado: {lang}")
                    subs = info['automatic_captions'][lang]
                    
                    for sub in subs:
                        if sub.get('ext') == 'json3':
                            print(f"   📄 Formato: {sub.get('ext')}")
                            print(f"   🔗 URL: {sub['url'][:100]}...")
                            
                            print(f"\n   📥 Baixando transcrição...")
                            response = requests.get(sub['url'])
                            
                            if response.status_code == 200:
                                data = response.json()
                                
                                # Extrair texto
                                transcript = []
                                if 'events' in data:
                                    for event in data['events']:
                                        if 'segs' in event:
                                            text = ''.join([seg.get('utf8', '') for seg in event['segs']])
                                            if text.strip():
                                                start = event.get('tStartMs', 0) / 1000
                                                transcript.append({
                                                    'start': start,
                                                    'text': text.strip()
                                                })
                                
                                if transcript:
                                    print(f"\n   ✅ Transcrição obtida: {len(transcript)} segmentos")
                                    print(f"\n   📝 Primeiros 3 segmentos:")
                                    for i, seg in enumerate(transcript[:3]):
                                        minutes = int(seg['start']) // 60
                                        seconds = int(seg['start']) % 60
                                        print(f"      [{minutes:02d}:{seconds:02d}] {seg['text'][:60]}...")
                                    
                                    print(f"\n   🎉 SUCESSO! Transcrição funcionando!")
                                    break
                                else:
                                    print(f"   ❌ Nenhum segmento extraído")
                            else:
                                print(f"   ❌ Erro HTTP: {response.status_code}")
                            break
                    break
            else:
                print("\n❌ Português não encontrado, tentando inglês...")
                
                if 'en' in info['automatic_captions']:
                    print(f"\n🎯 Encontrado: en")
                    subs = info['automatic_captions']['en']
                    
                    for sub in subs:
                        if sub.get('ext') == 'json3':
                            print(f"   📄 Formato: {sub.get('ext')}")
                            response = requests.get(sub['url'])
                            
                            if response.status_code == 200:
                                data = response.json()
                                transcript = []
                                
                                if 'events' in data:
                                    for event in data['events']:
                                        if 'segs' in event:
                                            text = ''.join([seg.get('utf8', '') for seg in event['segs']])
                                            if text.strip():
                                                start = event.get('tStartMs', 0) / 1000
                                                transcript.append({
                                                    'start': start,
                                                    'text': text.strip()
                                                })
                                
                                if transcript:
                                    print(f"\n   ✅ Transcrição EN obtida: {len(transcript)} segmentos")
                                    print(f"\n   🎉 SUCESSO!")
                                    break
                            break
        else:
            print("\n❌ Nenhuma legenda automática disponível")
            
except Exception as e:
    print(f"\n❌ ERRO: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
