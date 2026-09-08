'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import {
  ArrowRight,
  Terminal,
  Cpu,
  Database,
  Award,
  ShieldCheck,
  CheckCircle2,
  Sparkles,
  Layers,
  Code2,
  Check,
  Search,
  BookOpen,
} from 'lucide-react';
import { HeroInteractiveNodes } from '@/components/HeroInteractiveNodes';
import { CourseCard } from '@/components/CourseCard';
import { CodeBlock } from '@/components/CodeBlock';
import { api } from '@/lib/api';
import { Course } from '@/lib/types';

export default function HomePage() {
  const [courses, setCourses] = useState<Course[]>([]);
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [activeTabCode, setActiveTabCode] = useState<'python' | 'c' | 'sql'>('python');

  useEffect(() => {
    async function loadCourses() {
      try {
        const data = await api.get<{ results?: Course[] } | Course[]>('/courses/');
        if (Array.isArray(data)) {
          setCourses(data);
        } else if (data.results) {
          setCourses(data.results);
        }
      } catch {
        // Handled silently
      }
    }
    loadCourses();
  }, []);

  const sampleCodes = {
    python: `# Python 3.10+ Pattern Matching & Async Generators
async def event_stream_pipeline(queue: asyncio.Queue):
    while True:
        event = await queue.get()
        match event:
            case {"type": "DEPLOY", "cluster": str(c), "nodes": int(n)}:
                yield f"[K8s] Scaling {c} to {n} nodes"
            case {"type": "ERROR", "code": 500..599}:
                yield "[ALERT] Critical 5xx Gateway Outage"
            case _:
                continue`,
    c: `// Low-Level Virtual Memory Allocator & Mutex Lock
#include <sys/mman.h>
#include <pthread.h>

void* allocate_secure_page(size_t size) {
    void* addr = mmap(NULL, size, PROT_READ | PROT_WRITE,
                      MAP_ANONYMOUS | MAP_PRIVATE, -1, 0);
    if (addr == MAP_FAILED) return NULL;
    return addr; // Zero-fragmentation contiguous page
}`,
    sql: `-- Window Functions & Sub-Millisecond Index Query
SELECT 
    user_id,
    course_id,
    score,
    DENSE_RANK() OVER (PARTITION BY course_id ORDER BY score DESC) as rank
FROM assessments_assessmentattempt
WHERE passed = TRUE;`
  };

  const categories = [
    { id: 'all', name: 'All Curricula' },
    { id: 'languages', name: 'Programming Languages' },
    { id: 'systems', name: 'Systems Engineering' },
    { id: 'database', name: 'Database Systems' },
    { id: 'core', name: 'Computer Science Core' },
    { id: 'ai', name: 'Artificial Intelligence' },
  ];

  const filteredCourses = courses.filter((course) => {
    if (selectedCategory === 'all') return true;
    const catName = (course.category_name || '').toLowerCase();
    if (selectedCategory === 'languages') return catName.includes('language');
    if (selectedCategory === 'systems') return catName.includes('system') || catName.includes('c ');
    if (selectedCategory === 'database') return catName.includes('data') || catName.includes('database');
    if (selectedCategory === 'core') return catName.includes('core') || catName.includes('structure');
    if (selectedCategory === 'ai') return catName.includes('intelligence') || catName.includes('learning');
    return true;
  });

  return (
    <div className="flex flex-col min-h-screen">
      {/* =========================================================================
          1. HERO SECTION WITH INTERACTIVE COMPOSITION & DYNAMIC NODES
         ========================================================================= */}
      <section className="relative min-h-[90vh] flex items-center justify-center pt-16 pb-20 px-4 sm:px-6 lg:px-8 overflow-hidden bg-radial-gradient">
        {/* Dynamic Canvas Nodes */}
        <HeroInteractiveNodes />

        {/* Ambient Glows */}
        <div className="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[350px] bg-cyan-500/10 rounded-full blur-[140px] pointer-events-none" />
        <div className="absolute top-1/3 right-1/4 w-[400px] h-[300px] bg-indigo-600/10 rounded-full blur-[120px] pointer-events-none" />

        <div className="relative z-10 max-w-7xl mx-auto w-full">
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
            {/* Left Headline Column */}
            <div className="lg:col-span-7 space-y-8 text-left">
              {/* Badge */}
              <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-slate-900/90 border border-cyan-500/30 shadow-[0_0_20px_rgba(6,182,212,0.2)]">
                <span className="flex h-2 w-2 relative">
                  <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-cyan-400 opacity-75" />
                  <span className="relative inline-flex rounded-full h-2 w-2 bg-cyan-500" />
                </span>
                <span className="text-xs font-mono font-medium text-cyan-300 tracking-wider uppercase">
                  Techspire 2.0 • 9 Complete Engineering Curricula
                </span>
              </div>

              {/* Main Headline */}
              <div className="space-y-4">
                <h1 className="text-4xl sm:text-5xl lg:text-6xl font-extrabold tracking-tight text-white leading-[1.1]">
                  Master the technologies that{' '}
                  <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 via-sky-300 to-indigo-400">
                    build the future.
                  </span>
                </h1>
                <p className="text-base sm:text-lg text-slate-400 max-w-2xl leading-relaxed font-sans">
                  The rigorous technical academy for software architects. Deep dive into systems programming in C/C++, algorithms, distributed databases, operating system kernels, and machine learning foundations.
                </p>
              </div>

              {/* Action Buttons */}
              <div className="flex flex-wrap items-center gap-4 pt-2">
                <Link
                  href="/courses"
                  className="px-7 py-3.5 rounded-xl font-mono text-sm font-bold text-slate-950 bg-gradient-to-r from-cyan-400 via-cyan-300 to-cyan-400 hover:shadow-[0_0_30px_rgba(6,182,212,0.5)] transition-all flex items-center gap-2 group"
                >
                  <span>Explore 9 Flagship Tracks</span>
                  <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
                </Link>
                <Link
                  href="/register"
                  className="px-6 py-3.5 rounded-xl font-mono text-sm font-semibold text-slate-200 bg-slate-900/80 hover:bg-slate-800 border border-slate-700/80 hover:border-slate-600 transition-all flex items-center gap-2"
                >
                  <Sparkles className="w-4 h-4 text-cyan-400" />
                  <span>Start Learning Free</span>
                </Link>
              </div>

              {/* Feature Pills */}
              <div className="grid grid-cols-2 sm:grid-cols-3 gap-4 pt-4 border-t border-slate-800/80 text-xs font-mono text-slate-400">
                <div className="flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
                  <span>100% Original Content</span>
                </div>
                <div className="flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4 text-cyan-400 shrink-0" />
                  <span>Server-Validated Tests</span>
                </div>
                <div className="flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4 text-indigo-400 shrink-0" />
                  <span>SHA-256 Certificates</span>
                </div>
              </div>
            </div>

            {/* Right Interactive Code Terminal */}
            <div className="lg:col-span-5 relative">
              <div className="relative rounded-2xl p-1 bg-gradient-to-br from-cyan-500/30 via-indigo-500/20 to-transparent shadow-[0_20px_50px_rgba(0,0,0,0.6)]">
                <div className="bg-[#0B0F17] rounded-xl overflow-hidden border border-slate-800/90">
                  {/* Language Selector Bar */}
                  <div className="flex items-center justify-between px-4 py-3 bg-slate-900/90 border-b border-slate-800">
                    <div className="flex items-center gap-2">
                      <span className="w-3 h-3 rounded-full bg-rose-500" />
                      <span className="w-3 h-3 rounded-full bg-amber-500" />
                      <span className="w-3 h-3 rounded-full bg-emerald-500" />
                    </div>
                    <div className="flex items-center gap-1">
                      <button
                        onClick={() => setActiveTabCode('python')}
                        className={`px-2.5 py-1 rounded text-xs font-mono transition-colors ${
                          activeTabCode === 'python'
                            ? 'bg-cyan-500/20 text-cyan-300 border border-cyan-500/30'
                            : 'text-slate-400 hover:text-slate-200'
                        }`}
                      >
                        Python
                      </button>
                      <button
                        onClick={() => setActiveTabCode('c')}
                        className={`px-2.5 py-1 rounded text-xs font-mono transition-colors ${
                          activeTabCode === 'c'
                            ? 'bg-cyan-500/20 text-cyan-300 border border-cyan-500/30'
                            : 'text-slate-400 hover:text-slate-200'
                        }`}
                      >
                        C Systems
                      </button>
                      <button
                        onClick={() => setActiveTabCode('sql')}
                        className={`px-2.5 py-1 rounded text-xs font-mono transition-colors ${
                          activeTabCode === 'sql'
                            ? 'bg-cyan-500/20 text-cyan-300 border border-cyan-500/30'
                            : 'text-slate-400 hover:text-slate-200'
                        }`}
                      >
                        SQL
                      </button>
                    </div>
                  </div>

                  {/* Code Snippet View */}
                  <div className="p-4 font-mono text-xs text-cyan-200/90 leading-relaxed overflow-x-auto min-h-[220px]">
                    <pre>
                      <code>{sampleCodes[activeTabCode]}</code>
                    </pre>
                  </div>

                  {/* Terminal Execution Status */}
                  <div className="px-4 py-2.5 bg-slate-950/80 border-t border-slate-800/80 flex items-center justify-between text-xs font-mono">
                    <div className="flex items-center gap-2 text-emerald-400">
                      <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
                      <span>Syntax Verified • Django API Ready</span>
                    </div>
                    <span className="text-slate-500">O(1) Memory</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* =========================================================================
          2. FLAGSHIP CURRICULA SHOWCASE & LIVE FILTER
         ========================================================================= */}
      <section id="curriculum" className="py-24 px-4 sm:px-6 lg:px-8 bg-slate-950 relative border-t border-slate-900">
        <div className="max-w-7xl mx-auto space-y-12">
          {/* Section Header */}
          <div className="flex flex-col md:flex-row md:items-end justify-between gap-6">
            <div>
              <div className="flex items-center gap-2 text-xs font-mono text-cyan-400 uppercase tracking-widest mb-2">
                <Code2 className="w-4 h-4" />
                <span>Zero Shallow Tutorials</span>
              </div>
              <h2 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
                9 Engineering-Grade Curricula
              </h2>
              <p className="text-slate-400 text-sm mt-2 max-w-xl">
                Every course is engineered from first principles with full interactive notes, real code, diagrams, and comprehensive certification assessments.
              </p>
            </div>

            <Link
              href="/courses"
              className="inline-flex items-center gap-2 text-xs font-mono text-cyan-400 hover:text-cyan-300 uppercase tracking-wider"
            >
              <span>View All 9 Curricula</span>
              <ArrowRight className="w-4 h-4" />
            </Link>
          </div>

          {/* Category Filter Tabs */}
          <div className="flex flex-wrap items-center gap-2">
            {categories.map((cat) => (
              <button
                key={cat.id}
                onClick={() => setSelectedCategory(cat.id)}
                className={`px-4 py-2 rounded-xl text-xs font-mono transition-all ${
                  selectedCategory === cat.id
                    ? 'bg-cyan-500/20 text-cyan-300 border border-cyan-500/40 shadow-[0_0_15px_rgba(6,182,212,0.2)]'
                    : 'bg-slate-900/80 text-slate-400 border border-slate-800 hover:text-slate-200'
                }`}
              >
                {cat.name}
              </button>
            ))}
          </div>

          {/* Course Cards Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredCourses.map((course) => (
              <CourseCard key={course.id} course={course} />
            ))}
          </div>
        </div>
      </section>

      {/* =========================================================================
          3. THE TECHSPIRE LEARNING METHODOLOGY (ROADMAP PIPELINE)
         ========================================================================= */}
      <section className="py-24 px-4 sm:px-6 lg:px-8 bg-[#0B0F17] border-t border-slate-900 relative">
        <div className="max-w-7xl mx-auto space-y-16">
          <div className="text-center max-w-2xl mx-auto space-y-4">
            <span className="text-xs font-mono text-indigo-400 uppercase tracking-widest">
              Pedagogical Architecture
            </span>
            <h2 className="text-3xl sm:text-4xl font-extrabold text-white">
              The Techspire Learning Pipeline
            </h2>
            <p className="text-slate-400 text-sm">
              We reject shallow surface-level trivia. Every curriculum follows an uncompromised 5-stage progression designed for deep retention.
            </p>
          </div>

          {/* 5-Step Pipeline Grid */}
          <div className="grid grid-cols-1 md:grid-cols-5 gap-4 relative">
            {[
              {
                step: '01',
                title: 'Foundations',
                desc: 'Memory models, binary representation, and syntax invariants.',
                icon: Terminal,
                color: 'text-cyan-400',
              },
              {
                step: '02',
                title: 'Architecture',
                desc: 'Internal heap layout, pointers, call stacks, and CPU caches.',
                icon: Cpu,
                color: 'text-sky-400',
              },
              {
                step: '03',
                title: 'Implementation',
                desc: 'Writing clean, idiomatic algorithms and robust design patterns.',
                icon: Code2,
                color: 'text-indigo-400',
              },
              {
                step: '04',
                title: 'Assessment',
                desc: 'Server-evaluated exams with zero answer key leakage.',
                icon: Award,
                color: 'text-amber-400',
              },
              {
                step: '05',
                title: 'Certification',
                desc: 'Cryptographically verifiable credentials with unique hash signatures.',
                icon: ShieldCheck,
                color: 'text-emerald-400',
              },
            ].map((p, idx) => {
              const Icon = p.icon;
              return (
                <div
                  key={p.step}
                  className="p-6 rounded-2xl bg-slate-900/60 border border-slate-800/80 flex flex-col justify-between hover:border-slate-700 transition-all group"
                >
                  <div>
                    <div className="flex items-center justify-between mb-4">
                      <span className="font-mono text-2xl font-black text-slate-600 group-hover:text-cyan-400 transition-colors">
                        {p.step}
                      </span>
                      <Icon className={`w-5 h-5 ${p.color}`} />
                    </div>
                    <h3 className="text-base font-bold text-slate-100 mb-2">{p.title}</h3>
                    <p className="text-xs text-slate-400 leading-relaxed">{p.desc}</p>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* =========================================================================
          4. DIGITAL CERTIFICATION & PROOF OF MASTERY
         ========================================================================= */}
      <section className="py-24 px-4 sm:px-6 lg:px-8 bg-slate-950 border-t border-slate-900 relative">
        <div className="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
          <div className="lg:col-span-6 space-y-6">
            <span className="text-xs font-mono text-amber-400 uppercase tracking-widest">
              Verifiable Proof of Skill
            </span>
            <h2 className="text-3xl sm:text-4xl font-extrabold text-white leading-tight">
              Certificates backed by real, server-side evaluation.
            </h2>
            <p className="text-slate-400 text-sm leading-relaxed">
              Every certificate issued by Techspire is tied to an audited assessment score and a unique cryptographic verification hash. Employers and teams can verify authentic credentials publicly on <code className="text-cyan-300 bg-slate-900 px-1.5 py-0.5 rounded">/verify/[id]</code>.
            </p>

            <ul className="space-y-3 text-sm text-slate-300 font-mono text-xs">
              <li className="flex items-center gap-3">
                <Check className="w-4 h-4 text-emerald-400" />
                <span>SHA-256 Tamper-Proof Signature</span>
              </li>
              <li className="flex items-center gap-3">
                <Check className="w-4 h-4 text-cyan-400" />
                <span>Public Instant Verification URL</span>
              </li>
              <li className="flex items-center gap-3">
                <Check className="w-4 h-4 text-indigo-400" />
                <span>High-Resolution Print & PDF Ready Canvas</span>
              </li>
            </ul>

            <div className="pt-2">
              <Link
                href="/verify/TECHSPIRE-2026-SAMPLE"
                className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-slate-900 border border-slate-800 text-xs font-mono text-slate-200 hover:text-white hover:border-cyan-500/50 transition-all"
              >
                <span>Test Live Verification Endpoint</span>
                <ArrowRight className="w-4 h-4 text-cyan-400" />
              </Link>
            </div>
          </div>

          {/* Certificate Mockup Preview */}
          <div className="lg:col-span-6 relative">
            <div className="p-8 rounded-3xl bg-gradient-to-br from-slate-900 via-slate-950 to-black border border-amber-500/30 shadow-[0_0_40px_rgba(245,158,11,0.15)] relative overflow-hidden">
              <div className="absolute top-0 right-0 w-32 h-32 bg-amber-500/10 rounded-full blur-2xl pointer-events-none" />
              
              <div className="border border-amber-500/20 p-6 rounded-2xl bg-slate-950/60 backdrop-blur-md text-center space-y-4">
                <div className="inline-flex items-center justify-center w-12 h-12 rounded-2xl bg-amber-500/10 border border-amber-500/30 text-amber-400 mx-auto">
                  <Award className="w-6 h-6" />
                </div>
                <div>
                  <h4 className="font-mono text-[10px] tracking-widest text-amber-400 uppercase">
                    TECHSPIRE ACADEMY • CERTIFICATE OF MASTERY
                  </h4>
                  <p className="text-xl font-bold text-white mt-1">Alex Rivera</p>
                  <p className="text-xs text-slate-400 mt-1">Has demonstrated engineering competence in</p>
                  <p className="text-sm font-semibold text-cyan-300 font-mono mt-0.5">
                    Python Programming Mastery
                  </p>
                </div>

                <div className="flex items-center justify-between pt-4 border-t border-slate-800/80 text-[11px] font-mono text-slate-400">
                  <span>Score: 100.0%</span>
                  <span className="text-emerald-400 font-semibold">VALID CREDENTIAL</span>
                  <span>TECHSPIRE-2026-A1B2C3</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* =========================================================================
          5. FINAL HIGH-IMPACT CALL TO ACTION
         ========================================================================= */}
      <section className="py-24 px-4 sm:px-6 lg:px-8 bg-gradient-to-b from-slate-950 to-[#07090E] border-t border-slate-900 text-center relative overflow-hidden">
        <div className="max-w-4xl mx-auto space-y-8 relative z-10">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-cyan-500/10 border border-cyan-500/30 text-xs font-mono text-cyan-400">
            <Sparkles className="w-3.5 h-3.5" />
            <span>Start Building Real Systems Today</span>
          </div>

          <h2 className="text-4xl sm:text-5xl font-extrabold text-white tracking-tight">
            Ready to master software engineering from first principles?
          </h2>

          <p className="text-base text-slate-400 max-w-xl mx-auto">
            Join thousands of developers advancing their careers across systems, algorithms, databases, and AI.
          </p>

          <div className="flex flex-wrap items-center justify-center gap-4 pt-4">
            <Link
              href="/register"
              className="px-8 py-4 rounded-xl font-mono text-sm font-bold text-slate-950 bg-gradient-to-r from-cyan-400 via-cyan-300 to-cyan-400 hover:shadow-[0_0_35px_rgba(6,182,212,0.6)] transition-all uppercase tracking-wider"
            >
              Get Started Free
            </Link>
            <Link
              href="/courses"
              className="px-8 py-4 rounded-xl font-mono text-sm font-semibold text-slate-200 bg-slate-900 hover:bg-slate-800 border border-slate-800 transition-all"
            >
              Browse All Courses
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
}
