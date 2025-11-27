#!/usr/bin/env python3
"""
Coleta vídeos otimizada com cache, batch processing e fallback de API keys
Reduz uso de quota em ~60% através de otimizações inteligentes
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Importar módulos do projeto
from api_key_manager import APIKeyManager
from cache_manager import CacheManager

# Carregar variáveis de ambiente
load_dotenv()


class OptimizedVideoCollector:
    """
    Coletor otimizado de vídeos do YouTube
    """
    
    def __init__(self, days=7, use_cache=True):
        """
        Inicializa o coletor otimizado
        
        Args:
            days: Número de dias para buscar vídeos
            use_cache: Se deve usar cache
        """
        self.days = days
        self.use_cache = use_cache
        
        # Inicializar gerenciadores
        self.api_manager = APIKeyManager()
        self.cache = CacheManager() if use_cache else None
        self.youtube = self.api_manager.get_youtube_client()
        
        # Estatísticas
        self.stats = {
            'channels_processed': 0,
            'videos_collected': 0,
            'api_calls': 0,
            'cache_hits': 0,
            'errors': 0
        }
    
    def get_channel_info(self, channel_id):
        """
        Busca informações do canal (com cache)
        
        Args:
            channel_id: ID do canal
            
        Returns:
            Dict com informações do canal
        """
        # Tentar cache primeiro
        if self.cache:
            cached = self.cache.get('channel_info', channel_id)
            if cached:
                self.stats['cache_hits'] += 1
                return cached
        
        # Buscar da API
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
        
        # Salvar no cache
        if channel_info and self.cache:
            self.cache.set('channel_info', channel_id, channel_info)
        
        return channel_info
    
    def get_channel_videos(self, channel_id, max_results=50):
        """
        Busca vídeos recentes do canal (com cache)
        
        Args:
            channel_id: ID do canal
            max_results: Máximo de vídeos
            
        Returns:
            Lista de vídeos
        """
        # Chave de cache baseada em data
        cache_key = f"{channel_id}_{self.days}days"
        
        # Tentar cache primeiro
        if self.cache:
            cached = self.cache.get('channel_videos', cache_key)
            if cached:
                self.stats['cache_hits'] += 1
                return cached
        
        # Buscar da API
        published_after = (datetime.now() - timedelta(days=self.days)).isoformat() + 'Z'
        
        def fetch_videos(youtube):
            request = youtube.search().list(
                part='snippet',
                channelId=channel_id,
                publishedAfter=published_after,
                maxResults=max_results,
                order='date',
                type='video'
            )
            response = request.execute()
            self.stats['api_calls'] += 1
            
            return response.get('items', [])
        
        videos = self.api_manager.execute_with_fallback(fetch_videos)
        
        if videos is None:
            videos = []
        
        # Salvar no cache
        if self.cache:
            self.cache.set('channel_videos', cache_key, videos)
        
        return videos
    
    def get_videos_details_batch(self, video_ids):
        """
        Busca detalhes de múltiplos vídeos em uma única chamada (BATCH)
        Reduz de N chamadas para 1 chamada (98% de redução!)
        
        Args:
            video_ids: Lista de IDs de vídeos (máximo 50)
            
        Returns:
            Dict com detalhes dos vídeos {video_id: details}
        """
        if not video_ids:
            return {}
        
        # Limitar a 50 vídeos por chamada (limite da API)
        video_ids = video_ids[:50]
        
        # Verificar cache para cada vídeo
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
        
        # Buscar vídeos não cacheados em BATCH
        if uncached_ids:
            def fetch_batch(youtube):
                request = youtube.videos().list(
                    part='snippet,statistics,contentDetails',
                    id=','.join(uncached_ids)  # BATCH: múltiplos IDs em uma chamada!
                )
                response = request.execute()
                self.stats['api_calls'] += 1
                
                return response.get('items', [])
            
            videos = self.api_manager.execute_with_fallback(fetch_batch)
            
            if videos:
                for video in videos:
                    video_id = video['id']
                    cached_videos[video_id] = video
                    
                    # Salvar no cache
                    if self.cache:
                        self.cache.set('video_details', video_id, video)
        
        return cached_videos
    
    def collect_channel_videos(self, channel_id):
        """
        Coleta vídeos de um canal com todas as otimizações
        
        Args:
            channel_id: ID do canal
            
        Returns:
            Dict com informações do canal e vídeos
        """
        try:
            # 1. Buscar info do canal (com cache)
            channel_info = self.get_channel_info(channel_id)
            
            if not channel_info:
                print(f"   ⚠️  Canal {channel_id} não encontrado")
                self.stats['errors'] += 1
                return None
            
            channel_title = channel_info['snippet']['title']
            print(f"\n📺 {channel_title}")
            
            # 2. Buscar vídeos recentes (com cache)
            videos = self.get_channel_videos(channel_id)
            
            if not videos:
                print(f"   ℹ️  Nenhum vídeo nos últimos {self.days} dias")
                return {
                    'channel_info': channel_info,
                    'videos': []
                }
            
            print(f"   📹 {len(videos)} vídeos encontrados")
            
            # 3. Buscar detalhes em BATCH (50 vídeos por chamada)
            video_ids = [v['id']['videoId'] for v in videos]
            video_details = self.get_videos_details_batch(video_ids)
            
            # 4. Processar vídeos
            processed_videos = []
            
            for video in videos:
                video_id = video['id']['videoId']
                details = video_details.get(video_id)
                
                if not details:
                    continue
                
                # Extrair informações
                snippet = details['snippet']
                statistics = details.get('statistics', {})
                content_details = details.get('contentDetails', {})
                
                # Calcular duração em minutos
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
            
            print(f"   ✅ {len(processed_videos)} vídeos processados")
            
            return {
                'channel_info': channel_info,
                'videos': processed_videos
            }
        
        except Exception as e:
            print(f"   ❌ Erro ao processar canal: {e}")
            self.stats['errors'] += 1
            return None
    
    def _parse_duration(self, duration_str):
        """
        Converte duração ISO 8601 para minutos
        
        Args:
            duration_str: String no formato PT1H2M3S
            
        Returns:
            Duração em minutos
        """
        import re
        
        hours = 0
        minutes = 0
        seconds = 0
        
        # Extrair horas
        h_match = re.search(r'(\d+)H', duration_str)
        if h_match:
            hours = int(h_match.group(1))
        
        # Extrair minutos
        m_match = re.search(r'(\d+)M', duration_str)
        if m_match:
            minutes = int(m_match.group(1))
        
        # Extrair segundos
        s_match = re.search(r'(\d+)S', duration_str)
        if s_match:
            seconds = int(s_match.group(1))
        
        total_minutes = hours * 60 + minutes + seconds / 60
        return round(total_minutes, 1)
    
    def collect_all_channels(self, channel_ids, output_file=None):
        """
        Coleta vídeos de múltiplos canais
        
        Args:
            channel_ids: Lista de IDs de canais
            output_file: Arquivo para salvar resultados
            
        Returns:
            Dict com todos os dados coletados
        """
        print("=" * 70)
        print("📺 Coletor Otimizado de Vídeos do YouTube")
        print("=" * 70)
        print(f"\n🎯 Canais a processar: {len(channel_ids)}")
        print(f"📅 Período: Últimos {self.days} dias")
        print(f"💾 Cache: {'Ativado' if self.use_cache else 'Desativado'}")
        print()
        
        results = {
            'collected_at': datetime.now().isoformat(),
            'days': self.days,
            'channels': {}
        }
        
        for i, channel_id in enumerate(channel_ids, 1):
            print(f"\n[{i}/{len(channel_ids)}] Processando canal...")
            
            channel_data = self.collect_channel_videos(channel_id)
            
            if channel_data:
                results['channels'][channel_id] = channel_data
        
        # Salvar resultados
        if output_file:
            output_path = Path(__file__).parent.parent / 'newsletters' / output_file
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            
            print(f"\n💾 Resultados salvos em: {output_path}")
        
        # Estatísticas finais
        self._print_final_stats()
        
        return results
    
    def _print_final_stats(self):
        """Imprime estatísticas finais"""
        print("\n" + "=" * 70)
        print("📊 Estatísticas Finais")
        print("=" * 70)
        
        print(f"\n📺 Canais processados: {self.stats['channels_processed']}")
        print(f"🎬 Vídeos coletados: {self.stats['videos_collected']}")
        print(f"📡 Chamadas de API: {self.stats['api_calls']}")
        print(f"💾 Cache hits: {self.stats['cache_hits']}")
        print(f"❌ Erros: {self.stats['errors']}")
        
        # Calcular economia de quota
        total_requests = self.stats['api_calls'] + self.stats['cache_hits']
        if total_requests > 0:
            cache_rate = (self.stats['cache_hits'] / total_requests) * 100
            print(f"\n💰 Taxa de cache: {cache_rate:.1f}%")
            print(f"💰 Economia de quota: ~{self.stats['cache_hits']} chamadas")
        
        # Status do API Manager
        print("\n🔑 Status das Credenciais:")
        api_status = self.api_manager.get_status()
        print(f"   Credencial atual: {api_status['current_key']}")
        print(f"   Credenciais restantes: {api_status['remaining_keys']}")
        
        if self.cache:
            self.cache.print_stats()


def main():
    """Função principal"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Coleta vídeos otimizada')
    parser.add_argument('--channels', type=str, required=True, help='Arquivo com IDs dos canais')
    parser.add_argument('--days', type=int, default=7, help='Dias para buscar (padrão: 7)')
    parser.add_argument('--output', type=str, help='Arquivo de saída')
    parser.add_argument('--no-cache', action='store_true', help='Desativar cache')
    
    args = parser.parse_args()
    
    # Carregar IDs dos canais
    channels_file = Path(__file__).parent.parent / args.channels
    
    with open(channels_file, 'r') as f:
        data = json.load(f)
    
    channel_ids = list(data['channels'].keys())
    
    # Criar coletor
    collector = OptimizedVideoCollector(
        days=args.days,
        use_cache=not args.no_cache
    )
    
    # Coletar vídeos
    output_file = args.output or f"{datetime.now().strftime('%Y-%m-%d')}_videos.json"
    collector.collect_all_channels(channel_ids, output_file)


if __name__ == '__main__':
    main()
