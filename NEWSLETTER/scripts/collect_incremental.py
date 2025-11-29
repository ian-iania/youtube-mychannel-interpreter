#!/usr/bin/env python3
"""
Coleta incremental de vídeos - busca apenas vídeos novos desde última atualização
Faz merge com dados existentes e remove duplicatas por video_id

Uso:
    python collect_incremental.py --since "2025-11-27T20:22:00"
    python collect_incremental.py --since "2025-11-27T20:22:00" --merge newsletters/2025-11-27_videos.json
    python collect_incremental.py --days 2  # Últimos 2 dias
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Adicionar diretório de scripts ao path
sys.path.insert(0, str(Path(__file__).parent))

from api_key_manager import APIKeyManager
from cache_manager import CacheManager

load_dotenv()


class IncrementalVideoCollector:
    """
    Coletor incremental de vídeos - busca apenas novos desde uma data específica
    """
    
    def __init__(self, since: datetime = None, days: int = None, use_cache: bool = True):
        """
        Args:
            since: Data/hora de início (buscar vídeos publicados após esta data)
            days: Alternativa - número de dias para trás
            use_cache: Se deve usar cache
        """
        if since:
            self.published_after = since
        elif days:
            self.published_after = datetime.now() - timedelta(days=days)
        else:
            self.published_after = datetime.now() - timedelta(days=2)
        
        self.use_cache = use_cache
        self.api_manager = APIKeyManager()
        self.cache = CacheManager() if use_cache else None
        self.youtube = self.api_manager.get_youtube_client()
        
        self.stats = {
            'channels_processed': 0,
            'videos_collected': 0,
            'videos_new': 0,
            'videos_duplicate': 0,
            'api_calls': 0,
            'cache_hits': 0,
            'errors': 0
        }
        
        # Set para rastrear video_ids já vistos
        self.seen_video_ids = set()
    
    def load_existing_videos(self, file_path: str) -> dict:
        """
        Carrega vídeos existentes de um arquivo para merge
        """
        path = Path(file_path)
        if not path.is_absolute():
            path = Path(__file__).parent.parent / file_path
        
        if not path.exists():
            print(f"⚠️  Arquivo não encontrado: {path}")
            return {'channels': {}}
        
        print(f"📂 Carregando dados existentes: {path}")
        
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Extrair todos os video_ids existentes
        for channel_id, channel_data in data.get('channels', {}).items():
            for video in channel_data.get('videos', []):
                self.seen_video_ids.add(video.get('video_id'))
        
        print(f"   ✅ {len(self.seen_video_ids)} vídeos existentes carregados")
        
        return data
    
    def get_channel_info(self, channel_id: str) -> dict:
        """Busca informações do canal"""
        if self.cache:
            cached = self.cache.get('channel_info', channel_id)
            if cached:
                self.stats['cache_hits'] += 1
                return cached
        
        def fetch_channel(youtube):
            request = youtube.channels().list(
                part='snippet,statistics',
                id=channel_id
            )
            response = request.execute()
            self.stats['api_calls'] += 1
            
            if response.get('items'):
                return response['items'][0]
            return None
        
        channel_info = self.api_manager.execute_with_fallback(fetch_channel)
        
        if channel_info and self.cache:
            self.cache.set('channel_info', channel_id, channel_info)
        
        return channel_info
    
    def get_channel_videos(self, channel_id: str, max_results: int = 50) -> list:
        """Busca vídeos do canal publicados após a data especificada"""
        published_after_str = self.published_after.strftime('%Y-%m-%dT%H:%M:%SZ')
        
        def fetch_videos(youtube):
            request = youtube.search().list(
                part='snippet',
                channelId=channel_id,
                publishedAfter=published_after_str,
                maxResults=max_results,
                order='date',
                type='video'
            )
            response = request.execute()
            self.stats['api_calls'] += 1
            
            return response.get('items', [])
        
        videos = self.api_manager.execute_with_fallback(fetch_videos)
        
        return videos if videos else []
    
    def get_videos_details_batch(self, video_ids: list) -> dict:
        """Busca detalhes de múltiplos vídeos em batch"""
        if not video_ids:
            return {}
        
        video_ids = video_ids[:50]  # Limite da API
        
        # Verificar cache
        cached_videos = {}
        uncached_ids = []
        
        if self.cache:
            for video_id in video_ids:
                cached = self.cache.get('video_details', video_id)
                if cached:
                    cached_videos[video_id] = cached
                    self.stats['cache_hits'] += 1
                else:
                    uncached_ids.append(video_id)
        else:
            uncached_ids = video_ids
        
        # Buscar não cacheados em batch
        if uncached_ids:
            def fetch_batch(youtube):
                request = youtube.videos().list(
                    part='snippet,statistics,contentDetails',
                    id=','.join(uncached_ids)
                )
                response = request.execute()
                self.stats['api_calls'] += 1
                
                return response.get('items', [])
            
            videos = self.api_manager.execute_with_fallback(fetch_batch)
            
            if videos:
                for video in videos:
                    video_id = video['id']
                    cached_videos[video_id] = video
                    
                    if self.cache:
                        self.cache.set('video_details', video_id, video)
        
        return cached_videos
    
    def _parse_duration(self, duration_str: str) -> float:
        """Converte duração ISO 8601 para minutos"""
        import re
        
        hours = minutes = seconds = 0
        
        h_match = re.search(r'(\d+)H', duration_str)
        if h_match:
            hours = int(h_match.group(1))
        
        m_match = re.search(r'(\d+)M', duration_str)
        if m_match:
            minutes = int(m_match.group(1))
        
        s_match = re.search(r'(\d+)S', duration_str)
        if s_match:
            seconds = int(s_match.group(1))
        
        return round(hours * 60 + minutes + seconds / 60, 1)
    
    def collect_channel_videos(self, channel_id: str, channel_meta: dict = None) -> dict:
        """Coleta vídeos novos de um canal"""
        try:
            # Buscar info do canal
            channel_info = self.get_channel_info(channel_id)
            
            if not channel_info:
                print(f"   ⚠️  Canal {channel_id} não encontrado")
                self.stats['errors'] += 1
                return None
            
            channel_title = channel_info['snippet']['title']
            print(f"\n📺 {channel_title}")
            
            # Buscar vídeos recentes
            videos = self.get_channel_videos(channel_id)
            
            if not videos:
                print(f"   ℹ️  Nenhum vídeo novo desde {self.published_after.strftime('%d/%m %H:%M')}")
                return {
                    'channel_info': channel_info,
                    'videos': []
                }
            
            # Filtrar duplicatas
            new_video_ids = []
            for v in videos:
                video_id = v['id']['videoId']
                if video_id not in self.seen_video_ids:
                    new_video_ids.append(video_id)
                    self.seen_video_ids.add(video_id)
                else:
                    self.stats['videos_duplicate'] += 1
            
            if not new_video_ids:
                print(f"   ℹ️  {len(videos)} vídeos encontrados, todos duplicados")
                return {
                    'channel_info': channel_info,
                    'videos': []
                }
            
            print(f"   📹 {len(new_video_ids)} vídeos novos (de {len(videos)} encontrados)")
            
            # Buscar detalhes em batch
            video_details = self.get_videos_details_batch(new_video_ids)
            
            # Processar vídeos
            processed_videos = []
            
            for video_id in new_video_ids:
                details = video_details.get(video_id)
                
                if not details:
                    continue
                
                snippet = details['snippet']
                statistics = details.get('statistics', {})
                content_details = details.get('contentDetails', {})
                
                duration_str = content_details.get('duration', 'PT0S')
                duration_minutes = self._parse_duration(duration_str)
                
                processed_video = {
                    'video_id': video_id,
                    'title': snippet['title'],
                    'description': snippet.get('description', ''),
                    'published_at': snippet['publishedAt'],
                    'thumbnail': snippet['thumbnails'].get('high', {}).get('url', ''),
                    'duration_minutes': duration_minutes,
                    'view_count': int(statistics.get('viewCount', 0)),
                    'like_count': int(statistics.get('likeCount', 0)),
                    'comment_count': int(statistics.get('commentCount', 0))
                }
                
                processed_videos.append(processed_video)
            
            self.stats['channels_processed'] += 1
            self.stats['videos_collected'] += len(processed_videos)
            self.stats['videos_new'] += len(processed_videos)
            
            print(f"   ✅ {len(processed_videos)} vídeos processados")
            
            return {
                'channel_info': channel_info,
                'videos': processed_videos
            }
        
        except Exception as e:
            print(f"   ❌ Erro ao processar canal: {e}")
            self.stats['errors'] += 1
            return None
    
    def collect_all_channels(self, channels_data: dict, output_file: str = None, merge_data: dict = None):
        """
        Coleta vídeos de todos os canais
        
        Args:
            channels_data: Dict com dados dos canais
            output_file: Arquivo de saída
            merge_data: Dados existentes para merge
        """
        print("=" * 70)
        print("📺 Coletor Incremental de Vídeos - IANIA AI News")
        print("=" * 70)
        print(f"\n🎯 Canais a processar: {len(channels_data)}")
        print(f"📅 Buscar vídeos desde: {self.published_after.strftime('%d/%m/%Y %H:%M')}")
        print(f"💾 Cache: {'Ativado' if self.use_cache else 'Desativado'}")
        
        if merge_data:
            existing_videos = sum(
                len(ch.get('videos', [])) 
                for ch in merge_data.get('channels', {}).values()
            )
            print(f"📂 Merge com: {existing_videos} vídeos existentes")
        
        print()
        
        # Iniciar com dados existentes ou vazio
        results = merge_data or {
            'collected_at': datetime.now().isoformat(),
            'channels': {}
        }
        
        # Atualizar timestamp
        results['collected_at'] = datetime.now().isoformat()
        results['incremental_since'] = self.published_after.isoformat()
        
        # Processar cada canal
        for i, (channel_id, channel_meta) in enumerate(channels_data.items(), 1):
            print(f"\n[{i}/{len(channels_data)}] Processando canal...")
            
            channel_data = self.collect_channel_videos(channel_id, channel_meta)
            
            if channel_data:
                if channel_id in results['channels']:
                    # Merge: adicionar novos vídeos aos existentes
                    existing_videos = results['channels'][channel_id].get('videos', [])
                    new_videos = channel_data.get('videos', [])
                    
                    # Combinar sem duplicatas
                    existing_ids = {v['video_id'] for v in existing_videos}
                    for video in new_videos:
                        if video['video_id'] not in existing_ids:
                            existing_videos.append(video)
                    
                    results['channels'][channel_id]['videos'] = existing_videos
                    results['channels'][channel_id]['channel_info'] = channel_data['channel_info']
                else:
                    results['channels'][channel_id] = channel_data
        
        # Salvar resultados
        if output_file:
            output_path = Path(__file__).parent.parent / 'newsletters' / output_file
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            
            print(f"\n💾 Resultados salvos em: {output_path}")
        
        # Estatísticas finais
        self._print_final_stats(results)
        
        return results
    
    def _print_final_stats(self, results: dict):
        """Imprime estatísticas finais"""
        print("\n" + "=" * 70)
        print("📊 Estatísticas Finais")
        print("=" * 70)
        
        total_videos = sum(
            len(ch.get('videos', [])) 
            for ch in results.get('channels', {}).values()
        )
        
        print(f"\n📺 Canais processados: {self.stats['channels_processed']}")
        print(f"🎬 Vídeos novos coletados: {self.stats['videos_new']}")
        print(f"🔄 Vídeos duplicados ignorados: {self.stats['videos_duplicate']}")
        print(f"📦 Total de vídeos no arquivo: {total_videos}")
        print(f"📡 Chamadas de API: {self.stats['api_calls']}")
        print(f"💾 Cache hits: {self.stats['cache_hits']}")
        print(f"❌ Erros: {self.stats['errors']}")
        
        # Status do API Manager
        print("\n🔑 Status das Credenciais:")
        api_status = self.api_manager.get_status()
        print(f"   Credencial atual: {api_status['current_key']}")
        print(f"   Credenciais restantes: {api_status['remaining_keys']}")
        
        if self.cache:
            self.cache.print_stats()


def main():
    parser = argparse.ArgumentParser(description='Coleta incremental de vídeos')
    parser.add_argument('--channels', type=str, default='newsletter_channels.json',
                        help='Arquivo com canais (padrão: newsletter_channels.json)')
    parser.add_argument('--since', type=str, 
                        help='Data/hora de início (formato: YYYY-MM-DDTHH:MM:SS)')
    parser.add_argument('--days', type=int, default=2,
                        help='Dias para buscar (padrão: 2, ignorado se --since for especificado)')
    parser.add_argument('--merge', type=str,
                        help='Arquivo existente para merge (ex: newsletters/2025-11-27_videos.json)')
    parser.add_argument('--output', type=str,
                        help='Arquivo de saída')
    parser.add_argument('--no-cache', action='store_true',
                        help='Desativar cache')
    
    args = parser.parse_args()
    
    # Determinar data de início
    if args.since:
        since = datetime.fromisoformat(args.since.replace('Z', ''))
    else:
        since = None
    
    # Carregar canais
    channels_file = Path(__file__).parent.parent / args.channels
    
    with open(channels_file, 'r') as f:
        data = json.load(f)
    
    # Extrair dados dos canais
    channels_list = data.get('channels', data) if isinstance(data, dict) else data
    
    if isinstance(channels_list, list):
        channels_data = {c['channel_id']: c for c in channels_list}
    else:
        channels_data = channels_list
    
    # Criar coletor
    collector = IncrementalVideoCollector(
        since=since,
        days=args.days if not since else None,
        use_cache=not args.no_cache
    )
    
    # Carregar dados existentes para merge
    merge_data = None
    if args.merge:
        merge_data = collector.load_existing_videos(args.merge)
    
    # Determinar arquivo de saída
    output_file = args.output or f"{datetime.now().strftime('%Y-%m-%d')}_videos.json"
    
    # Coletar vídeos
    collector.collect_all_channels(channels_data, output_file, merge_data)


if __name__ == '__main__':
    main()
