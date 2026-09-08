'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import {
  Award,
  ShieldCheck,
  Download,
  ExternalLink,
  Printer,
  Sparkles,
  BookOpen,
} from 'lucide-react';
import { api } from '@/lib/api';
import { useAuth } from '@/lib/auth-context';
import { Certificate } from '@/lib/types';
import { formatDate } from '@/lib/utils';

export default function CertificatesPage() {
  const router = useRouter();
  const { isAuthenticated, isLoading: authLoading } = useAuth();
  const [certificates, setCertificates] = useState<Certificate[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      router.push('/login?redirect=/certificates');
      return;
    }

    async function loadCertificates() {
      try {
        const data = await api.get<Certificate[]>('/certificates/my-certificates/');
        setCertificates(Array.isArray(data) ? data : []);
      } catch (err) {
        console.error('Failed to load certificates', err);
      } finally {
        setIsLoading(false);
      }
    }

    if (isAuthenticated) {
      loadCertificates();
    }
  }, [isAuthenticated, authLoading]);

  const handlePrint = (certId: string) => {
    window.open(`/certificates/${certId}/print`, '_blank');
  };

  if (authLoading || isLoading) {
    return (
      <div className="min-h-[85vh] bg-[#07090E] flex items-center justify-center">
        <div className="w-10 h-10 rounded-full border-2 border-cyan-500 border-t-transparent animate-spin" />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#07090E] py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto space-y-12">
        {/* Header */}
        <div className="space-y-3">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-amber-500/10 border border-amber-500/30 text-xs font-mono text-amber-300">
            <Award className="w-3.5 h-3.5" />
            <span>Digital Verifiable Credentials</span>
          </div>
          <h1 className="text-3xl sm:text-5xl font-extrabold text-white tracking-tight">
            My Certification Portfolio
          </h1>
          <p className="text-slate-400 text-sm max-w-2xl">
            Official proof of engineering competency issued by Techspire Academy. Every certificate includes an immutable verification signature.
          </p>
        </div>

        {/* Certificates Grid */}
        {certificates.length > 0 ? (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {certificates.map((cert) => (
              <div
                key={cert.id}
                className="rounded-3xl bg-gradient-to-br from-slate-900 via-slate-950 to-black border border-amber-500/30 p-8 shadow-2xl space-y-6 relative overflow-hidden"
              >
                {/* Gold Seal Header */}
                <div className="flex items-center justify-between border-b border-slate-800/80 pb-6">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-xl bg-amber-500/10 border border-amber-500/30 flex items-center justify-center text-amber-400">
                      <Award className="w-6 h-6" />
                    </div>
                    <div>
                      <span className="text-[10px] font-mono tracking-widest text-amber-400 uppercase font-bold">
                        TECHSPIRE ACADEMY
                      </span>
                      <p className="text-xs text-slate-400 font-mono">Certificate of Completion</p>
                    </div>
                  </div>

                  <span className="text-[11px] font-mono px-2.5 py-1 rounded bg-emerald-500/10 border border-emerald-500/30 text-emerald-400">
                    VERIFIED
                  </span>
                </div>

                {/* Main Body */}
                <div className="space-y-3">
                  <p className="text-xs text-slate-400">This is to certify that</p>
                  <h3 className="text-2xl font-black text-white">{cert.student_name || 'Software Engineer'}</h3>
                  <p className="text-xs text-slate-400">has successfully passed all requirements and examinations for</p>
                  <h4 className="text-lg font-bold text-cyan-300 font-mono">{cert.course_title}</h4>
                </div>

                {/* Meta details */}
                <div className="grid grid-cols-2 gap-4 p-4 rounded-xl bg-slate-950/80 border border-slate-800/80 text-xs font-mono text-slate-400">
                  <div>
                    <span className="text-slate-500 block text-[10px]">ISSUE DATE</span>
                    <span>{formatDate(cert.issue_date)}</span>
                  </div>
                  <div>
                    <span className="text-slate-500 block text-[10px]">FINAL GRADE</span>
                    <span className="text-emerald-400 font-bold">{cert.grade_percentage}%</span>
                  </div>
                  <div className="col-span-2 truncate">
                    <span className="text-slate-500 block text-[10px]">CERTIFICATE ID</span>
                    <span className="text-cyan-400">{cert.certificate_code}</span>
                  </div>
                </div>

                {/* Actions */}
                <div className="flex items-center justify-between pt-2">
                  <Link
                    href={`/verify/${cert.certificate_code}`}
                    className="inline-flex items-center gap-1.5 text-xs font-mono text-cyan-400 hover:text-cyan-300"
                  >
                    <span>Public Verification Link</span>
                    <ExternalLink className="w-3.5 h-3.5" />
                  </Link>

                  <button
                    onClick={() => handlePrint(cert.id)}
                    className="px-4 py-2 rounded-xl bg-slate-900 border border-slate-800 hover:border-slate-700 text-xs font-mono text-slate-300 hover:text-white flex items-center gap-1.5 transition-all"
                  >
                    <Printer className="w-3.5 h-3.5" />
                    <span>Print / Save PDF</span>
                  </button>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="p-16 rounded-3xl bg-slate-900/40 border border-slate-800 text-center space-y-4 max-w-md mx-auto">
            <div className="w-12 h-12 rounded-2xl bg-amber-500/10 border border-amber-500/30 flex items-center justify-center text-amber-400 mx-auto">
              <Award className="w-6 h-6" />
            </div>
            <h3 className="text-lg font-bold text-white">No Credentials Minted Yet</h3>
            <p className="text-xs text-slate-400">
              Complete any of the 9 flagship curricula and pass the final certification exam to earn your verified credential.
            </p>
            <Link
              href="/courses"
              className="inline-block px-5 py-2.5 rounded-xl bg-cyan-400 text-slate-950 font-mono text-xs font-bold uppercase"
            >
              Explore Curricula
            </Link>
          </div>
        )}
      </div>
    </div>
  );
}
