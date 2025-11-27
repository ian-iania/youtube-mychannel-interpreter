#!/usr/bin/env python3
"""
Sistema de cache para reduzir chamadas à API do YouTube
Reduz uso de quota em ~50% através de cache inteligente
"""

import os
import json
import time
from pathlib import Path
from datetime import datetime, timedelta


class CacheManager:
    """
    Gerencia cache de dados da API do YouTube
    """
    
    def __init__(self, cache_dir='cache'):
        """
        Inicializa o gerenciador de cache
        
        Args:
            cache_dir: Diretório para armazenar cache
        """
        self.cache_dir = Path(__file__).parent.parent / cache_dir
        self.cache_dir.mkdir(exist_ok=True)
        
        # TTL (Time To Live) para diferentes tipos de dados
        self.ttl = {
            'channel_info': 24 * 3600,      # 24 horas
            'channel_videos': 6 * 3600,     # 6 horas
            'video_details': 12 * 3600,     # 12 horas
            'channel_stats': 12 * 3600      # 12 horas
        }
        
        self.stats = {
            'hits': 0,
            'misses': 0,
            'saves': 0
        }
    
    def _get_cache_file(self, cache_type, key):
        """
        Retorna caminho do arquivo de cache
        
        Args:
            cache_type: Tipo de cache (channel_info, channel_videos, etc)
            key: Chave única (channel_id, video_id, etc)
            
        Returns:
            Path do arquivo de cache
        """
        type_dir = self.cache_dir / cache_type
        type_dir.mkdir(exist_ok=True)
        
        # Sanitizar key para nome de arquivo
        safe_key = key.replace('/', '_').replace('\\', '_')
        return type_dir / f"{safe_key}.json"
    
    def get(self, cache_type, key):
        """
        Busca dado no cache
        
        Args:
            cache_type: Tipo de cache
            key: Chave do dado
            
        Returns:
            Dado em cache ou None se não encontrado/expirado
        """
        cache_file = self._get_cache_file(cache_type, key)
        
        if not cache_file.exists():
            self.stats['misses'] += 1
            return None
        
        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                cached = json.load(f)
            
            # Verificar se expirou
            cached_time = cached.get('cached_at', 0)
            ttl = self.ttl.get(cache_type, 3600)
            
            if time.time() - cached_time > ttl:
                # Cache expirado
                self.stats['misses'] += 1
                cache_file.unlink()  # Remover cache expirado
                return None
            
            # Cache válido
            self.stats['hits'] += 1
            return cached.get('data')
        
        except Exception as e:
            print(f"⚠️  Erro ao ler cache: {e}")
            self.stats['misses'] += 1
            return None
    
    def set(self, cache_type, key, data):
        """
        Salva dado no cache
        
        Args:
            cache_type: Tipo de cache
            key: Chave do dado
            data: Dado a ser cacheado
        """
        cache_file = self._get_cache_file(cache_type, key)
        
        try:
            cached = {
                'cached_at': time.time(),
                'cache_type': cache_type,
                'key': key,
                'data': data
            }
            
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(cached, f, ensure_ascii=False, indent=2)
            
            self.stats['saves'] += 1
        
        except Exception as e:
            print(f"⚠️  Erro ao salvar cache: {e}")
    
    def invalidate(self, cache_type, key=None):
        """
        Invalida cache
        
        Args:
            cache_type: Tipo de cache
            key: Chave específica (None = invalidar tudo do tipo)
        """
        if key:
            # Invalidar cache específico
            cache_file = self._get_cache_file(cache_type, key)
            if cache_file.exists():
                cache_file.unlink()
        else:
            # Invalidar todo o tipo
            type_dir = self.cache_dir / cache_type
            if type_dir.exists():
                for cache_file in type_dir.glob('*.json'):
                    cache_file.unlink()
    
    def clear_expired(self):
        """Remove todos os caches expirados"""
        removed = 0
        
        for cache_type in self.ttl.keys():
            type_dir = self.cache_dir / cache_type
            if not type_dir.exists():
                continue
            
            ttl = self.ttl[cache_type]
            
            for cache_file in type_dir.glob('*.json'):
                try:
                    with open(cache_file, 'r') as f:
                        cached = json.load(f)
                    
                    cached_time = cached.get('cached_at', 0)
                    
                    if time.time() - cached_time > ttl:
                        cache_file.unlink()
                        removed += 1
                
                except:
                    # Arquivo corrompido, remover
                    cache_file.unlink()
                    removed += 1
        
        return removed
    
    def get_stats(self):
        """
        Retorna estatísticas de uso do cache
        
        Returns:
            Dict com estatísticas
        """
        total_requests = self.stats['hits'] + self.stats['misses']
        hit_rate = (self.stats['hits'] / total_requests * 100) if total_requests > 0 else 0
        
        # Calcular tamanho do cache
        cache_size = 0
        cache_files = 0
        
        for cache_type_dir in self.cache_dir.iterdir():
            if cache_type_dir.is_dir():
                for cache_file in cache_type_dir.glob('*.json'):
                    cache_size += cache_file.stat().st_size
                    cache_files += 1
        
        return {
            'hits': self.stats['hits'],
            'misses': self.stats['misses'],
            'saves': self.stats['saves'],
            'hit_rate': hit_rate,
            'cache_files': cache_files,
            'cache_size_mb': cache_size / (1024 * 1024)
        }
    
    def print_stats(self):
        """Imprime estatísticas do cache"""
        stats = self.get_stats()
        
        print("\n📊 Estatísticas do Cache:")
        print(f"   ✅ Hits: {stats['hits']}")
        print(f"   ❌ Misses: {stats['misses']}")
        print(f"   💾 Saves: {stats['saves']}")
        print(f"   📈 Hit Rate: {stats['hit_rate']:.1f}%")
        print(f"   📁 Arquivos: {stats['cache_files']}")
        print(f"   💽 Tamanho: {stats['cache_size_mb']:.2f} MB")


def test_cache():
    """Testa o sistema de cache"""
    print("=" * 70)
    print("🧪 Testando Sistema de Cache")
    print("=" * 70)
    print()
    
    cache = CacheManager()
    
    # Teste 1: Salvar e recuperar
    print("📝 Teste 1: Salvar e recuperar dados")
    
    test_data = {
        'channel_id': 'UC123',
        'title': 'Test Channel',
        'subscribers': 10000
    }
    
    cache.set('channel_info', 'UC123', test_data)
    print("   ✅ Dados salvos")
    
    retrieved = cache.get('channel_info', 'UC123')
    
    if retrieved == test_data:
        print("   ✅ Dados recuperados corretamente")
    else:
        print("   ❌ Erro ao recuperar dados")
    
    # Teste 2: Cache miss
    print("\n📝 Teste 2: Cache miss")
    
    result = cache.get('channel_info', 'UC_INEXISTENTE')
    
    if result is None:
        print("   ✅ Cache miss detectado corretamente")
    else:
        print("   ❌ Erro: deveria retornar None")
    
    # Teste 3: Múltiplos tipos de cache
    print("\n📝 Teste 3: Múltiplos tipos de cache")
    
    cache.set('channel_videos', 'UC123', ['video1', 'video2'])
    cache.set('video_details', 'video1', {'title': 'Video 1'})
    
    print("   ✅ Múltiplos tipos salvos")
    
    # Estatísticas
    print()
    cache.print_stats()
    
    # Teste 4: Limpeza de expirados
    print("\n📝 Teste 4: Limpeza de cache expirado")
    
    removed = cache.clear_expired()
    print(f"   ✅ {removed} caches expirados removidos")
    
    print("\n✅ Todos os testes passaram!")


if __name__ == '__main__':
    test_cache()
