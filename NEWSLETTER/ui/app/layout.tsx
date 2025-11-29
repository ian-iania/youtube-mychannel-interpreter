import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "IANIA IA NEWS | Curadoria Semanal de Inteligência Artificial",
  description:
    "Portal editorial de newsletters de IA. Curadoria semanal organizada por temas relevantes, com análises profundas e insights sobre o futuro da tecnologia.",
  keywords: [
    "inteligência artificial",
    "IA",
    "machine learning",
    "deep learning",
    "newsletter",
    "tecnologia",
    "inovação",
  ],
  authors: [{ name: "IANIA IA NEWS" }],
  openGraph: {
    title: "IANIA IA NEWS",
    description: "Curadoria semanal de Inteligência Artificial",
    type: "website",
    locale: "pt_BR",
  },
  twitter: {
    card: "summary_large_image",
    title: "IANIA IA NEWS",
    description: "Curadoria semanal de Inteligência Artificial",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="pt-BR" className="scroll-smooth">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link href="https://fonts.googleapis.com/css2?family=Pacifico&display=swap" rel="stylesheet" />
      </head>
      <body className="antialiased overflow-x-hidden">
        {/* Noise overlay para textura */}
        <div className="noise-overlay fixed inset-0 pointer-events-none z-50" />
        
        {children}
      </body>
    </html>
  );
}
