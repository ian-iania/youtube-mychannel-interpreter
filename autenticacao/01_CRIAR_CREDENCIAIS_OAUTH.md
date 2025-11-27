# 🔐 Passo 1: Criar Credenciais OAuth 2.0 no Google Cloud

## 📋 Objetivo
Criar credenciais OAuth 2.0 para permitir que sua aplicação acesse playlists privadas do YouTube.

---

## ✅ Pré-requisitos

- Conta Google ativa
- Acesso ao Google Cloud Console
- Projeto no Google Cloud (ou criar um novo)

---

## 🚀 Passo a Passo Completo

### **1. Acessar Google Cloud Console**

Abra o navegador e acesse:
```
https://console.cloud.google.com/
```

---

### **2. Criar ou Selecionar um Projeto**

#### **Se você já tem um projeto:**
- No topo da página, clique no seletor de projetos
- Selecione seu projeto existente

#### **Se precisa criar um novo projeto:**
1. Clique em **"Criar projeto"**
2. Digite um nome: `YouTube Playlist Manager`
3. Clique em **"Criar"**
4. Aguarde a criação (leva alguns segundos)

---

### **3. Habilitar YouTube Data API v3**

1. No menu lateral, vá em: **APIs e serviços** → **Biblioteca**
2. Na barra de pesquisa, digite: `YouTube Data API v3`
3. Clique no resultado **"YouTube Data API v3"**
4. Clique no botão **"ATIVAR"**
5. Aguarde a ativação

---

### **4. Configurar Tela de Consentimento OAuth**

1. No menu lateral, vá em: **APIs e serviços** → **Tela de consentimento OAuth**

2. **Escolher tipo de usuário:**
   - Selecione: **"Externo"** (External)
   - Clique em **"CRIAR"**

3. **Preencher informações do app:**

   **Página 1 - Informações do app:**
   ```
   Nome do app: YouTube Playlist Manager
   E-mail de suporte do usuário: seu-email@gmail.com
   Logotipo do app: (opcional - pode pular)
   Domínio do app: (opcional - pode pular)
   Links autorizados: (opcional - pode pular)
   E-mail do desenvolvedor: seu-email@gmail.com
   ```
   - Clique em **"SALVAR E CONTINUAR"**

   **Página 2 - Escopos:**
   - Clique em **"ADICIONAR OU REMOVER ESCOPOS"**
   - Na busca, digite: `youtube.readonly`
   - Marque: **"YouTube Data API v3 - .../auth/youtube.readonly"**
   - Clique em **"ATUALIZAR"**
   - Clique em **"SALVAR E CONTINUAR"**

   **Página 3 - Usuários de teste:**
   - Clique em **"+ ADICIONAR USUÁRIOS"**
   - Digite seu email: `seu-email@gmail.com`
   - Clique em **"ADICIONAR"**
   - Clique em **"SALVAR E CONTINUAR"**

   **Página 4 - Resumo:**
   - Revise as informações
   - Clique em **"VOLTAR AO PAINEL"**

---

### **5. Criar Credenciais OAuth 2.0**

1. No menu lateral, vá em: **APIs e serviços** → **Credenciais**

2. Clique no botão **"+ CRIAR CREDENCIAIS"**

3. Selecione: **"ID do cliente OAuth"**

4. **Configurar credencial:**
   ```
   Tipo de aplicativo: App para computador (Desktop app)
   Nome: YouTube Playlist Manager Desktop
   ```

5. Clique em **"CRIAR"**

6. **Copiar credenciais:**
   
   Uma janela popup aparecerá com:
   ```
   ID do cliente: 31459815274-xxxxxxxxxx.apps.googleusercontent.com
   Código secreto do cliente: GOCSPX-xxxxxxxxxxxxxxxxxxxxxxxx
   ```

   **⚠️ IMPORTANTE: Copie e guarde essas informações!**

7. Clique em **"OK"**

---

### **6. Configurar URIs de Redirecionamento (Importante!)**

1. Na lista de credenciais, clique no **nome da credencial** que você acabou de criar

2. Role até a seção **"URIs de redirecionamento autorizados"**

3. Clique em **"+ ADICIONAR URI"**

4. Adicione os seguintes URIs (um por vez):
   ```
   http://localhost
   http://localhost:8080
   http://localhost:8000
   ```

5. Clique em **"SALVAR"**

---

### **7. Adicionar seu Email como Usuário de Teste**

1. No menu lateral, vá em: **APIs e serviços** → **Tela de consentimento OAuth**

2. Clique em **"EDITAR APLICATIVO"** ou role até **"Usuários de teste"**

3. Na seção **"Usuários de teste"**, clique em **"+ ADICIONAR USUÁRIOS"**

4. Digite seu email: `seu-email@gmail.com`

5. Clique em **"ADICIONAR"**

6. Clique em **"SALVAR"**

---

### **8. (Opcional) Publicar o App**

Se você quiser que o app funcione sem avisos de "não verificado":

1. Na tela de consentimento OAuth, clique em **"PUBLICAR APLICATIVO"**
2. Confirme a publicação
3. **Nota:** Para uso pessoal, não é necessário fazer verificação pelo Google

---

## 📝 Salvar Credenciais

Crie um arquivo chamado `Oauth-client.env` com as credenciais:

```bash
IDdoClient=31459815274-xxxxxxxxxx.apps.googleusercontent.com
secret=GOCSPX-xxxxxxxxxxxxxxxxxxxxxxxx
```

**⚠️ NUNCA compartilhe essas credenciais publicamente!**

---

## ✅ Checklist de Conclusão

- [ ] Projeto criado no Google Cloud
- [ ] YouTube Data API v3 habilitada
- [ ] Tela de consentimento OAuth configurada
- [ ] Credenciais OAuth 2.0 criadas
- [ ] URIs de redirecionamento adicionados
- [ ] Email adicionado como usuário de teste
- [ ] Credenciais salvas em arquivo seguro

---

## 🎯 Próximo Passo

Agora que você tem as credenciais OAuth, vá para:
**[02_ACESSAR_PLAYLISTS_PRIVADAS.md](02_ACESSAR_PLAYLISTS_PRIVADAS.md)**

---

## 📚 Referências

- [Google Cloud Console](https://console.cloud.google.com/)
- [YouTube Data API v3](https://developers.google.com/youtube/v3)
- [OAuth 2.0 Documentation](https://developers.google.com/identity/protocols/oauth2)

---

**Criado em:** 27 de Novembro de 2025  
**Versão:** 1.0
