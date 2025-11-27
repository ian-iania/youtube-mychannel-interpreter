# 🤖 AI Newsletter Generator

Gerador automático de newsletter sobre canais de IA do YouTube usando OAuth 2.0 e Google Gemini.

---

## 🎯 Funcionalidades

### **1. Coleta Automática**
- ✅ Lista canais que você segue (inscrições)
- ✅ Busca vídeos dos últimos N dias (configurável)
- ✅ Captura metadados: título, descrição, duração, thumbnail
- ✅ Identifica tipo de canal (pessoa/empresa/comunidade)

### **2. Análise Inteligente**
- ✅ Vídeos **≤15 min**: Transcrição completa + análise detalhada
- ✅ Vídeos **>15 min**: Análise da descrição + duração
- ✅ Usa **Google Gemini 2.5 Flash** (multimodal, vídeo nativo)
- ✅ Extrai: resumo, takeaways, tutorial (se aplicável)

### **3. Newsletter Formatada**
- ✅ Organizada por canal
- ✅ Identifica pessoa/empresa/comunidade
- ✅ Thumbnails dos vídeos
- ✅ Estatísticas gerais
- ✅ Narrativa jornalística
- ✅ Exporta em Markdown

---

## 💰 Custo-Benefício: Google Gemini vs OpenAI

### **Comparação de Modelos**

| Modelo | Entrada | Saída | Vídeo | Áudio | Contexto |
|--------|---------|-------|-------|-------|----------|
| **Gemini 2.5 Flash** | $0.075/1M | $0.30/1M | ✅ Nativo | ✅ Nativo | 1M tokens |
| **Gemini 2.5 Flash-Lite** | $0.0375/1M | $0.15/1M | ✅ Nativo | ✅ Nativo | 1M tokens |
| OpenAI GPT-4o-mini | $0.15/1M | $0.60/1M | ❌ | ❌ | 128K tokens |
| OpenAI Whisper | - | - | ❌ | $0.006/min | - |

### **Vantagens do Gemini 2.5 Flash**

#### **1. Análise Nativa de Vídeo**
```python
# Gemini: Envia vídeo diretamente
response = model.generate_content([
    video_file,
    "Analise este vídeo..."
])

# OpenAI: Precisa transcrever primeiro
audio = download_audio(video)  # Tempo + custo
transcript = whisper.transcribe(audio)  # $0.006/min
response = gpt.chat([transcript])  # $0.15/1M tokens
```

#### **2. Custo Muito Menor**

**Exemplo: 50 vídeos de 10 min cada**

| Solução | Processo | Custo |
|---------|----------|-------|
| **OpenAI** | Whisper (500 min) + GPT-4o-mini | $3.00 + $0.15 = **$3.15** |
| **Gemini 2.5 Flash** | Análise direta de vídeo | **$0.50** |
| **Gemini 2.5 Flash-Lite** | Análise direta de vídeo | **$0.25** |

**Economia: 85-92%!**

#### **3. Multimodal Nativo**
- ✅ Entende vídeo (visual + áudio)
- ✅ Vê slides, gráficos, código na tela
- ✅ Contexto completo (não só áudio)
- ✅ Melhor qualidade de análise

#### **4. Mais Rápido**
- ❌ OpenAI: Download → Transcrição → Análise (3 etapas)
- ✅ Gemini: Análise direta (1 etapa)

---

## 🎯 Estratégia de Processamento

### **Regra: Vídeos ≤15 minutos**

**Por quê 15 minutos?**
- ✅ Custo controlado (~$0.01 por vídeo)
- ✅ Tempo de processamento aceitável
- ✅ Qualidade de análise excelente
- ✅ Maioria dos vídeos de IA são curtos

**Processamento:**
```python
if duration_minutes <= 15:
    # Análise completa com Gemini
    analysis = gemini.analyze_video(
        video_url=video_url,
        prompt="""
        Analise este vídeo e forneça:
        1. Resumo (2-3 parágrafos)
        2. 3-5 principais takeaways
        3. Passo a passo (se for tutorial)
        4. Tópicos principais
        5. Nível de dificuldade
        """
    )
else:
    # Análise da descrição apenas
    analysis = {
        'summary': f"Vídeo longo ({duration}). Descrição: {description}",
        'note': "Vídeo não analisado (>15 min)"
    }
```

---

## 📊 Estimativa de Custos

### **Newsletter Semanal (50 vídeos)**

**Distribuição típica:**
- 35 vídeos ≤15 min (70%)
- 15 vídeos >15 min (30%)

**Custos com Gemini 2.5 Flash-Lite:**

| Item | Quantidade | Custo Unit. | Total |
|------|------------|-------------|-------|
| Vídeos curtos (≤15 min) | 35 × 10 min | $0.01/vídeo | $0.35 |
| Vídeos longos (>15 min) | 15 × descrição | $0.001/análise | $0.015 |
| Newsletter final | 1 × 50K tokens | $0.0075 | $0.0075 |
| **TOTAL** | | | **~$0.37** |

**Com tier grátis do Gemini:** Várias newsletters grátis!

**Comparação:**
- OpenAI (Whisper + GPT-4o-mini): **$3.15**
- Gemini 2.5 Flash-Lite: **$0.37**
- **Economia: 88%!**

---

## 🏗️ Arquitetura

```
NEWSLETTER/
├── scripts/
│   ├── collect_subscriptions.py    # Busca canais seguidos
│   ├── collect_videos.py            # Busca vídeos recentes
│   ├── analyze_videos.py            # Análise com Gemini
│   └── generate_newsletter.py       # Gera newsletter final
├── newsletters/
│   ├── 2025-11-27_data.json        # Dados brutos
│   └── 2025-11-27_newsletter.md    # Newsletter formatada
├── templates/
│   └── newsletter_template.md       # Template Markdown
├── docs/
│   ├── GEMINI_SETUP.md             # Setup da API Gemini
│   └── COST_ANALYSIS.md            # Análise de custos
├── channel_metadata.json            # Tipo de cada canal
├── app_newsletter.py                # UI Streamlit
├── requirements.txt                 # Dependências
└── README.md                        # Este arquivo
```

---

## 🔧 Tecnologias

### **APIs**
- Google YouTube Data API v3 (OAuth 2.0)
- Google Gemini 2.5 Flash-Lite
- yt-dlp (fallback se necessário)

### **Python**
- Streamlit (UI)
- google-generativeai (Gemini)
- google-api-python-client (YouTube)
- python-dotenv (variáveis de ambiente)

---

## 🚀 Como Usar

### **1. Configurar APIs**

```bash
# .env
GOOGLE_API_KEY=sua_chave_gemini
OAUTH_CLIENT_ID=seu_client_id
OAUTH_CLIENT_SECRET=seu_client_secret
```

### **2. Instalar Dependências**

```bash
cd NEWSLETTER
pip install -r requirements.txt
```

### **3. Executar UI**

```bash
streamlit run app_newsletter.py
```

### **4. Gerar Newsletter**

1. Selecionar período (últimos N dias)
2. Escolher canais (ou todos)
3. Clicar em "🚀 Gerar Newsletter"
4. Aguardar processamento
5. Baixar Markdown

---

## 📝 Formato da Newsletter

```markdown
# 🤖 AI Newsletter - Últimos 7 Dias
*Gerado em 27 de Novembro de 2025*

---

## 📺 Dave Ebbelaar (👤 Pessoa)
*3 vídeos | 42 min total*

![Thumbnail](https://i.ytimg.com/vi/abc/hqdefault.jpg)

### 🎯 Destaques da Semana
Dave focou em agentes de IA esta semana...

### 📹 Vídeos:

**1. Build RAG with LangChain** (12:30)
- **Resumo:** Tutorial completo sobre...
- **Principais Pontos:**
  - Como estruturar documentos
  - Embeddings eficientes
- **Tutorial:**
  1. Instalar LangChain
  2. Configurar vector store

**2. Advanced Agent Patterns** (15:45)
- **Resumo:** Padrões avançados...

**3. Long Video Title** (53:20)
- **Nota:** Vídeo longo (53:20)
- **Descrição:** Este vídeo explora...

---

## 🏢 OpenAI (🏢 Empresa)
*2 vídeos | 25 min total*

...

---

## 📊 Resumo Geral
- **Canais:** 15
- **Vídeos:** 47 (35 analisados, 12 descrições)
- **Duração total:** 8h 23min
- **Tópicos:** RAG, Agents, LangChain, Fine-tuning
```

---

## 🎨 Features da UI

### **Configurações**
- 📅 Período (1-30 dias)
- 🎯 Filtro de canais
- ⏱️ Limite de duração (15 min padrão)
- 🎨 Incluir thumbnails

### **Processamento**
- 📊 Barra de progresso
- 📝 Log em tempo real
- ⚠️ Avisos de custo
- 💾 Auto-save

### **Resultado**
- 📄 Preview da newsletter
- 📥 Download Markdown
- 📧 Enviar por email (futuro)
- 🔗 Compartilhar (futuro)

---

## 🔄 Reutilização de Código

### **Do Projeto Principal (80%)**

```python
# OAuth e autenticação
from ../scripts/export_playlists_oauth import get_authenticated_service

# Busca de vídeos
from ../scripts/export_playlists_oauth import get_video_durations

# Formatação
from ../app_oauth import format_duration

# Estrutura de dados
# Mesma estrutura JSON
```

### **Novo (20%)**

```python
# Integração Gemini
import google.generativeai as genai

# Análise de vídeo
def analyze_video_with_gemini(video_url, duration_minutes):
    if duration_minutes <= 15:
        # Análise completa
        return gemini.analyze_video(video_url)
    else:
        # Só descrição
        return analyze_description_only()

# Geração de newsletter
def generate_newsletter_narrative(channels_data):
    return gemini.generate_content(prompt)
```

---

## 📈 Roadmap

### **Fase 1: MVP (Atual)**
- [x] Estrutura do projeto
- [x] Documentação
- [ ] Coleta de inscrições
- [ ] Coleta de vídeos recentes
- [ ] Integração Gemini
- [ ] Geração de newsletter
- [ ] UI Streamlit

### **Fase 2: Melhorias**
- [ ] Cache de análises
- [ ] Filtros avançados
- [ ] Múltiplos templates
- [ ] Exportar PDF
- [ ] Envio por email

### **Fase 3: Avançado**
- [ ] Agendamento automático
- [ ] Notificações
- [ ] Análise de tendências
- [ ] Recomendações personalizadas

---

## 💡 Vantagens vs OpenAI

| Aspecto | OpenAI | Gemini |
|---------|--------|--------|
| **Custo** | $3.15 | $0.37 |
| **Velocidade** | 3 etapas | 1 etapa |
| **Qualidade** | Só áudio | Vídeo completo |
| **Contexto** | 128K | 1M tokens |
| **Multimodal** | ❌ | ✅ |
| **Tier grátis** | $5 | Generoso |

---

## 🎯 Conclusão

**Por que Gemini 2.5 Flash-Lite?**

1. ✅ **88% mais barato** que OpenAI
2. ✅ **Análise nativa de vídeo** (vê slides, código)
3. ✅ **Mais rápido** (1 etapa vs 3)
4. ✅ **Melhor qualidade** (contexto visual)
5. ✅ **Tier grátis generoso**

**Resultado:**
- Newsletter semanal por **$0.37**
- Qualidade superior
- Processamento mais rápido
- Análise mais rica

---

**Status:** 🚧 Em Desenvolvimento  
**Próximo:** Implementar coleta de inscrições  
**Data:** 27 de Novembro de 2025
