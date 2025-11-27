template da newsletter define **muito bem a estrutura de dados**, e o que falta é “ensinar” isso para o prompt de UI — em vez de ficar só falando em “serviços de agência”.

Vou fazer duas coisas:

1. **Refletir rápido sobre o formato** (landing vs blog).
2. **Te entregar um prompt novo, mais elaborado, já adaptado para o formato da newsletter + imagens multimodais**, com o nome **IANIA IA NEWS**.

---

## 1. Reflexão rápida: landing ou blog?

Pelo seu template (`template_newsletter.md`), a newsletter tem:

* Cabeçalho:

  * título (`AI Newsletter - Semana de [DATA]`),
  * tagline,
  * resumo da edição.
* Um índice “📊 Nesta Edição” com **categorias + contagem de vídeos**.
* Várias **seções/categorias** (`## 🚀 Novos Modelos e Atualizações`, `## 🏢 Produtos...`, `## ⚙️ Automação...`, etc.).
* Dentro de cada categoria:

  * Vários **vídeos**, cada um com:

    * título do vídeo
    * nome do canal
    * duração
    * views
    * resumo em texto
    * lista de “Principais pontos”
    * link do vídeo.

Isso é **mais um blog / hub de conteúdo** do que uma landing “one shot” de produto.

💡 Então a melhor metáfora é:

* Uma página principal tipo **“portal de notícias / blog de IA”**, com:

  * **Aba / modo “Edição Atual”** (semana corrente, dividida em categorias).
  * **Aba / modo “Por Categoria”** (filtrar pelo tema: Modelos, Automação, IDEs, etc.).
  * **Aba / modo “Arquivo”** (lista de edições passadas).

Mesmo assim, podemos manter toda a estética de **landing Awwwards** (hero insano, shader, bento grid) — só que aplicada a um **blog/editorial IA-first**.

O nome perfeito: **IANIA IA NEWS** ✅

---

## 2. Prompt novo e mais elaborado (em português)

Aqui vai o **prompt completo revisado**, já levando em conta:

* Formato da newsletter (edição, categorias, vídeos).
* Estrutura mais “blog/hub” com abas.
* Geração de ícones/imagens com modelo multimodal.
* Design avançado (shader, bento grid, framer-motion, etc.).

> Você pode usar esse prompt direto para gerar a UI em Next/React.

---

### 🧾 PROMPT: **IANIA IA NEWS – Portal de Newsletters de Inteligência Artificial**

Você é um Creative Developer & UI/UX Designer premiado, especialista em interfaces “AI-First” dignas de Awwwards. Seu estilo combina:

* Shaders reativos (React Three Fiber / GLSL)
* Glassmorphism técnico
* Gradientes profundos e texturas sutis
* Animações fluidas com Framer Motion
* Layouts editoriais sofisticados (tipo blog premium)

---

## 🎯 Objetivo

Construir uma **página web/portal editorial** chamada **“IANIA IA NEWS”**, que apresenta **newsletters semanais de Inteligência Artificial**.

O foco não é criar o conteúdo (ele já existe), mas sim:

* Visualizar **a edição atual** de forma envolvente.
* Permitir navegar pelas notícias **por categoria**.
* Acessar **edições anteriores** (arquivo).
* Usar um **modelo multimodal** para sugerir/gerar **ícones e imagens** para:

  * o brand principal (IANIA IA NEWS),
  * cada categoria da newsletter.

A stack visual/código deve ser:

* **Next.js 14 (App Router)**
* **React**
* **Tailwind CSS**
* **Framer Motion**
* **React Three Fiber** (shader de fundo)
* **lucide-react** (ícones vetoriais)
* `clsx` + `tailwind-merge` para classes

---

## 📚 Estrutura de Dados da Newsletter (importante entender)

A newsletter segue uma estrutura fixa, similar ao markdown abaixo (apenas exemplo):

* Título geral:

  * `# 🤖 AI Newsletter - Semana de [DATA]`
* Subtítulo:

  * `> Sua curadoria semanal de IA e tecnologia, organizada por temas relevantes`
* Seção índice:

  * `## 📊 Nesta Edição`

    * Lista de categorias com contagem:

      * “🚀 Novos Modelos e Atualizações (X vídeos)”
      * “🏢 Produtos e Atualizações de Empresas (X vídeos)”
      * “⚙️ Automação e Workflows (X vídeos)`
      * “💻 IDEs e Agentes de Código (X vídeos)`, etc.
* Para cada categoria (exemplos reais do template):

  * `## 🚀 Novos Modelos e Atualizações`
  * `## 🏢 Produtos e Atualizações de Empresas`
  * `## ⚙️ Automação e Workflows`
  * `## 💻 IDEs e Agentes de Código`
  * `## 📓 NotebookLM`
  * `## 🏗️ Arquitetura e Design`
  * `## 🎓 Cursos e Treinamentos`
  * `## 🔧 Ferramentas de Desenvolvimento`
  * `## 🎨 Ferramentas de Mídia`
  * `## 📰 Notícias e Assuntos Gerais`
  * `## 📌 Outros Temas`
  * `## 📚 Recursos Adicionais`

Dentro de cada categoria, existem **vários vídeos**, cada um com:

* `#### [Título do Vídeo]`
* Linha de meta:

  * `**📺 [Nome do Canal]** | ⏱️ X min | 👁️ X.XK views`
* Resumo em parágrafo:

  * `[...] [Resumo do vídeo...]`
* Lista de “Principais pontos”:

  * `**Principais pontos:**`
  * `- item 1`
  * `- item 2`
  * ...
* Link:

  * `[▶️ Assistir](https://youtube.com/watch?v=...)`

Você deve assumir que esse conteúdo será fornecido em formato estruturado (por exemplo, um objeto JavaScript ou JSON com:

```ts
type Video = {
  title: string;
  channel: string;
  duration: string;
  views: string;
  summary: string;
  keyPoints: string[];
  url: string;
};

type Category = {
  id: string;
  emoji: string; // ex: "🚀"
  name: string;  // ex: "Novos Modelos e Atualizações"
  description: string;
  videoCount: number;
  videos: Video[];
};

type Edition = {
  id: string;
  weekLabel: string;    // ex: "Semana de 24/11/2025"
  dateRange: string;    // ex: "24–30 nov 2025"
  tagline: string;
  categories: Category[];
  summaryHighlights: {
    categoryName: string;
    emoji: string;
    videoCount: number;
  }[];
};
```

---

## 🧠 Arquitetura da Página / Navegação

A interface do **IANIA IA NEWS** deve funcionar mais como um **portal/blog de notícias** do que uma landing estática.

Estrutura principal:

1. **Hero (Edição Atual + Marca)**
2. **Tabs / Navegação de Conteúdo**:

   * Tab 1: **“Edição Atual”**
   * Tab 2: **“Por Categoria”**
   * Tab 3: **“Arquivo de Edições”** (mock de edições anteriores)
3. **Seção “Por que IANIA IA NEWS?”**
4. **Footer interativo com marquee**

### Tab 1 – Edição Atual

* Mostrar a edição atual como um **editorial longo**:

  * Hero da edição: título “IA Newsletter – Semana de [DATA]”.
  * Subtítulo da curadoria.
  * Cards-resumo da seção “📊 Nesta Edição” (cada card = categoria + X vídeos).
* Embaixo, o conteúdo por categoria:

  * Cada categoria em uma **seção colapsável** ou **accordion animado**:

    * Cabeçalho com:

      * emoji + nome da categoria
      * descrição curta
      * badge com “X vídeos”
      * **ícone/imagem gerado com IA** (detalhado na seção “Multimodal” abaixo)
    * Ao expandir:

      * Lista de vídeos como **cards editoriais**:

        * título do vídeo
        * metadados (canal, duração, views)
        * resumo
        * lista “Principais pontos”
        * botão “▶ Assistir” com link externo
      * Cards com hover técnico (parallax, blur, glow).

### Tab 2 – Por Categoria

* Um layout em **Bento Grid** onde cada **categoria** é um bloco destacado.
* Ao clicar numa categoria:

  * Mostrar apenas os vídeos daquela categoria em um painel central (tipo blog category view).
* Cada bloco de categoria:

  * Usa o **ícone/imagem multimodal** associado à categoria.
  * Mostra:

    * emoji + nome
    * 1–2 frases de descrição
    * contagem de vídeos
  * Hover:

    * tilt 3D
    * glow neon
    * leve zoom da imagem de fundo.

### Tab 3 – Arquivo

* Mock de edições anteriores:

  * Timeline vertical ou cards horizontais com:

    * Semana / Data
    * Principais categorias daquela edição
    * Contagem total de vídeos
  * Cada card tem CTA “Ver edição” (mesmo layout da Tab 1).

---

## 🧬 Geração Multimodal (ícones, logos, imagens)

Você deve **planejar o layout de forma que seja fácil plugar um modelo multimodal** (ex.: GPT-4o, Flux, SDXL, etc.) para gerar imagens.

Requisitos:

1. **Logo/Marca principal – IANIA IA NEWS**

   * Reservar espaço no hero para um logotipo/ícone abstrato de IA.

   * Definir um **prompt textual padrão** para gerar o logo, por exemplo:

   > “Generate a minimalist, neon-style logo for a premium AI newsletter called ‘IANIA IA NEWS’, with abstract neural network shapes, dark background and electric blue/purple highlights.”

   * O UI deve mostrar esse logo como `<Image>` com fallback (caso a geração não exista).

2. **Ícone/Imagem por categoria**

   * Cada `Category` deve ter um campo derivado, por exemplo `imagePrompt`, que descreve a imagem ideal para aquela categoria.
   * Exemplos:

     * Novos Modelos: “abstract 3D brain made of glowing polygons, representing new AI models”
     * Automação e Workflows: “flowing diagram of nodes and arrows with neon circuits”
     * IDEs e Agentes de Código: “code editor in dark mode with glowing AI assistant orb”
   * O layout dos cards de categoria deve:

     * exibir a imagem gerada + overlay com gradiente escuro
     * manter legibilidade do texto por cima.

3. **Thumbnails de vídeos (opcional)**

   * Planejar o card de vídeo com espaço para:

     * thumbnail do próprio YouTube (se quiser puxar via URL), ou
     * imagem multimodal gerada a partir do título + resumo.

Você não precisa implementar a chamada ao modelo multimodal, mas deve:

* Estruturar o código e props para receber `imageUrl` e/ou `imagePrompt`.
* Comentar no código onde a geração de imagem se encaixaria.

---

## 🎨 Diretrizes de Design (AI-First, anti-“AI slop”)

### Tipografia

* ❌ NÃO usar: Inter, Roboto, Open Sans, Segoe UI, system default.
* ✔️ USAR:

  * Heading: **Space Grotesk** ou **Syne** (peso 700–800, tracking apertado, tamanhos enormes).
  * Body: **JetBrains Mono** ou **DM Sans** (técnico, limpo).
* Contraste agressivo:

  * Títulos muito grandes.
  * Corpo bem legível, tamanho menor, peso mais leve.

### Atmosfera

* Fundo: nada chapado.
* Base: `#030305` (void escuro).
* Sobre isso:

  * radial gradients, mesh gradients, ruído sutil.
* Paleta:

  * Electric Blue `#3B82F6`
  * Cyber Purple `#8B5CF6`
  * Acid Green para detalhes pontuais.
* Cartões:

  * glassmorphism
  * bordas suaves
  * box-shadow com glow.

### Motion & Interatividade

* Usar **Framer Motion** para:

  * stagger na entrada:

    * logo → título → subtítulo → CTAs → tabs.
  * scroll animations:

    * elementos sobem, desfocam, aparecem aos poucos.
* Microinterações:

  * botões com efeito magnético ou leve “liquid hover”.
  * cartões com tilt 3D.
* Shader:

  * Usar React Three Fiber para um **background shader reativo ao mouse**, algo como:

    * ondas digitais
    * fumaça de partículas
    * starfield distorcido.

---

## 🧱 Componentes Obrigatórios

1. **ShaderBackground**

   * Primeiro componente: canvas WebGL/Three, atrás de tudo.
2. **Header**

   * Logo “IANIA IA NEWS” (texto + logo gerado)
   * Navegação: “Edição Atual”, “Por Categoria”, “Arquivo”, “Sobre”
   * Botão “Assinar Newsletter” com borda neon animada.
3. **Tabs de Conteúdo**

   * Controle de aba com animação (Framer Motion).
4. **Hero da Edição Atual**

   * Título, subtítulo, data da semana.
   * Pequeno resumo da edição.
5. **Cards de “📊 Nesta Edição”**

   * Grid com as categorias + contagem de vídeos.
6. **Seções de Categoria (Edição Atual)**

   * Accordion ou blocos com smooth expand.
   * Lista de vídeos em cards.
7. **Bento Grid de Categorias (Tab “Por Categoria”)**

   * Cards grandes com imagens multimodais e resumo.
8. **Arquivo de Edições**

   * Lista/timeline de edições (mock, pode ser dados estáticos).
9. **Seção “Por que IANIA IA NEWS?”**

   * Comparação “Antes / Depois”:

     * Velho jeito (feeds caóticos)
     * Novo jeito (curadoria estruturada por IA).
10. **Footer**

    * Marquee: “let’s build the AI future” / frase em PT.
    * Links, redes, contatos.

---

## 🔧 Requisitos Técnicos

* Usar:

  * `lucide-react` para ícones.
  * `framer-motion` para todas as animações principais.
  * `clsx` + `tailwind-merge` para composição de classes.
* Layout:

  * Mobile-first, responsivo.
  * Evitar layout Bootstrap básico/centrado.
* Código:

  * Começar definindo o **componente de shader**.
  * Depois componentes de UI (Header, Tabs, Cards, etc.).
  * Por fim, montar a página principal (ex.: `app/page.tsx` ou `app/(site)/page.tsx`).
* Comentar nos pontos onde:

  * a newsletter real será injetada (props/data).
  * a geração multimodal de imagens será plugar.

---

