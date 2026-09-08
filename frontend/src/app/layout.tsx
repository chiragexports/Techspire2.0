import type { Metadata } from 'next';
import './globals.css';
import { AuthProvider } from '@/lib/auth-context';
import { ToastProvider } from '@/components/Toast';
import { Navbar } from '@/components/Navbar';
import { Footer } from '@/components/Footer';

export const metadata: Metadata = {
  title: 'Techspire — Master the Technologies That Build the Future',
  description:
    'The premier technical education platform for systems engineering, algorithms, database architectures, machine learning, and modern programming.',
  keywords: [
    'Techspire',
    'Python',
    'C Systems',
    'Modern C++',
    'SQL Databases',
    'Data Structures',
    'Algorithms',
    'Machine Learning',
    'Operating Systems',
    'Technical Education'
  ],
  authors: [{ name: 'Techspire Engineering Academy' }],
  openGraph: {
    title: 'Techspire — Premium Technical Education',
    description: 'Master systems, algorithms, distributed databases, and artificial intelligence.',
    type: 'website',
    url: 'https://techspire.io',
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link
          href="https://fonts.googleapis.com/css2?family=Alex+Brush&family=Cinzel:wght@600;700;800;900&family=Cormorant+Garamond:wght@600;700&family=Great+Vibes&family=JetBrains+Mono:wght@400;500;600;700&family=Montserrat:wght@400;500;600;700;800;900&family=Pinyon+Script&family=Playfair+Display:ital,wght@0,600;0,700;0,800;1,600&display=swap"
          rel="stylesheet"
        />
      </head>
      <body className="min-h-screen flex flex-col bg-[#07090E] text-slate-100 antialiased selection:bg-cyan-500/30 selection:text-cyan-200">
        <AuthProvider>
          <ToastProvider>
            <Navbar />
            <main className="flex-1 w-full">{children}</main>
            <Footer />
          </ToastProvider>
        </AuthProvider>
      </body>
    </html>
  );
}
