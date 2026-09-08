'use client';

import React, { useState } from 'react';
import { Check, Copy, Terminal } from 'lucide-react';

interface CodeBlockProps {
  code: string;
  language?: string;
  title?: string;
}

export function CodeBlock({ code, language = 'python', title }: CodeBlockProps) {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(code);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch {
      // Fallback
    }
  };

  const lines = code.trim().split('\n');

  return (
    <div className="my-6 rounded-2xl overflow-hidden border border-slate-800 bg-[#0B0F17] shadow-[0_10px_30px_rgba(0,0,0,0.5)] font-mono text-sm group">
      {/* Terminal Top Bar */}
      <div className="flex items-center justify-between px-4 py-3 bg-slate-900/90 border-b border-slate-800/80">
        <div className="flex items-center gap-2">
          <div className="flex items-center gap-1.5">
            <span className="w-3 h-3 rounded-full bg-rose-500/80 border border-rose-600 inline-block" />
            <span className="w-3 h-3 rounded-full bg-amber-500/80 border border-amber-600 inline-block" />
            <span className="w-3 h-3 rounded-full bg-emerald-500/80 border border-emerald-600 inline-block" />
          </div>
          {title ? (
            <span className="ml-3 text-xs text-slate-300 font-medium">{title}</span>
          ) : (
            <div className="ml-3 flex items-center gap-1.5 text-xs text-slate-400">
              <Terminal className="w-3.5 h-3.5 text-cyan-400" />
              <span>{language.toUpperCase()}</span>
            </div>
          )}
        </div>

        <button
          onClick={handleCopy}
          className="flex items-center gap-1.5 px-2.5 py-1 rounded-lg text-xs font-sans text-slate-300 hover:text-white bg-slate-800 hover:bg-slate-700 border border-slate-700/60 transition-all duration-200"
          title="Copy snippet"
        >
          {copied ? (
            <>
              <Check className="w-3.5 h-3.5 text-emerald-400" />
              <span className="text-emerald-400 font-medium">Copied!</span>
            </>
          ) : (
            <>
              <Copy className="w-3.5 h-3.5 text-slate-400 group-hover:text-cyan-400 transition-colors" />
              <span>Copy</span>
            </>
          )}
        </button>
      </div>

      {/* Code Area with Line Numbers */}
      <div className="p-4 overflow-x-auto text-slate-200 text-xs md:text-sm leading-relaxed">
        <table className="border-collapse w-full">
          <tbody>
            {lines.map((line, idx) => (
              <tr key={idx} className="hover:bg-slate-800/40 transition-colors">
                <td className="pr-4 py-0.5 text-right select-none text-slate-600 w-8 font-mono text-xs align-top">
                  {idx + 1}
                </td>
                <td className="py-0.5 whitespace-pre font-mono text-cyan-200/90 align-top">
                  {line || ' '}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
