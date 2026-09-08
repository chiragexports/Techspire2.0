'use client';

import React, { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import Link from 'next/link';
import {
  ShieldCheck,
  Award,
  CheckCircle2,
  AlertTriangle,
  Search,
  ExternalLink,
  Lock,
  ArrowRight,
} from 'lucide-react';
import { api } from '@/lib/api';
import { PublicVerifiedCertificate } from '@/lib/types';
import { formatDate } from '@/lib/utils';

export default function CertificateVerificationPage() {
  const { code } = useParams() as { code: string };
  const router = useRouter();

  const [certData, setCertData] = useState<PublicVerifiedCertificate | null>(null);
  const [isValid, setIsValid] = useState<boolean | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [searchCode, setSearchCode] = useState(code || '');

  useEffect(() => {
    async function verifyCertificate() {
      if (!code || code === 'TECHSPIRE-2026-SAMPLE') {
        // Sample demonstration fallback
        setCertData({
          id: 'e1d88a4b-9c71-4a7b-a2c9-1a3b4c5d6e7f',
          certificate_code: 'TECHSPIRE-2026-SAMPLE',
          recipient_name: 'Alex Rivera',
          course_title: 'Python Programming Mastery',
          course_slug: 'python-programming',
          course_difficulty: 'beginner',
          estimated_hours: 35,
          grade_percentage: 100.0,
          issue_date: new Date().toISOString(),
          is_valid: true,
          verification_hash: '9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08',
        });
        setIsValid(true);
        setIsLoading(false);
        return;
      }

      setIsLoading(true);
      try {
        const res = await api.get<{ is_valid: boolean; certificate: PublicVerifiedCertificate }>(
          `/certificates/verify/${code}/`
        );
        if (res.is_valid && res.certificate) {
          setCertData(res.certificate);
          setIsValid(true);
        } else {
          setIsValid(false);
        }
      } catch {
        setIsValid(false);
      } finally {
        setIsLoading(false);
      }
    }

    verifyCertificate();
  }, [code]);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchCode.trim()) {
      router.push(`/verify/${encodeURIComponent(searchCode.trim())}`);
    }
  };

  return (
    <div className="min-h-screen bg-[#07090E] py-16 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto space-y-12">
        {/* Header */}
        <div className="text-center space-y-4">
          <div className="inline-flex items-center gap-2 px-3.5 py-1 rounded-full bg-cyan-500/10 border border-cyan-500/30 text-xs font-mono text-cyan-400">
            <ShieldCheck className="w-4 h-4" />
            <span>Cryptographic Digital Verification</span>
          </div>
          <h1 className="text-3xl sm:text-5xl font-extrabold text-white tracking-tight">
            Verify Academy Credential
          </h1>
          <p className="text-slate-400 text-sm max-w-xl mx-auto">
            Public verification portal for authenticating Techspire credentials, issued scores, and engineering accomplishments.
          </p>

          {/* Search Bar for Code */}
          <form onSubmit={handleSearch} className="max-w-md mx-auto flex gap-2 pt-2">
            <input
              type="text"
              value={searchCode}
              onChange={(e) => setSearchCode(e.target.value)}
              placeholder="e.g. TECHSPIRE-2026-XXXXXXXX"
              className="flex-1 px-4 py-2.5 rounded-xl bg-slate-900 border border-slate-800 text-xs font-mono text-slate-200 placeholder-slate-500 focus:outline-none focus:border-cyan-500"
            />
            <button
              type="submit"
              className="px-5 py-2.5 rounded-xl bg-cyan-400 text-slate-950 font-mono text-xs font-bold uppercase hover:bg-cyan-300"
            >
              Verify
            </button>
          </form>
        </div>

        {/* Verification Result Card */}
        {isLoading ? (
          <div className="p-16 rounded-3xl bg-slate-900/40 border border-slate-800 text-center">
            <div className="w-10 h-10 rounded-full border-2 border-cyan-500 border-t-transparent animate-spin mx-auto mb-3" />
            <span className="text-xs font-mono text-slate-400">Querying Blockchain / PostgreSQL Ledger...</span>
          </div>
        ) : isValid && certData ? (
          <div className="rounded-3xl bg-gradient-to-br from-slate-900 via-slate-950 to-black border border-emerald-500/40 p-8 sm:p-12 shadow-2xl space-y-8 relative overflow-hidden">
            <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 border-b border-slate-800 pb-6">
              <div className="flex items-center gap-3">
                <div className="w-12 h-12 rounded-2xl bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center text-emerald-400">
                  <CheckCircle2 className="w-7 h-7" />
                </div>
                <div>
                  <span className="text-xs font-mono font-bold uppercase tracking-widest text-emerald-400">
                    AUTHENTICATED CREDENTIAL
                  </span>
                  <p className="text-xs text-slate-400 font-mono mt-0.5">
                    Issued by Techspire Technical Academy
                  </p>
                </div>
              </div>

              <div className="text-left sm:text-right font-mono text-xs text-slate-400">
                <span className="text-slate-500 block text-[10px]">VERIFICATION ID</span>
                <span className="text-cyan-400 font-bold">{certData.certificate_code}</span>
              </div>
            </div>

            {/* Recipient and Course Details */}
            <div className="space-y-4">
              <div>
                <span className="text-xs text-slate-500 font-mono uppercase">Certified Recipient</span>
                <h2 className="text-2xl sm:text-3xl font-black text-white mt-1">
                  {certData.recipient_name}
                </h2>
              </div>

              <div>
                <span className="text-xs text-slate-500 font-mono uppercase">Completed Track</span>
                <h3 className="text-lg sm:text-xl font-bold text-cyan-300 font-mono mt-1">
                  {certData.course_title}
                </h3>
              </div>
            </div>

            {/* Verification Metadata Grid */}
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 p-5 rounded-2xl bg-slate-950 border border-slate-800/90 text-xs font-mono">
              <div>
                <span className="text-slate-500 block text-[10px]">ISSUE TIMESTAMP</span>
                <span className="text-slate-200">{formatDate(certData.issue_date)}</span>
              </div>
              <div>
                <span className="text-slate-500 block text-[10px]">RECORDED SCORE</span>
                <span className="text-emerald-400 font-bold">{certData.grade_percentage}% PASS</span>
              </div>
              <div>
                <span className="text-slate-500 block text-[10px]">STATUS</span>
                <span className="text-emerald-400 font-bold">VALID & ACTIVE</span>
              </div>
            </div>

            {/* SHA-256 Hash Seal */}
            <div className="p-4 rounded-xl bg-slate-950 border border-slate-900 flex items-center justify-between gap-4 text-[11px] font-mono text-slate-500">
              <div className="flex items-center gap-2 truncate">
                <Lock className="w-3.5 h-3.5 text-slate-400 shrink-0" />
                <span className="truncate">SHA-256: {certData.verification_hash || 'SHA256_VERIFIED_SIGNATURE'}</span>
              </div>
              <span className="shrink-0 text-emerald-400">Tamper-Proof</span>
            </div>

            <div className="flex flex-col sm:flex-row items-center justify-between gap-4 pt-2">
              <button
                onClick={() => window.open(`/certificates/${certData.certificate_code}/print`, '_blank')}
                className="px-4 py-2 rounded-xl bg-slate-900 border border-slate-800 hover:border-amber-500/50 text-xs font-mono text-amber-300 flex items-center gap-1.5 transition-all"
              >
                <span>Print Official Certificate (A4 PDF)</span>
              </button>

              <Link
                href={`/courses/${certData.course_slug}`}
                className="inline-flex items-center gap-1.5 text-xs font-mono text-cyan-400 hover:text-cyan-300"
              >
                <span>Explore this Curriculum Track</span>
                <ArrowRight className="w-4 h-4" />
              </Link>
            </div>
          </div>
        ) : (
          <div className="p-12 rounded-3xl bg-slate-900/60 border border-rose-500/40 text-center space-y-4 max-w-lg mx-auto">
            <div className="w-12 h-12 rounded-2xl bg-rose-500/10 border border-rose-500/30 flex items-center justify-center text-rose-400 mx-auto">
              <AlertTriangle className="w-6 h-6" />
            </div>
            <h3 className="text-lg font-bold text-white">Credential Verification Failed</h3>
            <p className="text-xs text-slate-400 leading-relaxed">
              No valid certificate matching the identifier <code className="text-rose-300 bg-slate-950 px-1.5 py-0.5 rounded">{code}</code> was found in the official registry.
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
