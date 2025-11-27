#!/usr/bin/env python3
"""
Testa especificamente o OAuth2 secundário (persival.ai@gmail.com)
"""

import os
import sys
import pickle
from pathlib import Path
from dotenv import load_dotenv
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Carregar variáveis de ambiente
load_dotenv()

# Escopos OAuth necessários
SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']

def test_oauth2_secondary():
    """Testa OAuth2 secundário"""
    print("=" * 70)
    print("🔑 Testando OAuth2 Secundário (persival.ai@gmail.com)")
    print("=" * 70)
    print()
    
    # Carregar credenciais OAuth secundárias
    client_id = os.getenv('OAUTH_CLIENT_ID_2')
    client_secret = os.getenv('OAUTH_CLIENT_SECRET_2')
    
    if not client_id or not client_secret:
        print("❌ Erro: OAUTH_CLIENT_ID_2 e OAUTH_CLIENT_SECRET_2 não encontrados no .env")
        sys.exit(1)
    
    print(f"✅ Credenciais OAuth2 secundárias encontradas")
    print(f"   Client ID: {client_id[:20]}...")
    print()
    
    # Nome do arquivo de token
    token_file = "token_oauth_secondary.pickle"
    
    creds = None
    
    # Verificar se já existe token salvo
    if os.path.exists(token_file):
        print(f"📂 Token existente encontrado: {token_file}")
        try:
            with open(token_file, 'rb') as token:
                creds = pickle.load(token)
            print("✅ Token carregado com sucesso")
        except Exception as e:
            print(f"⚠️  Erro ao carregar token: {e}")
    
    # Se não há credenciais válidas, fazer login
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                print("🔄 Renovando token expirado...")
                creds.refresh(Request())
                print("✅ Token renovado com sucesso")
            except Exception as e:
                print(f"⚠️  Erro ao renovar token: {e}")
                creds = None
        
        if not creds:
            print()
            print("🔐 Iniciando autenticação OAuth 2.0...")
            print()
            print("⚠️  IMPORTANTE: Use a conta persival.ai@gmail.com")
            print()
            
            # Criar configuração do cliente OAuth
            client_config = {
                "installed": {
                    "client_id": client_id,
                    "client_secret": client_secret,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "redirect_uris": ["http://localhost"]
                }
            }
            
            try:
                flow = InstalledAppFlow.from_client_config(
                    client_config,
                    SCOPES
                )
                creds = flow.run_local_server(port=0)
                
                # Salvar credenciais
                with open(token_file, 'wb') as token:
                    pickle.dump(creds, token)
                
                print()
                print(f"✅ Autenticação concluída! Token salvo em {token_file}")
            
            except Exception as e:
                print(f"❌ Erro na autenticação OAuth: {e}")
                sys.exit(1)
    
    # Testar API
    print()
    print("🧪 Testando chamada de API...")
    
    try:
        youtube = build('youtube', 'v3', credentials=creds)
        
        # Fazer uma chamada simples
        request = youtube.search().list(
            part='snippet',
            q='AI',
            type='video',
            maxResults=1
        )
        response = request.execute()
        
        print("✅ Teste bem-sucedido!")
        print()
        print(f"   Vídeo encontrado: {response['items'][0]['snippet']['title']}")
        print(f"   Canal: {response['items'][0]['snippet']['channelTitle']}")
        
        # Verificar informações da conta autenticada
        print()
        print("📊 Testando acesso às inscrições (subscriptions)...")
        
        try:
            subs_request = youtube.subscriptions().list(
                part='snippet',
                mine=True,
                maxResults=1
            )
            subs_response = subs_request.execute()
            
            if subs_response.get('items'):
                print("✅ Acesso às inscrições confirmado!")
                print(f"   Primeira inscrição: {subs_response['items'][0]['snippet']['title']}")
            else:
                print("⚠️  Conta não tem inscrições ou acesso negado")
        
        except Exception as e:
            print(f"⚠️  Erro ao acessar inscrições: {e}")
        
        print()
        print("=" * 70)
        print("✅ OAuth2 secundário funcionando perfeitamente!")
        print("=" * 70)
        print()
        print(f"📝 Token salvo em: {token_file}")
        print("   Este token será reutilizado automaticamente")
        print()
    
    except Exception as e:
        print(f"❌ Erro ao testar API: {e}")
        sys.exit(1)


if __name__ == '__main__':
    test_oauth2_secondary()
