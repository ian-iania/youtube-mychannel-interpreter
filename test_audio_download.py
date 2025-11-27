#!/usr/bin/env python3
"""
Teste de download de áudio
"""

import yt_dlp
import os

video_id = "lfnJXlgpJT0"  # TOON Just Replaced JSON
video_url = f"https://www.youtube.com/watch?v={video_id}"
audio_file = f"temp_audio_{video_id}"

print(f"🎬 Testando download de áudio: {video_id}")
print("=" * 60)

# Configurações para baixar apenas áudio
ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': audio_file,
    'quiet': False,  # Mostrar mensagens
    'no_warnings': False,
    'extract_audio': True,
}

try:
    print("\n📥 Baixando áudio...")
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=True)
        
        print(f"\n✅ Download concluído!")
        print(f"   Extensão retornada: {info.get('ext', 'N/A')}")
        print(f"   Formato: {info.get('format', 'N/A')}")
        
        # Listar arquivos criados
        print(f"\n📁 Arquivos criados:")
        for file in os.listdir('.'):
            if file.startswith(f'temp_audio_{video_id}'):
                size = os.path.getsize(file) / 1024 / 1024  # MB
                print(f"   - {file} ({size:.2f} MB)")
        
        # Tentar encontrar o arquivo
        ext = info.get('ext', 'webm')
        expected_file = f"{audio_file}.{ext}"
        
        print(f"\n🔍 Procurando arquivo:")
        print(f"   Esperado: {expected_file}")
        print(f"   Existe? {os.path.exists(expected_file)}")
        
        # Tentar outras extensões
        for possible_ext in ['webm', 'm4a', 'mp3', 'opus', 'ogg']:
            possible_file = f"{audio_file}.{possible_ext}"
            if os.path.exists(possible_file):
                print(f"   ✅ Encontrado: {possible_file}")
                size = os.path.getsize(possible_file) / 1024 / 1024
                print(f"      Tamanho: {size:.2f} MB")
                
except Exception as e:
    print(f"\n❌ Erro: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
