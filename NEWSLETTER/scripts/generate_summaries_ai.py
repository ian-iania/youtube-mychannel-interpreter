#!/usr/bin/env python3
"""
Script para gerar summaries e key points usando GPT-4o-mini
Lê: newsletters/2025-11-27_videos_categorized.json
Atualiza: newsletters/2025-11-27_videos_enriched.json
"""

import json
import os
from typing import Dict, List, Any
from openai import OpenAI
from dotenv import load_dotenv
import time

# Carregar variáveis de ambiente
load_dotenv()

# Inicializar cliente OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_summary_and_keypoints(title: str, channel: str, category: str) -> Dict[str, Any]:
    """
    Gera summary e key points para um vídeo usando GPT-4o-mini
    """
    
    prompt = f"""Você é um especialista em criar resumos concisos e informativos sobre conteúdo de tecnologia e IA.

VÍDEO:
Título: {title}
Canal: {channel}
Categoria: {category}

TAREFA:
1. Crie um resumo de 1-2 frases (máx 150 caracteres) explicando o tema principal do vídeo
2. Liste 3 pontos-chave (key points) que provavelmente são abordados no vídeo

FORMATO DE RESPOSTA (JSON):
{{
  "summary": "Resumo conciso aqui",
  "keyPoints": [
    "Ponto 1",
    "Ponto 2",
    "Ponto 3"
  ]
}}

INSTRUÇÕES:
- Summary: objetivo, claro, sem fluff
- Key points: específicos, acionáveis, relevantes
- Use linguagem técnica mas acessível
- Foque no valor para o leitor
- Seja conciso

RESPOSTA (apenas JSON):"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Você é um especialista em criar resumos técnicos concisos. Responda sempre em JSON válido."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=300,
            response_format={"type": "json_object"}
        )
        
        content = response.choices[0].message.content.strip()
        result = json.loads(content)
        
        # Validar estrutura
        if "summary" not in result or "keyPoints" not in result:
            print(f"⚠️  Resposta inválida para: {title[:50]}...")
            return {"summary": "", "keyPoints": []}
        
        # Limitar key points a 3
        result["keyPoints"] = result["keyPoints"][:3]
        
        return result
        
    except Exception as e:
        print(f"❌ Erro ao gerar summary para '{title[:50]}...': {e}")
        return {"summary": "", "keyPoints": []}

def enrich_videos_batch():
    """
    Enriquece todos os vídeos com summaries e key points
    """
    
    # Caminhos
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_file = os.path.join(base_dir, "newsletters", "2025-11-27_videos_categorized.json")
    output_file = os.path.join(base_dir, "newsletters", "2025-11-27_videos_enriched.json")
    
    print("📖 Lendo vídeos categorizados...")
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    categories = data.get("categories", {})
    total_videos = sum(len(videos) for videos in categories.values())
    
    print(f"✅ Encontrados {total_videos} vídeos em {len(categories)} categorias")
    print(f"🤖 Gerando summaries e key points com GPT-4o-mini...")
    print(f"⏱️  Estimativa: ~{total_videos * 2} segundos (~{total_videos * 2 / 60:.1f} minutos)")
    
    # Processar cada categoria
    enriched_categories = {}
    processed = 0
    start_time = time.time()
    
    for cat_id, videos in categories.items():
        enriched_videos = []
        
        for video in videos:
            processed += 1
            title = video.get("title", "")
            channel = video.get("channel", "")
            
            # Gerar summary e key points
            enrichment = generate_summary_and_keypoints(title, channel, cat_id)
            
            # Atualizar vídeo
            enriched_video = {
                **video,
                "summary": enrichment.get("summary", ""),
                "keyPoints": enrichment.get("keyPoints", [])
            }
            enriched_videos.append(enriched_video)
            
            # Progress
            elapsed = time.time() - start_time
            rate = processed / elapsed if elapsed > 0 else 0
            eta = (total_videos - processed) / rate if rate > 0 else 0
            
            print(f"[{processed}/{total_videos}] {cat_id:20} | ETA: {eta/60:.1f}min | {title[:50]}")
            
            # Rate limiting (evitar throttling)
            time.sleep(0.5)
        
        enriched_categories[cat_id] = enriched_videos
    
    # Salvar resultado
    print(f"\n💾 Salvando em: {output_file}")
    
    output_data = {
        "collected_at": data.get("collected_at"),
        "categorized_at": data.get("categorized_at"),
        "enriched_at": __import__("datetime").datetime.now().isoformat(),
        "total_videos": total_videos,
        "categories": enriched_categories
    }
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    # Estatísticas
    total_time = time.time() - start_time
    print(f"\n📊 Estatísticas:")
    print(f"  Total de vídeos: {total_videos}")
    print(f"  Tempo total: {total_time/60:.1f} minutos")
    print(f"  Taxa: {total_videos/total_time:.1f} vídeos/segundo")
    print(f"  Custo estimado: ~${total_videos * 0.0003:.2f}")
    
    # Verificar qualidade
    with_summary = sum(1 for videos in enriched_categories.values() for v in videos if v.get("summary"))
    with_keypoints = sum(1 for videos in enriched_categories.values() for v in videos if v.get("keyPoints"))
    
    print(f"\n✅ Qualidade:")
    print(f"  Com summary: {with_summary}/{total_videos} ({with_summary/total_videos*100:.1f}%)")
    print(f"  Com key points: {with_keypoints}/{total_videos} ({with_keypoints/total_videos*100:.1f}%)")
    
    print("\n✨ Enriquecimento completo!")
    print(f"📁 Arquivo salvo: {output_file}")

if __name__ == "__main__":
    enrich_videos_batch()
