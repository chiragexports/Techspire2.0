'use client';

import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { TechspireLogo } from './TechspireLogo';
import { ShieldCheck, Terminal, Cpu, Database, Award, ArrowUpRight } from 'lucide-react';

export function Footer() {
  const pathname = usePathname();

  if (pathname?.includes('/print')) {
    return null;
  }

  return (
    <footer className="w-full bg-slate-950 border-t border-slate-900 text-slate-400 text-sm relative z-10">
      {/* Top Banner */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-14">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-10">
          {/* Brand Column */}
          <div className="lg:col-span-2 space-y-4">
            <TechspireLogo size="md" showTagline />
            <p className="text-slate-400 text-sm leading-relaxed max-w-sm">
              The premium technical education academy engineered for deep systems, algorithm design, distributed computing, and artificial intelligence.
            </p>

            {/* Platform Health Status Indicator */}
            <div className="inline-flex items-center gap-2.5 px-3 py-1.5 rounded-full bg-slate-900/80 border border-emerald-500/30 text-xs font-mono text-emerald-400">
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-ping" />
              <span>All Systems Operational (DRF API v2.0)</span>
            </div>
          </div>

          {/* Curricula Column */}
          <div>
            <h4 className="text-xs font-mono font-bold text-slate-200 uppercase tracking-wider mb-4 flex items-center gap-1.5">
              <Terminal className="w-3.5 h-3.5 text-cyan-400" />
              <span>Curricula</span>
            </h4>
            <ul className="space-y-2.5 text-xs">
              <li>
                <Link href="/courses/python-programming" className="hover:text-cyan-300 transition-colors">
                  Python Programming Mastery
                </Link>
              </li>
              <li>
                <Link href="/courses/c-programming" className="hover:text-cyan-300 transition-colors">
                  C Systems Programming
                </Link>
              </li>
              <li>
                <Link href="/courses/cpp-programming" className="hover:text-cyan-300 transition-colors">
                  Modern C++ Architecture
                </Link>
              </li>
              <li>
                <Link href="/courses/sql-databases" className="hover:text-cyan-300 transition-colors">
                  SQL & Database Systems
                </Link>
              </li>
              <li>
                <Link href="/courses/data-structures" className="hover:text-cyan-300 transition-colors">
                  Data Structures & Algorithms
                </Link>
              </li>
              <li>
                <Link href="/courses/operating-systems" className="hover:text-cyan-300 transition-colors">
                  Operating Systems Internals
                </Link>
              </li>
            </ul>
          </div>

          {/* Engineering & AI */}
          <div>
            <h4 className="text-xs font-mono font-bold text-slate-200 uppercase tracking-wider mb-4 flex items-center gap-1.5">
              <Cpu className="w-3.5 h-3.5 text-indigo-400" />
              <span>Intelligence</span>
            </h4>
            <ul className="space-y-2.5 text-xs">
              <li>
                <Link href="/courses/ai-fundamentals" className="hover:text-indigo-300 transition-colors">
                  Artificial Intelligence
                </Link>
              </li>
              <li>
                <Link href="/courses/machine-learning" className="hover:text-indigo-300 transition-colors">
                  Machine Learning Modeling
                </Link>
              </li>
              <li>
                <Link href="/courses/oop-design-patterns" className="hover:text-indigo-300 transition-colors">
                  OOP & Design Patterns
                </Link>
              </li>
              <li>
                <Link href="/courses" className="hover:text-indigo-300 transition-colors inline-flex items-center gap-1">
                  <span>Browse All 9 Tracks</span>
                  <ArrowUpRight className="w-3 h-3" />
                </Link>
              </li>
            </ul>
          </div>

          {/* Platform & Verification */}
          <div>
            <h4 className="text-xs font-mono font-bold text-slate-200 uppercase tracking-wider mb-4 flex items-center gap-1.5">
              <Award className="w-3.5 h-3.5 text-amber-400" />
              <span>Credentials</span>
            </h4>
            <ul className="space-y-2.5 text-xs">
              <li>
                <Link href="/verify/TECHSPIRE-2026-SAMPLE" className="hover:text-amber-300 transition-colors">
                  Verify Digital Certificate
                </Link>
              </li>
              <li>
                <Link href="/dashboard" className="hover:text-amber-300 transition-colors">
                  Student Cockpit
                </Link>
              </li>
              <li>
                <Link href="/profile" className="hover:text-amber-300 transition-colors">
                  Profile & Transcripts
                </Link>
              </li>
              <li>
                <Link href="/login" className="hover:text-amber-300 transition-colors">
                  Academy Portal
                </Link>
              </li>
            </ul>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="mt-12 pt-8 border-t border-slate-900 flex flex-col sm:flex-row items-center justify-between gap-4 text-xs font-mono text-slate-400">
          <p>© 2026 TECHSPIRE Academy. Precision engineered for high-performance software architects.</p>
          <div className="flex items-center gap-6">
            <span className="flex items-center gap-1 text-slate-400">
              <ShieldCheck className="w-4 h-4 text-cyan-400" />
              <span>SHA-256 Verified Certificates</span>
            </span>
          </div>
        </div>
      </div>
    </footer>
  );
}
