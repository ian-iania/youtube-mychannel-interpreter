#!/usr/bin/env python3
"""
Script para categorizar vídeos automaticamente usando GPT-4o-mini
Lê: newsletters/2025-11-27_videos_full.json
Atualiza: ui/lib/real-data.ts com categorias corretas
"""

import json
import os
from typing import Dict, List, Any
from openai import OpenAI
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Inicializar cliente OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Categorias disponíveis
CATEGORIES = {
    "novos-modelos": {
        "name": "Novos Modelos e Atualizações",
        "description": "Lançamentos e atualizações de modelos de IA (GPT, Claude, Gemini, etc.)",
        "keywords": ["gpt", "claude", "gemini", "llama", "model", "release", "update", "version"]
    },
    "produtos-empresas": {
        "name": "Produtos e Atualizações de Empresas",
        "description": "Novos produtos, features e atualizações de empresas de IA",
        "keywords": ["product", "launch", "feature", "company", "startup", "announcement"]
    },
    "ides-agentes": {
        "name": "IDEs e Agentes de Código",
        "description": "Ferramentas de desenvolvimento com IA (Cursor, Copilot, Cline, etc.)",
        "keywords": ["cursor", "copilot", "cline", "ide", "coding", "agent", "aider", "windsurf"]
    },
    "automacao-workflows": {
        "name": "Automação e Workflows",
        "description": "Automação de processos, workflows e integrações com IA",
        "keywords": ["automation", "workflow", "zapier", "n8n", "make", "integration"]
    },
    "notebooklm": {
        "name": "NotebookLM",
        "description": "Tutoriais, casos de uso e novidades sobre NotebookLM",
        "keywords": ["notebooklm", "notebook lm", "google notebook"]
    },
    "arquitetura-design": {
        "name": "Arquitetura e Design",
        "description": "Arquitetura de sistemas, design patterns e melhores práticas com IA",
        "keywords": ["architecture", "design", "pattern", "rag", "vector", "embedding"]
    },
    "cursos-treinamentos": {
        "name": "Cursos e Treinamentos",
        "description": "Cursos, tutoriais e conteúdo educacional sobre IA",
        "keywords": ["course", "tutorial", "learn", "training", "guide", "how to"]
    },
    "ferramentas-dev": {
        "name": "Ferramentas de Desenvolvimento",
        "description": "Ferramentas e bibliotecas para desenvolvimento com IA",
        "keywords": ["tool", "library", "framework", "sdk", "api", "langchain", "llamaindex"]
    },
    "ferramentas-midia": {
        "name": "Ferramentas de Mídia",
        "description": "Ferramentas de geração de imagens, vídeos, áudio e música",
        "keywords": ["image", "video", "audio", "music", "generation", "midjourney", "stable diffusion", "sora"]
    },
    "noticias": {
        "name": "Notícias e Assuntos Gerais",
        "description": "Notícias, tendências e discussões gerais sobre IA",
        "keywords": ["news", "trend", "discussion", "debate", "opinion", "analysis"]
    },
    "outros": {
        "name": "Outros Temas",
        "description": "Outros temas relacionados a IA que não se encaixam nas categorias acima",
        "keywords": []
    }
}

def categorize_video_with_ai(title: str, channel: str) -> str:
    """
    Categoriza um vídeo usando GPT-4o-mini
    """
    
    # Criar prompt
    categories_list = "\n".join([
        f"- {cat_id}: {info['name']} - {info['description']}"
        for cat_id, info in CATEGORIES.items()
    ])
    
    prompt = f"""Você é um especialista em categorização de conteúdo sobre Inteligência Artificial.

Analise o título e canal do vídeo abaixo e escolha a categoria mais apropriada.

VÍDEO:
Título: {title}
Canal: {channel}

CATEGORIAS DISPONÍVEIS:
{categories_list}

INSTRUÇÕES:
1. Analise o título e canal cuidadosamente
2. Escolha APENAS UMA categoria que melhor se encaixa
3. Retorne APENAS o ID da categoria (ex: "novos-modelos")
4. Se não tiver certeza, use "outros"

RESPOSTA (apenas o ID da categoria):"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Você é um categorizador preciso e conciso. Responda apenas com o ID da categoria."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=20
        )
        
        category = response.choices[0].message.content.strip().lower()
        
        # Validar categoria
        if category in CATEGORIES:
            return category
        else:
            print(f"⚠️  Categoria inválida '{category}' para: {title[:50]}... → usando 'outros'")
            return "outros"
            
    except Exception as e:
        print(f"❌ Erro ao categorizar '{title[:50]}...': {e}")
        return "outros"

def categorize_videos_batch():
    """
    Categoriza todos os vídeos em batch
    """
    
    # Caminhos
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_file = os.path.join(base_dir, "newsletters", "2025-11-27_videos_full.json")
    output_file = os.path.join(base_dir, "newsletters", "2025-11-27_videos_categorized.json")
    
    print("📖 Lendo vídeos...")
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # Extrair todos os vídeos
    all_videos = []
    channels = data.get("channels", {})
    
    for channel_id, channel_data in channels.items():
        videos = channel_data.get("videos", [])
        channel_name = channel_data.get("channel_info", {}).get("snippet", {}).get("title", "Unknown")
        
        for video in videos:
            all_videos.append({
                "video": video,
                "channel_name": channel_name,
                "channel_id": channel_id
            })
    
    print(f"✅ Encontrados {len(all_videos)} vídeos")
    print(f"🤖 Categorizando com GPT-4o-mini...")
    
    # Categorizar cada vídeo
    categorized_videos = {cat_id: [] for cat_id in CATEGORIES.keys()}
    
    for i, item in enumerate(all_videos, 1):
        video = item["video"]
        channel_name = item["channel_name"]
        title = video.get("title", "")
        
        # Categorizar
        category = categorize_video_with_ai(title, channel_name)
        
        # Adicionar à categoria
        video_data = {
            **video,
            "channel": channel_name,
            "category": category
        }
        categorized_videos[category].append(video_data)
        
        # Progress
        print(f"[{i}/{len(all_videos)}] {category:20} | {title[:60]}")
    
    # Salvar resultado
    print(f"\n💾 Salvando em: {output_file}")
    
    output_data = {
        "collected_at": data.get("collected_at"),
        "categorized_at": __import__("datetime").datetime.now().isoformat(),
        "total_videos": len(all_videos),
        "categories": categorized_videos
    }
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    # Estatísticas
    print("\n📊 Estatísticas de Categorização:")
    for cat_id, videos in sorted(categorized_videos.items(), key=lambda x: len(x[1]), reverse=True):
        cat_name = CATEGORIES[cat_id]["name"]
        count = len(videos)
        percentage = (count / len(all_videos)) * 100
        print(f"  {cat_name:40} {count:3} vídeos ({percentage:5.1f}%)")
    
    print("\n✨ Categorização completa!")
    print(f"📁 Arquivo salvo: {output_file}")

if __name__ == "__main__":
    categorize_videos_batch()
