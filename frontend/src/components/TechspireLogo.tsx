import React from 'react';
import Link from 'next/link';

interface TechspireLogoProps {
  className?: string;
  size?: 'sm' | 'md' | 'lg';
  showTagline?: boolean;
}

export function TechspireLogo({ className = '', size = 'md', showTagline = false }: TechspireLogoProps) {
  const sizeMap = {
    sm: { icon: 'w-7 h-7', text: 'text-lg', dot: 'w-1.5 h-1.5' },
    md: { icon: 'w-9 h-9', text: 'text-xl', dot: 'w-2 h-2' },
    lg: { icon: 'w-12 h-12', text: 'text-3xl', dot: 'w-2.5 h-2.5' }
  };

  const currentSize = sizeMap[size];

  return (
    <Link href="/" className={`inline-flex items-center gap-3 group select-none ${className}`}>
      {/* Geometric Techspire Monogram */}
      <div className={`relative ${currentSize.icon} flex items-center justify-center rounded-xl bg-slate-950 border border-cyan-500/30 shadow-[0_0_20px_rgba(6,182,212,0.25)] group-hover:border-cyan-400 group-hover:shadow-[0_0_30px_rgba(6,182,212,0.45)] transition-all duration-300`}>
        <div className="absolute inset-0 rounded-xl bg-gradient-to-br from-cyan-500/20 via-indigo-600/20 to-transparent opacity-80" />
        <svg
          viewBox="0 0 24 24"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
          className="w-3/5 h-3/5 text-cyan-400 group-hover:scale-110 transition-transform duration-300 relative z-10"
        >
          {/* Techspire Spire & Node Geometry */}
          <path
            d="M12 2L3 7V17L12 22L21 17V7L12 2Z"
            stroke="currentColor"
            strokeWidth="1.75"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
          <path
            d="M12 6V18M12 12L19 8M12 12L5 8"
            stroke="#818CF8"
            strokeWidth="1.5"
            strokeLinecap="round"
          />
          <circle cx="12" cy="12" r="2" fill="#22D3EE" />
        </svg>
      </div>

      {/* Brand Typography */}
      <div className="flex flex-col">
        <div className="flex items-center gap-1.5">
          <span className={`font-black tracking-wider text-slate-100 uppercase ${currentSize.text} font-mono group-hover:text-white transition-colors`}>
            Tech<span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-indigo-400">spire</span>
          </span>
          <span className={`${currentSize.dot} rounded-full bg-cyan-400 animate-pulse shadow-[0_0_8px_#22D3EE]`} />
        </div>
        {showTagline && (
          <span className="text-[10px] uppercase font-mono tracking-widest text-slate-400 -mt-1">
            Engineering Academy
          </span>
        )}
      </div>
    </Link>
  );
}
