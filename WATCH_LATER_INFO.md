# 📺 Sobre a Playlist "Watch Later" (Assistir Mais Tarde)

## ❓ Por Que Não Foi Exportada?

A playlist **"Watch Later"** (`list=WL`) é uma **playlist especial** do YouTube que:

- ❌ Não aparece na lista de playlists do canal
- ❌ Não é retornada pela API de playlists
- ✅ É uma funcionalidade interna do YouTube
- ✅ Só pode ser acessada diretamente pela URL

---

## 🔍 Como Identificar

URLs da playlist "Watch Later" têm o formato:
```
https://www.youtube.com/watch?v=VIDEO_ID&list=WL
```

O `list=WL` indica que é a playlist "Watch Later".

---

## 💡 Solução: Exportar Watch Later Manualmente

### **Opção 1: Criar Playlist Normal**

1. Acesse sua playlist "Watch Later"
2. Selecione todos os vídeos
3. Clique em "Adicionar a" → "Nova playlist"
4. Dê um nome: "Watch Later - Backup"
5. Execute o script OAuth novamente:
   ```bash
   python scripts/export_playlists_oauth.py
   ```

---

### **Opção 2: Script Específico para Watch Later**

Posso criar um script específico que exporta a playlist "Watch Later" usando o ID especial `WL`.

**Quer que eu crie esse script?**

---

## 🎯 Vídeo Específico

O vídeo que você mencionou:
```
URL: https://www.youtube.com/watch?v=KO6a3QYpZbo&list=WL
Título: TOON Just Replaced JSON… And It's 5× Faster! I'm Shocked!
```

**Este vídeo está na playlist "Watch Later"**, por isso não apareceu nos resultados.

---

## ✅ Vídeos Encontrados

Os 2 vídeos que apareceram nos resultados estão na playlist **"wip-persival"**:

1. **TOON Just Replaced JSON… And It's 5× Faster! I'm Shocked!**
   - Data: 2025-11-17
   - Keywords: json, toon

2. **Toon vs Json vs CSV**
   - Data: 2025-11-15
   - Keywords: json, toon

**Nota:** O primeiro vídeo pode estar em DUAS playlists:
- ✅ "wip-persival" (exportada)
- ✅ "Watch Later" (não exportada)

---

## 🔧 Próximos Passos

### **Para Incluir Watch Later:**

**Opção A - Criar Playlist Normal (Recomendado):**
1. Criar playlist normal com vídeos do Watch Later
2. Exportar novamente com OAuth

**Opção B - Script Específico:**
1. Eu crio um script para exportar Watch Later
2. Você executa o script
3. Vídeos aparecem no app

---

## 📊 Comparação

| Playlist | Tipo | Exportável? | Solução |
|----------|------|-------------|---------|
| Playlists normais | Normal | ✅ Sim | Script OAuth |
| Watch Later | Especial | ❌ Não | Script específico ou criar playlist normal |
| Liked Videos | Especial | ❌ Não | Script específico |
| History | Especial | ❌ Não | API diferente |

---

## 💡 Recomendação

**Criar uma playlist normal** é a solução mais simples e mantém seus vídeos organizados:

1. Acesse: https://www.youtube.com/playlist?list=WL
2. Selecione os vídeos importantes
3. Adicione a uma nova playlist: "Meus Vídeos Salvos"
4. Execute: `python scripts/export_playlists_oauth.py`
5. Os vídeos aparecerão no app!

---

**Quer que eu crie um script específico para Watch Later?** 🚀
