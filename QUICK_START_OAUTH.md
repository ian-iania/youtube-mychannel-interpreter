# 🚀 Quick Start - OAuth para Playlists Privadas

## ⚡ Início Rápido (3 passos)

### 1️⃣ Instalar Dependências
```bash
pip install -r requirements.txt
```

### 2️⃣ Executar Script OAuth
```bash
python scripts/export_playlists_oauth.py
```

### 3️⃣ Autorizar no Navegador
- 🌐 Navegador abrirá automaticamente
- 🔐 Faça login na sua conta Google
- ✅ Clique em "Permitir"
- 🎉 Pronto! Playlists privadas exportadas!

---

## 📁 Resultado

```
playlists_oauth/
├── Minha_Playlist_Publica.json
├── Minha_Playlist_Privada.json    ← NOVO! 🔒
└── ...
```

---

## 🔄 Próximas Execuções

Não precisa autorizar novamente! O token é salvo automaticamente.

```bash
python scripts/export_playlists_oauth.py
# Executa direto, sem abrir navegador
```

---

## 📚 Documentação Completa

Para mais detalhes, veja: [OAUTH_SETUP.md](OAUTH_SETUP.md)

---

## ✨ Diferença

| Comando | Resultado |
|---------|-----------|
| `python scripts/export_playlists.py` | Só playlists públicas |
| `python scripts/export_playlists_oauth.py` | **Todas as playlists** 🎯 |

---

**Simples assim! 🚀**
