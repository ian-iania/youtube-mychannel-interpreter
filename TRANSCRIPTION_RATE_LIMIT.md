# ⏳ Problema de Rate Limit nas Transcrições

## 🚨 Problema Atual

O YouTube está bloqueando as requisições de transcrição com **erro 429 (Too Many Requests)**.

### **Mensagem de Erro:**
```
429 Client Error: Too Many Requests for url: https://www.youtube.com/api/timedtext
```

---

## 🔍 Por Que Acontece?

O YouTube tem limites de requisições para evitar abuso:

1. **Muitas requisições em pouco tempo** - Testamos vários vídeos seguidos
2. **Mesmo IP fazendo muitas requisições** - Todos os testes vêm do mesmo computador
3. **Rate limit temporário** - YouTube bloqueia por algumas horas

---

## ✅ Soluções Implementadas

### **1. Cache de Transcrições**
```python
@st.cache_data(ttl=3600)  # Cache por 1 hora
def get_transcript(video_id, languages=['pt', 'pt-BR', 'en']):
    # ... código ...
```

**Benefício:** Transcrições já obtidas não precisam ser baixadas novamente.

### **2. Mensagem Informativa**
Quando o erro 429 ocorre, o app mostra:
```
⏳ YouTube bloqueou temporariamente as transcrições (muitas requisições). 
Aguarde alguns minutos e tente novamente.
```

### **3. Método Duplo**
- **Método 1:** `youtube-transcript-api` (principal)
- **Método 2:** `yt-dlp` (fallback)

---

## 🕐 Quanto Tempo Esperar?

O bloqueio do YouTube geralmente dura:
- **Mínimo:** 15-30 minutos
- **Típico:** 1-2 horas
- **Máximo:** 24 horas (casos raros)

---

## 💡 Como Evitar o Problema

### **Para Usuários:**

1. **Não teste muitos vídeos seguidos**
   - Aguarde 1-2 minutos entre transcrições
   - Use o cache (não recarregue a página)

2. **Use o cache do Streamlit**
   - Transcrições já obtidas ficam em cache por 1 hora
   - Não precisa baixar novamente

3. **Aguarde se bloqueado**
   - Se aparecer a mensagem de bloqueio, aguarde 30 minutos
   - Tente novamente depois

### **Para Desenvolvedores:**

1. **Implementar delay entre requisições**
   ```python
   import time
   time.sleep(2)  # Aguardar 2 segundos entre requisições
   ```

2. **Usar proxy/VPN** (avançado)
   - Mudar o IP para evitar bloqueio
   - Requer configuração adicional

3. **Implementar cache persistente**
   - Salvar transcrições em arquivo
   - Não fazer requisições repetidas

---

## 🔧 Solução Temporária (Agora)

### **Opção 1: Aguardar**
```bash
# Aguarde 30-60 minutos
# Depois tente novamente
```

### **Opção 2: Limpar Cache do Navegador**
```
1. Feche o app Streamlit
2. Aguarde 30 minutos
3. Abra novamente
```

### **Opção 3: Usar VPN**
```
1. Ative uma VPN
2. Mude para outro país
3. Tente novamente
```

---

## 📊 Status Atual

| Item | Status |
|------|--------|
| **youtube-transcript-api** | ❌ Bloqueado (429) |
| **yt-dlp** | ❌ Bloqueado (429) |
| **Cache** | ✅ Implementado |
| **Mensagem informativa** | ✅ Implementada |
| **Solução** | ⏳ Aguardar reset do rate limit |

---

## 🎯 Próximos Passos

### **Curto Prazo (Agora):**
1. ✅ Implementar cache (feito)
2. ✅ Adicionar mensagem informativa (feito)
3. ⏳ Aguardar reset do rate limit (30-60 min)

### **Médio Prazo (Futuro):**
1. Implementar delay automático entre requisições
2. Salvar transcrições em arquivo local
3. Adicionar opção de usar proxy

### **Longo Prazo (Opcional):**
1. Usar API oficial do YouTube (requer pagamento)
2. Implementar sistema de filas
3. Adicionar rate limiting no app

---

## 🧪 Como Testar

### **Verificar se o bloqueio acabou:**

```bash
# Ativar ambiente virtual
source venv/bin/activate

# Testar transcrição
python test_transcript_api.py
```

**Se funcionar:** ✅ Bloqueio acabou!  
**Se erro 429:** ⏳ Ainda bloqueado, aguarde mais

---

## 📚 Referências

- [YouTube Data API - Rate Limits](https://developers.google.com/youtube/v3/getting-started#quota)
- [youtube-transcript-api Issues](https://github.com/jdepoix/youtube-transcript-api/issues)
- [yt-dlp Documentation](https://github.com/yt-dlp/yt-dlp)

---

## 🆘 Suporte

Se o problema persistir por mais de 24 horas:

1. Verifique se o vídeo tem transcrição disponível no YouTube
2. Tente com outro vídeo
3. Verifique sua conexão de internet
4. Considere usar VPN

---

**Última Atualização:** 27 de Novembro de 2025, 11:27 UTC-03:00  
**Status:** ⏳ Aguardando reset do rate limit do YouTube
