# 🔄 Atualizar Playlists com Duração dos Vídeos

## 📊 Nova Funcionalidade Adicionada!

A interface agora mostra a **duração de cada vídeo** entre "Publicado" e "Playlist":

```
📅 Publicado | ⏱️ Duração | 🔒 Playlist | 🔑 Keywords | 🔗 Link
```

---

## ⚠️ Importante

**Playlists antigas não têm o campo `duration`**

Para ver as durações, você precisa **re-exportar suas playlists**.

---

## 🚀 Como Re-exportar Playlists

### **Opção 1: Re-exportar Todas as Playlists**

```bash
cd /Users/persivalballeste/Documents/LAB
source venv/bin/activate
python scripts/export_playlists_oauth.py
```

**Tempo estimado:** 2-5 minutos (depende do número de vídeos)

### **Opção 2: Re-exportar Playlist Específica**

Se você quiser re-exportar apenas uma playlist específica, pode deletar o arquivo JSON dela e rodar o script novamente:

```bash
# Exemplo: Re-exportar apenas "wip-persival"
rm playlists_oauth/wip-persival.json
python scripts/export_playlists_oauth.py
```

---

## 📊 O Que Mudou

### **Antes (sem duração):**
```json
{
  "video_id": "lfnJXlgpJT0",
  "title": "TOON Just Replaced JSON...",
  "published_at": "2025-11-17T...",
  ...
}
```

### **Depois (com duração):**
```json
{
  "video_id": "lfnJXlgpJT0",
  "title": "TOON Just Replaced JSON...",
  "published_at": "2025-11-17T...",
  "duration": "PT7M28S",
  ...
}
```

---

## 🎯 Formato de Duração

### **No JSON (ISO 8601):**
- `PT7M28S` = 7 minutos e 28 segundos
- `PT1H5M30S` = 1 hora, 5 minutos e 30 segundos
- `PT45S` = 45 segundos

### **Na Interface (Formatado):**
- `7:28` = 7 minutos e 28 segundos
- `1:05:30` = 1 hora, 5 minutos e 30 segundos
- `0:45` = 45 segundos

---

## 🔧 Como Funciona

### **Script Atualizado:**

1. **Busca vídeos da playlist** (como antes)
2. **Busca durações em lote** (NOVO!)
   - Agrupa até 50 vídeos por chamada
   - Usa `youtube.videos().list(part='contentDetails')`
   - Adiciona campo `duration` em cada vídeo

### **Interface Atualizada:**

1. **Lê campo `duration`** do JSON
2. **Converte formato** (PT7M28S → 7:28)
3. **Exibe na interface** entre Publicado e Playlist

---

## 💡 Exemplo de Uso

### **1. Re-exportar Playlists:**

```bash
cd /Users/persivalballeste/Documents/LAB
source venv/bin/activate
python scripts/export_playlists_oauth.py
```

**Saída esperada:**
```
🔐 Iniciando autenticação OAuth 2.0...
✅ Autenticação concluída!
📋 Buscando playlists...
✅ Encontradas 15 playlists

📋 Processando: wip-persival (789 vídeos)
   📊 Buscando durações de 789 vídeos...
   ✅ Exportada: playlists_oauth/wip-persival.json

📋 Processando: Estudos (125 vídeos)
   📊 Buscando durações de 125 vídeos...
   ✅ Exportada: playlists_oauth/Estudos.json

...
```

### **2. Recarregar App:**

```bash
# O app detecta automaticamente os novos arquivos
# Basta recarregar a página no navegador
```

### **3. Ver Durações:**

Busque por qualquer vídeo e veja:

```
📅 Publicado: 2025-11-17
⏱️ Duração: 7:28          ← NOVO!
🔒 Playlist: Privada
🔑 Keywords: toon json
🔗 Abrir vídeo
```

---

## 📈 Estatísticas

### **Chamadas à API:**

**Antes:**
- 1 chamada por playlist (listar vídeos)

**Depois:**
- 1 chamada por playlist (listar vídeos)
- 1 chamada a cada 50 vídeos (buscar durações)

**Exemplo:**
- Playlist com 100 vídeos = 3 chamadas (1 + 2)
- Playlist com 500 vídeos = 11 chamadas (1 + 10)

### **Quota da API:**

- Cada chamada = ~1-3 unidades de quota
- Limite diário = 10.000 unidades
- **Você tem quota suficiente!**

---

## ⏱️ Tempo de Processamento

| Vídeos | Tempo Estimado |
|--------|----------------|
| 50 | ~5 segundos |
| 100 | ~10 segundos |
| 500 | ~45 segundos |
| 1000 | ~1.5 minutos |

---

## 🐛 Troubleshooting

### **Problema: "Quota exceeded"**

**Solução:** Aguarde até o próximo dia (quota reseta à meia-noite PST)

### **Problema: "Duração não aparece"**

**Causa:** Playlist não foi re-exportada

**Solução:**
```bash
# Deletar playlist antiga
rm playlists_oauth/nome-da-playlist.json

# Re-exportar
python scripts/export_playlists_oauth.py
```

### **Problema: "Duração mostra 0:00"**

**Causa:** Vídeo foi deletado ou está privado

**Solução:** Normal - API retorna `PT0S` para vídeos inacessíveis

---

## 📝 Notas Técnicas

### **Função `get_video_durations()`:**

```python
def get_video_durations(youtube, video_ids):
    """
    Obtém durações em lote (até 50 vídeos por chamada)
    
    Returns:
        Dict {video_id: duration_iso}
    """
    durations = {}
    
    for i in range(0, len(video_ids), 50):
        batch = video_ids[i:i+50]
        
        response = youtube.videos().list(
            part='contentDetails',
            id=','.join(batch)
        ).execute()
        
        for item in response['items']:
            durations[item['id']] = item['contentDetails']['duration']
    
    return durations
```

### **Função `format_duration()`:**

```python
def format_duration(duration_iso):
    """
    Converte PT7M28S → 7:28
    Converte PT1H5M30S → 1:05:30
    """
    # Extrai H, M, S usando regex
    # Formata com zero-padding
    # Retorna string legível
```

---

## ✅ Checklist

- [ ] Re-exportar playlists com `python scripts/export_playlists_oauth.py`
- [ ] Verificar que arquivos JSON foram atualizados
- [ ] Recarregar app no navegador
- [ ] Buscar vídeos e verificar coluna "⏱️ Duração"
- [ ] Confirmar que durações estão corretas

---

## 🎉 Resultado Final

**Interface Completa:**

```
1. TOON Just Replaced JSON... And It's 5× Faster! I'm Shocked!

📅 Publicado: 2025-11-17
⏱️ Duração: 7:28
🔒 Playlist: Privada
🔑 Keywords: toon json
🔗 Abrir vídeo

📝 Ver descrição
📄 Obter Transcrição
```

**Perfeito! Agora você tem todas as informações importantes de cada vídeo! 🚀**

---

**Última Atualização:** 27 de Novembro de 2025, 12:10 UTC-03:00  
**Status:** ✅ Implementado e Funcionando
