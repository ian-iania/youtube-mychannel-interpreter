#!/usr/bin/env python3
"""
Teste usando youtube-transcript-api
"""

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound

video_id = "lfnJXlgpJT0"  # TOON Just Replaced JSON

print(f"🎬 Testando com youtube-transcript-api: {video_id}")
print("=" * 60)

try:
    # Listar transcrições disponíveis
    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
    
    print("\n✅ Transcrições disponíveis:")
    for transcript in transcript_list:
        print(f"   - {transcript.language_code}: {transcript.language} (gerada: {transcript.is_generated})")
    
    # Tentar obter em português
    languages = ['pt', 'pt-BR', 'en']
    
    for lang in languages:
        try:
            print(f"\n🎯 Tentando: {lang}")
            transcript = transcript_list.find_transcript([lang])
            data = transcript.fetch()
            
            print(f"   ✅ SUCESSO! Obtidos {len(data)} segmentos")
            print(f"   📝 Primeiros 3 segmentos:")
            for i, seg in enumerate(data[:3]):
                minutes = int(seg['start']) // 60
                seconds = int(seg['start']) % 60
                print(f"      [{minutes:02d}:{seconds:02d}] {seg['text'][:60]}...")
            
            print(f"\n   🎉 Transcrição funcionando com {lang}!")
            break
        except NoTranscriptFound:
            print(f"   ❌ Não encontrado: {lang}")
            continue
    
    # Tentar legendas geradas
    if not data:
        print("\n🔄 Tentando legendas geradas automaticamente...")
        for lang in languages:
            try:
                transcript = transcript_list.find_generated_transcript([lang])
                data = transcript.fetch()
                
                print(f"   ✅ SUCESSO! Obtidos {len(data)} segmentos (gerada)")
                print(f"   🎉 Transcrição funcionando com {lang} (auto)!")
                break
            except NoTranscriptFound:
                continue
    
except TranscriptsDisabled:
    print("\n❌ Transcrições desabilitadas para este vídeo")
except Exception as e:
    print(f"\n❌ ERRO: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
