# 📺 UI Streamlit - Cadastro de Canais

Interface web para gerenciar e classificar canais do YouTube.

## 🎯 Funcionalidades

### ✅ Visualização
- Lista completa de todos os canais
- Dados detalhados: inscritos, vídeos, views, país, etc.
- Estatísticas em tempo real

### 🔍 Filtros
- **Por Categoria:** Empresa, Comunidade, Pessoa, Não Considerado
- **Por Prioridade:** Alta, Média, Baixa
- **Por Texto:** Busca por nome do canal

### ✏️ Edição
- **Categoria:** Alterar tipo do canal
- **Subcategoria:** Campo texto livre para contexto adicional
- **Prioridade:** Definir relevância (Alta, Média, Baixa)

### ⚙️ Ações em Massa
- Selecionar múltiplos canais
- Aplicar categoria/prioridade em lote
- Economizar tempo em edições repetitivas

### 💾 Persistência
- Salva alterações em `newsletter_channels.json`
- Backup automático com timestamp
- Recarregar dados a qualquer momento

## 🚀 Como Usar

### Opção 1: Script Automático
```bash
./run_cadastro_canais.sh
```

### Opção 2: Manual
```bash
cd ui_streamlit
streamlit run cadastro_de_canais.py
```

### Opção 3: Com porta customizada
```bash
streamlit run ui_streamlit/cadastro_de_canais.py --server.port 8502
```

## 📊 Interface

### Sidebar
- **Filtros:** Categoria, Prioridade, Busca
- **Estatísticas:** Distribuição por categoria

### Main Area
- **Métricas:** Total, Filtrados, Média de Inscritos, Alta Prioridade
- **Ações em Massa:** Aplicar mudanças em lote
- **Lista de Canais:** Expandir para editar

### Cada Canal Mostra
- Nome, ID, URL
- Inscritos, Vídeos, Views
- País, Data de Criação
- Descrição
- Campos editáveis: Categoria, Subcategoria, Prioridade

## 💡 Casos de Uso

### 1. Revisar Classificação Automática
- Filtrar por categoria
- Verificar se está correto
- Corrigir se necessário

### 2. Adicionar Contexto
- Usar subcategoria para detalhar
- Ex: "Tech News", "AI Tools", "Tutorials"

### 3. Priorizar Canais
- Definir prioridade baseado em:
  - Relevância do conteúdo
  - Frequência de postagem
  - Qualidade dos vídeos

### 4. Preparar para Automação
- Dados limpos e estruturados
- Prontos para scripts de coleta
- Filtros para priorização

## 📁 Estrutura de Dados

### Input: `newsletter_channels.json`
```json
{
  "channels": [
    {
      "channel_id": "UC...",
      "channel_name": "Nome do Canal",
      "subscriber_count": 123456,
      "type": "empresa",
      "subcategory": "",
      "priority": "média"
    }
  ]
}
```

### Campos Adicionados
- `subcategory`: string (texto livre)
- `priority`: "alta" | "média" | "baixa"
- `updated_at`: timestamp ISO

## 🎨 Categorias

### Tipos Principais
1. **Empresa:** Canais corporativos, produtos
2. **Comunidade:** Grupos, comunidades, coletivos
3. **Pessoa:** Criadores individuais, influencers
4. **Não Considerado:** Canais irrelevantes ou fora do escopo

### Prioridades
1. **Alta:** Conteúdo essencial, alta relevância
2. **Média:** Conteúdo bom, relevância moderada
3. **Baixa:** Conteúdo ocasional, baixa relevância

## 🔄 Workflow Recomendado

1. **Abrir UI**
   ```bash
   ./run_cadastro_canais.sh
   ```

2. **Filtrar por Categoria**
   - Começar com "não considerado"
   - Reclassificar se necessário

3. **Adicionar Subcategorias**
   - Dar contexto aos canais
   - Facilitar futuras buscas

4. **Definir Prioridades**
   - Alta: canais principais
   - Média: canais secundários
   - Baixa: canais ocasionais

5. **Salvar Alterações**
   - Clicar em "💾 Salvar Alterações"
   - Verificar mensagem de sucesso

6. **Usar Dados**
   - Scripts de coleta podem usar prioridades
   - Filtros podem usar subcategorias
   - Análises podem usar classificações

## 🛠️ Tecnologias

- **Streamlit:** Framework web Python
- **Pandas:** Manipulação de dados
- **JSON:** Persistência de dados

## 📝 Notas

- Alterações são salvas apenas ao clicar em "Salvar"
- Recarregar dados descarta alterações não salvas
- Filtros não afetam os dados, apenas a visualização
- Ações em massa requerem seleção prévia

## 🚨 Troubleshooting

### Streamlit não encontrado
```bash
pip3 install streamlit
```

### Porta 8501 ocupada
```bash
streamlit run ui_streamlit/cadastro_de_canais.py --server.port 8502
```

### Erro ao salvar
- Verificar permissões do arquivo
- Verificar se JSON está válido
- Verificar espaço em disco

## 🔗 Links Úteis

- [Streamlit Docs](https://docs.streamlit.io)
- [JSON Validator](https://jsonlint.com)

---

**Desenvolvido para IANIA IA NEWS** 🤖✨
