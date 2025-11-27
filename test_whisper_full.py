#!/usr/bin/env python3
"""
Teste completo: Download + Whisper
"""

import yt_dlp
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

video_id = "lfnJXlgpJT0"  # TOON Just Replaced JSON

print(f"🎬 Teste completo: Download + Whisper")
print("=" * 60)

# Passo 1: Download de áudio
print("\n📥 Passo 1: Baixando áudio...")
video_url = f"https://www.youtube.com/watch?v={video_id}"
audio_file = f"temp_audio_{video_id}"

ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': audio_file,
    'quiet': True,
    'no_warnings': True,
}

try:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=True)
        
        # Obter extensão
        ext = info.get('ext', 'webm')
        
        # Verificar arquivo sem extensão primeiro e renomear
        if os.path.exists(audio_file):
            final_audio = f"{audio_file}.{ext}"
            os.rename(audio_file, final_audio)
            print(f"   ✅ Áudio baixado e renomeado: {final_audio}")
        else:
            # Tentar com extensão
            final_audio = f"{audio_file}.{ext}"
            if os.path.exists(final_audio):
                print(f"   ✅ Áudio baixado: {final_audio}")
            else:
                print(f"   ❌ Arquivo não encontrado!")
                exit(1)
        
        size = os.path.getsize(final_audio) / 1024 / 1024
        print(f"   📊 Tamanho: {size:.2f} MB")
        
        if size > 25:
            print(f"   ⚠️  Arquivo muito grande (limite: 25MB)")
            exit(1)
        
except Exception as e:
    print(f"   ❌ Erro: {e}")
    exit(1)

# Passo 2: Transcrição com Whisper
print("\n🤖 Passo 2: Transcrevendo com Whisper...")

try:
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("   ❌ OPENAI_API_KEY não configurada")
        exit(1)
    
    client = OpenAI(api_key=api_key)
    
    with open(final_audio, 'rb') as audio:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio,
            language="pt",
            response_format="verbose_json",
            timestamp_granularities=["segment"]
        )
    
    print(f"   ✅ Transcrição obtida!")
    print(f"   📝 Idioma: {transcript.language}")
    print(f"   ⏱️  Duração: {transcript.duration:.1f}s")
    
    if hasattr(transcript, 'segments') and transcript.segments:
        print(f"   📊 Segmentos: {len(transcript.segments)}")
        print(f"\n   📝 Primeiros 3 segmentos:")
        for i, seg in enumerate(transcript.segments[:3]):
            minutes = int(seg['start']) // 60
            seconds = int(seg['start']) % 60
            print(f"      [{minutes:02d}:{seconds:02d}] {seg['text'][:60]}...")
    else:
        print(f"   📝 Texto: {transcript.text[:200]}...")
    
    # Limpar arquivo
    os.remove(final_audio)
    print(f"\n   🗑️  Arquivo temporário removido")
    
    print(f"\n✅ SUCESSO! Tudo funcionando!")
    
except Exception as e:
    print(f"   ❌ Erro: {e}")
    import traceback
    traceback.print_exc()
    
    # Limpar arquivo em caso de erro
    try:
        if os.path.exists(final_audio):
            os.remove(final_audio)
    except:
        pass

print("\n" + "=" * 60)
