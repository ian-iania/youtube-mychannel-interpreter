#!/usr/bin/env python3
"""
Gerenciador de API Keys do YouTube com fallback automático
Suporta múltiplas API keys e OAuth2 como fallback
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Carregar variáveis de ambiente
load_dotenv()


class APIKeyManager:
    """
    Gerencia múltiplas API keys do YouTube com fallback automático
    """
    
    def __init__(self):
        """Inicializa o gerenciador com todas as keys disponíveis"""
        self.api_keys = self._load_api_keys()
        self.current_key_index = 0
        self.youtube = None
        self.quota_exceeded_keys = set()
        
        # Tentar inicializar com a primeira key
        self._initialize_youtube()
    
    def _load_api_keys(self):
        """
        Carrega todas as API keys disponíveis do .env
        
        Returns:
            Lista de API keys
        """
        keys = []
        
        # Key principal
        main_key = os.getenv('YOUTUBE_API_KEY')
        if main_key:
            keys.append({
                'key': main_key,
                'name': 'YOUTUBE_API_KEY',
                'type': 'api_key'
            })
        
        # Keys adicionais (YOUTUBE_API_KEY_2, YOUTUBE_API_KEY_3, etc)
        for i in range(2, 10):
            key = os.getenv(f'YOUTUBE_API_KEY_{i}')
            if key:
                keys.append({
                    'key': key,
                    'name': f'YOUTUBE_API_KEY_{i}',
                    'type': 'api_key'
                })
        
        # OAuth2 como fallback (se configurado)
        oauth_client_id = os.getenv('OAUTH_CLIENT_ID')
        oauth_client_secret = os.getenv('OAUTH_CLIENT_SECRET')
        
        if oauth_client_id and oauth_client_secret:
            keys.append({
                'client_id': oauth_client_id,
                'client_secret': oauth_client_secret,
                'name': 'OAUTH_PRIMARY',
                'type': 'oauth2'
            })
        
        # OAuth2 secundário
        oauth_client_id_2 = os.getenv('OAUTH_CLIENT_ID_2')
        oauth_client_secret_2 = os.getenv('OAUTH_CLIENT_SECRET_2')
        
        if oauth_client_id_2 and oauth_client_secret_2:
            keys.append({
                'client_id': oauth_client_id_2,
                'client_secret': oauth_client_secret_2,
                'name': 'OAUTH_SECONDARY',
                'type': 'oauth2'
            })
        
        if not keys:
            print("❌ Erro: Nenhuma API key ou OAuth configurado no .env")
            sys.exit(1)
        
        return keys
    
    def _initialize_youtube(self):
        """Inicializa o cliente do YouTube com a key atual"""
        if self.current_key_index >= len(self.api_keys):
            print("❌ Erro: Todas as API keys esgotadas")
            return False
        
        current = self.api_keys[self.current_key_index]
        
        try:
            if current['type'] == 'api_key':
                # Usar API key direta
                self.youtube = build('youtube', 'v3', developerKey=current['key'])
                print(f"✅ Usando {current['name']}")
                return True
            
            elif current['type'] == 'oauth2':
                # Usar OAuth2 (requer autenticação)
                print(f"⚠️  {current['name']} requer autenticação OAuth2")
                print("   Não implementado ainda neste script")
                # Pular para próxima key
                self.current_key_index += 1
                return self._initialize_youtube()
        
        except Exception as e:
            print(f"❌ Erro ao inicializar {current['name']}: {e}")
            self.current_key_index += 1
            return self._initialize_youtube()
    
    def get_youtube_client(self):
        """
        Retorna o cliente do YouTube atual
        
        Returns:
            Cliente do YouTube API
        """
        return self.youtube
    
    def handle_quota_error(self):
        """
        Trata erro de quota excedida, mudando para próxima key
        
        Returns:
            True se conseguiu mudar para outra key, False se esgotou todas
        """
        current = self.api_keys[self.current_key_index]
        self.quota_exceeded_keys.add(current['name'])
        
        print(f"\n⚠️  Quota excedida para {current['name']}")
        print(f"   Keys esgotadas: {len(self.quota_exceeded_keys)}/{len(self.api_keys)}")
        
        # Tentar próxima key
        self.current_key_index += 1
        
        if self.current_key_index >= len(self.api_keys):
            print("\n❌ TODAS as API keys esgotaram a quota!")
            print("   Aguarde até amanhã ou adicione mais keys no .env")
            return False
        
        # Inicializar com próxima key
        if self._initialize_youtube():
            print(f"✅ Mudou para {self.api_keys[self.current_key_index]['name']}")
            return True
        
        return False
    
    def execute_with_fallback(self, api_call_func, *args, **kwargs):
        """
        Executa uma chamada de API com fallback automático
        
        Args:
            api_call_func: Função que faz a chamada de API
            *args, **kwargs: Argumentos para a função
            
        Returns:
            Resultado da API ou None se todas as keys falharam
        """
        max_retries = len(self.api_keys)
        
        for attempt in range(max_retries):
            try:
                # Executar chamada de API
                result = api_call_func(self.youtube, *args, **kwargs)
                return result
            
            except HttpError as e:
                if e.resp.status == 403 and 'quotaExceeded' in str(e):
                    # Quota excedida, tentar próxima key
                    if not self.handle_quota_error():
                        return None
                    # Tentar novamente com nova key
                    continue
                else:
                    # Outro erro HTTP
                    raise
            
            except Exception as e:
                # Outro erro
                print(f"❌ Erro inesperado: {e}")
                raise
        
        return None
    
    def get_status(self):
        """
        Retorna status atual do gerenciador
        
        Returns:
            Dict com informações de status
        """
        current = self.api_keys[self.current_key_index] if self.current_key_index < len(self.api_keys) else None
        
        return {
            'total_keys': len(self.api_keys),
            'current_key': current['name'] if current else 'None',
            'current_index': self.current_key_index,
            'quota_exceeded': list(self.quota_exceeded_keys),
            'remaining_keys': len(self.api_keys) - len(self.quota_exceeded_keys)
        }


def test_api_keys():
    """Testa todas as API keys disponíveis"""
    print("=" * 70)
    print("🔑 Testando API Keys do YouTube")
    print("=" * 70)
    print()
    
    manager = APIKeyManager()
    
    print(f"📊 Keys encontradas: {len(manager.api_keys)}")
    for i, key_info in enumerate(manager.api_keys, 1):
        print(f"   {i}. {key_info['name']} ({key_info['type']})")
    
    print()
    
    # Testar chamada simples
    def test_call(youtube):
        """Chamada de teste simples"""
        request = youtube.search().list(
            part='snippet',
            q='AI',
            type='video',
            maxResults=1
        )
        return request.execute()
    
    print("🧪 Testando chamada de API...")
    result = manager.execute_with_fallback(test_call)
    
    if result:
        print("✅ Teste bem-sucedido!")
        print(f"   Vídeo encontrado: {result['items'][0]['snippet']['title']}")
    else:
        print("❌ Teste falhou")
    
    print()
    print("📊 Status final:")
    status = manager.get_status()
    for key, value in status.items():
        print(f"   {key}: {value}")


if __name__ == '__main__':
    test_api_keys()
