# 🤖 IANIA IA NEWS

Portal editorial de newsletters de Inteligência Artificial com design AI-First digno de Awwwards.

## 🎨 Stack Tecnológica

- **Next.js 14** (App Router)
- **React 18**
- **TypeScript**
- **Tailwind CSS** (design system customizado)
- **Framer Motion** (animações fluidas)
- **React Three Fiber** (shader background WebGL)
- **Lucide React** (ícones)

## 🚀 Começar

```bash
# Instalar dependências
npm install

# Rodar em desenvolvimento
npm run dev

# Build para produção
npm run build

# Rodar produção
npm start
```

Abra [http://localhost:3000](http://localhost:3000) no navegador.

## 📁 Estrutura do Projeto

```
ui/
├── app/                    # Next.js App Router
│   ├── layout.tsx         # Layout raiz
│   ├── page.tsx           # Página principal
│   └── globals.css        # Estilos globais
├── components/            # Componentes React
│   ├── ShaderBackground.tsx
│   ├── Header.tsx
│   ├── Hero.tsx
│   ├── Tabs.tsx
│   ├── CategoryCard.tsx
│   ├── VideoCard.tsx
│   ├── BentoGrid.tsx
│   └── Footer.tsx
├── lib/                   # Utilitários
│   ├── types.ts          # TypeScript types
│   ├── utils.ts          # Helper functions
│   └── data.ts           # Mock data
└── public/               # Assets estáticos
```

## 🎨 Design System

### Cores

- **Void**: `#030305` (background escuro)
- **Electric Blue**: `#3B82F6`
- **Cyber Purple**: `#8B5CF6`
- **Acid Green**: `#10B981`

### Tipografia

- **Heading**: Space Grotesk (700-800)
- **Body**: DM Sans (400-700)
- **Mono**: JetBrains Mono (400-600)

### Componentes

- Glassmorphism cards
- Neon borders
- Glow effects
- 3D tilt animations
- Shader backgrounds

## 📊 Estrutura de Dados

```typescript
type Video = {
  video_id: string;
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
  emoji: string;
  name: string;
  description: string;
  videoCount: number;
  videos: Video[];
};

type Edition = {
  id: string;
  weekLabel: string;
  dateRange: string;
  tagline: string;
  categories: Category[];
};
```

## 🧬 Geração Multimodal

O sistema está preparado para integração com modelos multimodais (GPT-4o, Flux, SDXL) para gerar:

- Logo da marca IANIA IA NEWS
- Ícones/imagens para cada categoria
- Thumbnails personalizados (opcional)

## 📝 Licença

Projeto privado - IANIA IA NEWS © 2025
