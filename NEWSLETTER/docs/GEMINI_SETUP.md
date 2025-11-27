# 🔧 Setup Google Gemini API

## 📋 Pré-requisitos

- Conta Google
- Projeto no Google Cloud Console
- API Key do Gemini

---

## 🚀 Passo a Passo

### **1. Acessar Google AI Studio**

```
https://aistudio.google.com/
```

### **2. Criar API Key**

1. Clique em "Get API Key"
2. Selecione ou crie um projeto
3. Copie a API Key gerada

### **3. Adicionar ao .env**

```bash
# NEWSLETTER/.env
GOOGLE_API_KEY=sua_chave_aqui
OAUTH_CLIENT_ID=seu_client_id
OAUTH_CLIENT_SECRET=seu_client_secret
```

---

## 💰 Tier Grátis

### **Limites Generosos**

| Modelo | RPM | RPD | TPM |
|--------|-----|-----|-----|
| Gemini 2.5 Flash | 15 | 1,500 | 1M |
| Gemini 2.5 Flash-Lite | 15 | 1,500 | 1M |

**RPM:** Requests Per Minute  
**RPD:** Requests Per Day  
**TPM:** Tokens Per Minute

### **O Que Dá Para Fazer Grátis**

- ✅ **100 vídeos/dia** (análise completa)
- ✅ **Várias newsletters** por semana
- ✅ **Sem cartão de crédito** necessário

---

## 🧪 Testar Instalação

```python
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# Configurar API
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

# Testar
model = genai.GenerativeModel('gemini-2.5-flash-lite')
response = model.generate_content('Hello, Gemini!')

print(response.text)
```

**Saída esperada:**
```
Hello! How can I help you today?
```

---

## 📊 Modelos Disponíveis

### **Gemini 2.5 Flash**
- **Uso:** Tarefas complexas, raciocínio
- **Custo:** $0.075/$0.30 por 1M tokens
- **Contexto:** 1M tokens

### **Gemini 2.5 Flash-Lite** ⭐ Recomendado
- **Uso:** Análise de vídeos, newsletters
- **Custo:** $0.0375/$0.15 por 1M tokens
- **Contexto:** 1M tokens
- **Vantagem:** 50% mais barato!

### **Gemini 2.0 Flash**
- **Uso:** Tarefas rápidas
- **Custo:** Grátis (tier grátis)
- **Contexto:** 1M tokens

---

## 🎥 Análise de Vídeo

### **Exemplo Básico**

```python
import google.generativeai as genai

# Configurar
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
model = genai.GenerativeModel('gemini-2.5-flash-lite')

# Analisar vídeo do YouTube
video_url = "https://www.youtube.com/watch?v=VIDEO_ID"

response = model.generate_content([
    {
        'mime_type': 'video/youtube',
        'uri': video_url
    },
    """
    Analise este vídeo e forneça:
    1. Resumo em 2-3 parágrafos
    2. 3-5 principais takeaways
    3. Passo a passo (se for tutorial)
    4. Tópicos principais
    5. Nível de dificuldade
    
    Formato JSON.
    """
])

print(response.text)
```

### **Exemplo com Estrutura**

```python
import json

prompt = """
Analise este vídeo sobre IA e retorne JSON:

{
  "summary": "Resumo em 2-3 parágrafos",
  "key_takeaways": [
    "Ponto 1",
    "Ponto 2",
    "Ponto 3"
  ],
  "tutorial_steps": [
    "Passo 1",
    "Passo 2"
  ],
  "topics": ["AI", "LangChain"],
  "difficulty": "intermediate"
}
"""

response = model.generate_content([video_url, prompt])

# Parse JSON
analysis = json.loads(response.text)
print(analysis['summary'])
```

---

## ⚠️ Limites e Boas Práticas

### **Limites do Tier Grátis**

- ✅ 15 requests/minuto
- ✅ 1,500 requests/dia
- ✅ 1M tokens/minuto

### **Boas Práticas**

1. **Cache de Resultados**
   ```python
   # Salvar análises para não re-processar
   cache_file = f"cache/{video_id}.json"
   if os.path.exists(cache_file):
       return load_cache(cache_file)
   ```

2. **Rate Limiting**
   ```python
   import time
   
   # Aguardar entre requests
   time.sleep(4)  # 15 req/min = 1 a cada 4 seg
   ```

3. **Batch Processing**
   ```python
   # Processar em lotes
   for batch in chunks(videos, 15):
       process_batch(batch)
       time.sleep(60)  # Aguardar 1 minuto
   ```

4. **Fallback para Descrição**
   ```python
   # Vídeos >15 min: só descrição
   if duration_minutes > 15:
       return analyze_description_only(video)
   ```

---

## 🐛 Troubleshooting

### **Erro: API Key inválida**

```
Error: API key not valid
```

**Solução:**
1. Verificar se API Key está correta no `.env`
2. Verificar se API está habilitada no Google Cloud Console
3. Gerar nova API Key se necessário

### **Erro: Quota excedida**

```
Error: Resource exhausted
```

**Solução:**
1. Aguardar reset (diário às 00:00 PST)
2. Implementar cache
3. Reduzir número de requests
4. Upgrade para tier pago

### **Erro: Vídeo não encontrado**

```
Error: Video not available
```

**Solução:**
1. Verificar se vídeo é público
2. Verificar se URL está correta
3. Tentar com outro vídeo

---

## 📚 Recursos

- [Documentação Oficial](https://ai.google.dev/gemini-api/docs)
- [Pricing](https://ai.google.dev/gemini-api/docs/pricing)
- [Google AI Studio](https://aistudio.google.com/)
- [Exemplos](https://github.com/google-gemini/cookbook)

---

## ✅ Checklist

- [ ] Conta Google criada
- [ ] API Key gerada
- [ ] API Key no `.env`
- [ ] Biblioteca instalada (`pip install google-generativeai`)
- [ ] Teste básico funcionando
- [ ] Análise de vídeo funcionando

---

**Status:** ✅ Pronto para Uso  
**Próximo:** Implementar análise de vídeos
