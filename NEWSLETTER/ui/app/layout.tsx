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
      <body className="antialiased overflow-x-hidden">
        {/* Noise overlay para textura */}
        <div className="noise-overlay fixed inset-0 pointer-events-none z-50" />
        
        {children}
      </body>
    </html>
  );
}
