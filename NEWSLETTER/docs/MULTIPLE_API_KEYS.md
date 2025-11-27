# 🔑 Sistema de Múltiplas API Keys

Guia completo para configurar e usar múltiplas API keys do YouTube com fallback automático.

---

## 📋 Visão Geral

O sistema permite usar **múltiplas API keys** do YouTube com **fallback automático** quando uma key atinge o limite de quota.

### **Benefícios:**
- ✅ **3x mais quota** (30,000 units/dia com 3 keys)
- ✅ **Fallback automático** quando quota excede
- ✅ **Zero downtime** - troca automática de keys
- ✅ **Fácil configuração** - apenas adicionar no .env

---

## 🚀 Como Funciona

### **1. Detecção Automática**
```python
# O sistema detecta automaticamente todas as keys no .env
YOUTUBE_API_KEY=key1          # Key principal
YOUTUBE_API_KEY_2=key2        # Key secundária
YOUTUBE_API_KEY_3=key3        # Key terciária
# ... até YOUTUBE_API_KEY_9
```

### **2. Fallback Automático**
```
Request → Key 1 → Quota OK? → Sucesso ✅
                ↓ Quota excedida
              Key 2 → Quota OK? → Sucesso ✅
                    ↓ Quota excedida
                  Key 3 → Sucesso ✅
```

### **3. Monitoramento**
```python
# Status em tempo real
{
    'total_keys': 3,
    'current_key': 'YOUTUBE_API_KEY_2',
    'quota_exceeded': ['YOUTUBE_API_KEY'],
    'remaining_keys': 2
}
```

---

## 🔧 Configuração

### **Passo 1: Criar API Keys Adicionais**

#### **No Google Cloud Console:**

1. **Acesse:** https://console.cloud.google.com/

2. **Crie um novo projeto** (ou use existente)
   - Nome: `YouTube Newsletter 2` (exemplo)
   - ID do projeto: auto-gerado

3. **Ative a YouTube Data API v3**
   ```
   APIs & Services → Library → YouTube Data API v3 → Enable
   ```

4. **Crie credenciais**
   ```
   APIs & Services → Credentials → Create Credentials → API Key
   ```

5. **Restrinja a key (recomendado)**
   ```
   - Application restrictions: None (ou HTTP referrers)
   - API restrictions: YouTube Data API v3
   ```

6. **Copie a API Key**
   ```
   AIzaSy... (exemplo)
   ```

### **Passo 2: Adicionar no .env**

```bash
# Editar .env
nano /Users/persivalballeste/Documents/LAB/.env

# Adicionar novas keys
YOUTUBE_API_KEY_2=AIzaSy...  # Segunda key
YOUTUBE_API_KEY_3=AIzaSy...  # Terceira key (opcional)
```

### **Passo 3: Testar**

```bash
cd NEWSLETTER
python3 scripts/api_key_manager.py
```

**Output esperado:**
```
✅ Usando YOUTUBE_API_KEY
📊 Keys encontradas: 3
   1. YOUTUBE_API_KEY (api_key)
   2. YOUTUBE_API_KEY_2 (api_key)
   3. YOUTUBE_API_KEY_3 (api_key)

🧪 Testando chamada de API...
✅ Teste bem-sucedido!
```

---

## 📊 Quota do YouTube API

### **Limites por Key:**
- **Quota diária:** 10,000 units
- **Reset:** Meia-noite PST (Pacific Standard Time)

### **Custos por Operação:**

| Operação | Custo (units) | Exemplo |
|----------|---------------|---------|
| `search.list` | 100 | Buscar vídeos |
| `videos.list` | 1 | Detalhes de vídeo |
| `channels.list` | 1 | Detalhes de canal |
| `playlistItems.list` | 1 | Vídeos de playlist |

### **Cálculo de Quota:**

**Coletar 103 canais:**
```
103 channels × 1 unit = 103 units (channel info)
103 channels × 100 units = 10,300 units (search videos)
~886 videos × 1 unit = 886 units (video details)

Total: ~11,289 units
```

**Com 1 key:** ❌ Não é possível (excede 10,000)  
**Com 2 keys:** ✅ Possível (20,000 units)  
**Com 3 keys:** ✅ Confortável (30,000 units)

---

## 💻 Uso no Código

### **Exemplo Básico:**

```python
from api_key_manager import APIKeyManager

# Inicializar gerenciador
manager = APIKeyManager()

# Obter cliente do YouTube
youtube = manager.get_youtube_client()

# Fazer chamadas normalmente
def get_channel_info(youtube, channel_id):
    request = youtube.channels().list(
        part='snippet,statistics',
        id=channel_id
    )
    return request.execute()

# Executar com fallback automático
result = manager.execute_with_fallback(get_channel_info, 'UC...')
```

### **Integração com collect_videos.py:**

```python
# No início do script
from api_key_manager import APIKeyManager

# Substituir:
youtube = build('youtube', 'v3', developerKey=api_key)

# Por:
manager = APIKeyManager()
youtube = manager.get_youtube_client()

# Usar execute_with_fallback para chamadas críticas
def collect_videos_safe(channel_id):
    return manager.execute_with_fallback(
        collect_videos_for_channel,
        channel_id
    )
```

---

## 🔍 Monitoramento

### **Status em Tempo Real:**

```python
status = manager.get_status()

print(f"Keys totais: {status['total_keys']}")
print(f"Key atual: {status['current_key']}")
print(f"Keys esgotadas: {len(status['quota_exceeded'])}")
print(f"Keys restantes: {status['remaining_keys']}")
```

### **Logs Automáticos:**

```
✅ Usando YOUTUBE_API_KEY
⚠️  Quota excedida para YOUTUBE_API_KEY
   Keys esgotadas: 1/3
✅ Mudou para YOUTUBE_API_KEY_2
```

---

## 🛠️ Troubleshooting

### **Problema: "Todas as API keys esgotadas"**

**Solução:**
1. Aguardar até meia-noite PST (reset de quota)
2. Adicionar mais API keys no .env
3. Otimizar chamadas de API (caching, batching)

### **Problema: "API key inválida"**

**Solução:**
1. Verificar se a key está correta no .env
2. Verificar se YouTube Data API v3 está ativada
3. Verificar restrições da API key

### **Problema: "OAuth2 não funciona"**

**Solução:**
- OAuth2 ainda não está implementado no fallback
- Use apenas API keys por enquanto
- OAuth2 será adicionado na Fase 3

---

## 📈 Estratégias de Otimização

### **1. Caching (50% redução)**
```python
# Cache channel info por 24h
# Cache videos por 6h
# Evita chamadas redundantes
```

### **2. Batch Processing (98% redução)**
```python
# Processar 50 vídeos por request
# Reduz de 100 calls para 2 calls
```

### **3. Prioritization**
```python
# Processar canais high-activity primeiro
# Garantir conteúdo mais relevante
```

### **4. Multiple Keys (3x quota)**
```python
# 3 keys = 30,000 units/dia
# Suficiente para 103 canais
```

---

## 🎯 Recomendações

### **Para 103 Canais:**

**Mínimo:** 2 API keys (20,000 units)  
**Recomendado:** 3 API keys (30,000 units)  
**Ideal:** 3 keys + otimizações (caching, batching)

### **Configuração Ideal:**

```bash
# .env
YOUTUBE_API_KEY=key1          # Projeto principal
YOUTUBE_API_KEY_2=key2        # Projeto secundário
YOUTUBE_API_KEY_3=key3        # Projeto terciário (backup)
```

**Resultado:**
- ✅ 30,000 units/dia
- ✅ Fallback automático
- ✅ Zero downtime
- ✅ Processa 103 canais confortavelmente

---

## 📝 Checklist de Setup

- [ ] Criar 2-3 projetos no Google Cloud
- [ ] Ativar YouTube Data API v3 em cada projeto
- [ ] Criar API keys
- [ ] Adicionar keys no .env
- [ ] Testar com `api_key_manager.py`
- [ ] Verificar fallback automático
- [ ] Integrar com `collect_videos.py`
- [ ] Monitorar uso de quota

---

## 🔗 Links Úteis

- **Google Cloud Console:** https://console.cloud.google.com/
- **YouTube API Docs:** https://developers.google.com/youtube/v3
- **Quota Calculator:** https://developers.google.com/youtube/v3/determine_quota_cost
- **API Key Best Practices:** https://cloud.google.com/docs/authentication/api-keys

---

*Última atualização: 27 de Novembro de 2025*
