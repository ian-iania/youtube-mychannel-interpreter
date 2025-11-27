# 🔐 Documentação de Autenticação OAuth 2.0

## 📚 Índice de Documentos

Esta pasta contém toda a documentação necessária para configurar e usar OAuth 2.0 para acessar playlists privadas do YouTube.

---

## 📄 Documentos Disponíveis

### **1. [01_CRIAR_CREDENCIAIS_OAUTH.md](01_CRIAR_CREDENCIAIS_OAUTH.md)**
**Objetivo:** Criar credenciais OAuth 2.0 no Google Cloud Console

**Conteúdo:**
- Criar projeto no Google Cloud
- Habilitar YouTube Data API v3
- Configurar tela de consentimento OAuth
- Criar credenciais OAuth 2.0
- Adicionar URIs de redirecionamento
- Adicionar usuários de teste
- Publicar o app (opcional)

**Tempo estimado:** 15-20 minutos

---

### **2. [02_ACESSAR_PLAYLISTS_PRIVADAS.md](02_ACESSAR_PLAYLISTS_PRIVADAS.md)**
**Objetivo:** Usar OAuth 2.0 para exportar playlists privadas

**Conteúdo:**
- Configurar credenciais no projeto
- Instalar dependências OAuth
- Executar script de exportação
- Processo completo de autenticação
- Lidar com avisos de segurança
- Autorizar permissões
- Verificar resultados
- Troubleshooting completo

**Tempo estimado:** 10-15 minutos (primeira vez)

---

## 🚀 Fluxo Recomendado

```
1️⃣ Criar Credenciais OAuth
   ↓
   [01_CRIAR_CREDENCIAIS_OAUTH.md]
   ↓
2️⃣ Configurar e Usar
   ↓
   [02_ACESSAR_PLAYLISTS_PRIVADAS.md]
   ↓
3️⃣ Sucesso! ✅
```

---

## ⚡ Quick Start

### **Se você já tem credenciais OAuth:**

Pule para: [02_ACESSAR_PLAYLISTS_PRIVADAS.md](02_ACESSAR_PLAYLISTS_PRIVADAS.md)

### **Se é a primeira vez:**

Comece por: [01_CRIAR_CREDENCIAIS_OAUTH.md](01_CRIAR_CREDENCIAIS_OAUTH.md)

---

## 📊 Comparação: API Key vs OAuth 2.0

| Característica | API Key | OAuth 2.0 |
|----------------|---------|-----------|
| **Acesso** | Apenas playlists públicas | Todas as playlists |
| **Configuração** | Simples (1 passo) | Moderada (2 passos) |
| **Autenticação** | Não requer | Login Google |
| **Playlists Privadas** | ❌ Não | ✅ Sim |
| **Tempo de Setup** | 5 minutos | 25-35 minutos |
| **Uso Recomendado** | Testes rápidos | Uso completo |

---

## 🎯 Quando Usar Cada Método

### **Use API Key quando:**
- ✅ Você só precisa de playlists públicas
- ✅ Quer testar rapidamente
- ✅ Não quer configurar OAuth

### **Use OAuth 2.0 quando:**
- ✅ Precisa acessar playlists privadas
- ✅ Quer acesso completo às suas playlists
- ✅ Está usando em produção

---

## 📁 Arquivos Importantes

### **Credenciais:**
```
.env                    # Configuração principal (OAuth + API Key)
Oauth-client.env        # Backup das credenciais OAuth
token.pickle            # Token OAuth salvo (gerado automaticamente)
```

### **Scripts:**
```
scripts/export_playlists.py         # Usa API Key (só públicas)
scripts/export_playlists_oauth.py   # Usa OAuth (todas)
```

### **Playlists Exportadas:**
```
playlists/              # Playlists públicas (API Key)
playlists_oauth/        # Todas as playlists (OAuth)
```

---

## ✅ Checklist Completo

### **Fase 1: Criar Credenciais**
- [ ] Projeto criado no Google Cloud
- [ ] YouTube Data API v3 habilitada
- [ ] Tela de consentimento configurada
- [ ] Credenciais OAuth criadas
- [ ] URIs de redirecionamento adicionados
- [ ] Email adicionado como usuário de teste
- [ ] Credenciais salvas

### **Fase 2: Usar OAuth**
- [ ] Credenciais configuradas no `.env`
- [ ] Dependências instaladas
- [ ] Script executado
- [ ] Autenticação concluída
- [ ] Token salvo
- [ ] Playlists exportadas
- [ ] Playlists privadas acessíveis

---

## 🐛 Problemas Comuns

### **1. Erro: "redirect_uri_mismatch"**
**Solução:** Adicionar URIs de redirecionamento no Google Cloud Console

### **2. Erro: "access_denied" ou "Error 403"**
**Solução:** Adicionar email como usuário de teste

### **3. Erro: "invalid_client"**
**Solução:** Verificar Client Secret no `.env`

### **4. Aviso: "App não verificado"**
**Solução:** Clicar em "Avançado" → "Ir para app (não seguro)"

---

## 📚 Documentação Adicional

### **No Projeto:**
- `OAUTH_SETUP.md` - Documentação completa e detalhada
- `QUICK_START_OAUTH.md` - Guia rápido de 3 passos
- `OAUTH_SUMMARY.md` - Resumo executivo com estatísticas

### **Google:**
- [YouTube Data API v3](https://developers.google.com/youtube/v3)
- [OAuth 2.0 Documentation](https://developers.google.com/identity/protocols/oauth2)
- [Google Cloud Console](https://console.cloud.google.com/)

---

## 🎊 Resultado Final

Após seguir toda a documentação, você terá:

- ✅ **Acesso completo** às suas playlists
- ✅ **2.777+ vídeos** exportados
- ✅ **Playlists privadas** acessíveis
- ✅ **Token salvo** para uso futuro
- ✅ **Sistema funcionando** perfeitamente

---

## 🆘 Suporte

Se precisar de ajuda:

1. **Consulte os documentos** nesta pasta
2. **Verifique o Troubleshooting** em cada documento
3. **Revise as configurações** no Google Cloud Console
4. **Teste com o script** de exportação

---

## 📝 Notas Importantes

### **Segurança:**
- 🔒 Nunca compartilhe suas credenciais OAuth
- 🔒 Nunca versione `token.pickle` no Git
- 🔒 Use `.env` para configurações sensíveis
- 🔒 Revogue tokens se comprometidos

### **Manutenção:**
- 🔄 Token é renovado automaticamente
- 🔄 Não precisa reautenticar sempre
- 🔄 Credenciais são válidas indefinidamente
- 🔄 Pode revogar acesso a qualquer momento

---

## 🎯 Próximos Passos

Após concluir a autenticação OAuth:

1. **Explorar playlists exportadas** em `playlists_oauth/`
2. **Usar no app Streamlit** para buscar vídeos
3. **Obter transcrições** de vídeos privados
4. **Marcar favoritos** de todas as playlists

---

**Criado em:** 27 de Novembro de 2025  
**Versão:** 1.0  
**Status:** ✅ Completo e Testado

---

**Boa sorte com sua implementação OAuth! 🚀**
