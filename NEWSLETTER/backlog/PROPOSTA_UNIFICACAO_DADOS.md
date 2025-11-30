# Proposta: Unificação de Dados entre Site e Streamlit

**Data:** 29/11/2025  
**Status:** Backlog  
**Prioridade:** Média

## Contexto

Atualmente existem dois sistemas separados:

| Sistema | Fonte de dados | Vídeos |
|---------|----------------|--------|
| **Site Next.js** | `ui/lib/real-data.ts` | 148 (newsletter AI curada) |
| **Streamlit (app.py)** | `playlists/*.json` | 2.279 (playlists pessoais) |

Os dados não são compartilhados entre os sistemas.

---

## Opção A: Site como Interface Principal (Recomendado)

Migrar tudo para o site Next.js, que é mais moderno e bonito.

```
┌─────────────────────────────────────────────────────────────┐
│                    SITE UNIFICADO                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  🌐 SITE NEXT.JS (interface única)                          │
│     │                                                       │
│     ├── 📰 Aba "Newsletter AI" (148 vídeos curados)         │
│     │      └── Fonte: pipeline de canais AI                 │
│     │                                                       │
│     └── 📺 Aba "Minhas Playlists" (2.279 vídeos)            │
│            └── Fonte: playlists/*.json                      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Vantagens
- Interface única e moderna
- Filtros, busca, categorias já implementados
- Sem duplicação de código
- Design responsivo

### Implementação
1. Adicionar seletor no topo: "Newsletter AI" | "Minhas Playlists"
2. Carregar dados diferentes baseado na seleção
3. Adicionar funcionalidade de transcrição ao site

### Esforço estimado: 4-6 horas

---

## Opção B: Streamlit como Interface Principal

Adicionar os dados da newsletter ao Streamlit existente.

```
┌─────────────────────────────────────────────────────────────┐
│                 STREAMLIT UNIFICADO                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  📱 STREAMLIT (interface única)                             │
│     │                                                       │
│     ├── 📺 Aba "Minhas Playlists" (atual)                   │
│     │                                                       │
│     └── 📰 Aba "Newsletter AI" (nova)                       │
│            └── Com resumos, transcrições, etc.              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Vantagens
- Mais simples de manter (só Python)
- Transcrições já funcionam
- Menos tecnologias envolvidas

### Implementação
1. Adicionar aba para Newsletter AI
2. Carregar dados de `editions/*.json`
3. Adaptar visualização

### Esforço estimado: 2-3 horas

---

## Opção C: Manter Separados mas Sincronizados

Ambos sistemas leem da mesma fonte de dados.

```
┌─────────────────────────────────────────────────────────────┐
│                   FONTE ÚNICA                               │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  📁 editions/*.json (fonte única)                           │
│     │                                                       │
│     ├──→ 🌐 Site Next.js (visualização bonita)              │
│     │                                                       │
│     └──→ 📱 Streamlit (transcrições, busca)                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Vantagens
- Cada sistema mantém sua especialidade
- Dados sempre sincronizados
- Menor risco de quebrar algo

### Implementação
1. Converter playlists para formato editions
2. Adaptar Streamlit para ler editions
3. Manter ambos sistemas

### Esforço estimado: 3-4 horas

---

## Recomendação

**Opção A** é a mais recomendada por:
1. UI mais moderna e profissional
2. Menos manutenção a longo prazo
3. Melhor experiência do usuário
4. Possibilidade de deploy público

---

## Ferramentas já criadas

- `scripts/convert_playlists_to_edition.py` - Converte playlists para formato do site
- `scripts/generate_real_data.py` - Gera TypeScript a partir de editions

---

## Próximos passos (quando implementar)

1. [ ] Escolher opção
2. [ ] Implementar seletor de fonte de dados
3. [ ] Testar com ambas fontes
4. [ ] Adicionar transcrições (se Opção A)
5. [ ] Deploy
