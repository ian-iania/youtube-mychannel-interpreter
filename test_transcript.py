#!/usr/bin/env python3
"""
Script de teste para verificar qual método de transcrição funciona
"""

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
import yt_dlp
import requests

video_id = "lfnJXlgpJT0"  # TOON Just Replaced JSON

print(f"🎬 Testando vídeo: {video_id}")
print("=" * 60)

# Método 1: youtube-transcript-api
print("\n📝 Método 1: youtube-transcript-api")
print("-" * 60)
try:
    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
    print(f"✅ Transcrições disponíveis:")
    
    for transcript in transcript_list:
        print(f"   - {transcript.language_code}: {transcript.language} (gerada: {transcript.is_generated})")
    
    # Tentar obter em português
    try:
        transcript = transcript_list.find_transcript(['pt', 'pt-BR'])
        data = transcript.fetch()
        print(f"\n✅ Transcrição PT obtida: {len(data)} segmentos")
        print(f"   Primeiros 3 segmentos:")
        for i, seg in enumerate(data[:3]):
            print(f"   {i+1}. [{seg['start']:.1f}s] {seg['text'][:50]}...")
    except NoTranscriptFound:
        print("❌ Transcrição PT não encontrada")
        
        # Tentar inglês
        try:
            transcript = transcript_list.find_transcript(['en'])
            data = transcript.fetch()
            print(f"\n✅ Transcrição EN obtida: {len(data)} segmentos")
            print(f"   Primeiros 3 segmentos:")
            for i, seg in enumerate(data[:3]):
                print(f"   {i+1}. [{seg['start']:.1f}s] {seg['text'][:50]}...")
        except NoTranscriptFound:
            print("❌ Transcrição EN não encontrada")
            
except TranscriptsDisabled:
    print("❌ Transcrições desabilitadas para este vídeo")
except Exception as e:
    print(f"❌ Erro: {e}")

# Método 2: yt-dlp
print("\n\n📝 Método 2: yt-dlp")
print("-" * 60)
try:
    video_url = f"https://www.youtube.com/watch?v={video_id}"
    
    ydl_opts = {
        'skip_download': True,
        'writesubtitles': True,
        'writeautomaticsub': True,
        'subtitleslangs': ['pt', 'pt-BR', 'en'],
        'quiet': True,
        'no_warnings': True,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=False)
        
        print("Legendas automáticas disponíveis:")
        if 'automatic_captions' in info and info['automatic_captions']:
            for lang in info['automatic_captions'].keys():
                print(f"   - {lang}")
        else:
            print("   Nenhuma")
            
        print("\nLegendas manuais disponíveis:")
        if 'subtitles' in info and info['subtitles']:
            for lang in info['subtitles'].keys():
                print(f"   - {lang}")
        else:
            print("   Nenhuma")
            
except Exception as e:
    print(f"❌ Erro: {e}")

print("\n" + "=" * 60)
print("✅ Teste concluído!")
