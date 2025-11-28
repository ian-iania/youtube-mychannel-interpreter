# 📰 IANIA IA NEWS - YouTube Newsletter Curator

Sistema automatizado de curadoria de vídeos do YouTube sobre Inteligência Artificial, com categorização por IA e interface web moderna.

---

## 🚀 **Quick Start**

### **1. UI Next.js (Pública)**
```bash
cd ui
npm install
npm run dev
```
**Acesse:** http://localhost:3003

### **2. Streamlit Admin (Classificação de Canais)**
```bash
./run_cadastro_canais.sh
```
**Acesse:** http://localhost:9500

---

## 📋 **Status do Projeto**

✅ **Concluído:**
- Extração de dados com fallback
- Categorização com IA (GPT-4o-mini)
- Classificação de 103 canais
- UI Next.js básica
- Streamlit Admin funcional

🚧 **Em Desenvolvimento:**
- Geração de newsletter (UI)
- Otimização da UI Next.js
- Performance Streamlit

📖 **Documentação:** Ver [`next-steps.md`](./next-steps.md) para detalhes completos

---

## 📁 **Estrutura**

```
NEWSLETTER/
├── scripts/          # Scripts Python (coleta, categorização, etc)
├── ui/              # Next.js UI pública
├── ui_streamlit/    # Streamlit Admin
├── docs/            # Documentação técnica
├── logs/            # Arquivos de log
├── newsletters/     # Dados de newsletters
└── next-steps.md    # Próximas etapas detalhadas
```

---

## 🛠️ **Tecnologias**

- **Backend:** Python 3.x
- **Frontend:** Next.js 14, React, TypeScript, Tailwind CSS
- **Admin:** Streamlit
- **IA:** OpenAI GPT-4o-mini
- **APIs:** YouTube Data API v3

---

## 📊 **Dados Atuais**

- **103 canais** classificados
- **473 vídeos** curados
- **11 categorias** de conteúdo
- **Alta prioridade:** 1 canal

---

## 🔗 **Links**

- **Próximas Etapas:** [`next-steps.md`](./next-steps.md)
- **Documentação Técnica:** [`docs/`](./docs/)
- **GitHub:** https://github.com/ian-iania/youtube-mychannel-interpreter

---

**Última atualização:** 27/11/2025
