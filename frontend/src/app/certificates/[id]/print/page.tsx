'use client';

import React, { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import Link from 'next/link';
import QRCode from 'qrcode';
import {
  Printer,
  ArrowLeft,
  ShieldCheck,
  CheckCircle2,
  Award,
} from 'lucide-react';
import { api } from '@/lib/api';
import { Certificate } from '@/lib/types';
import { formatDate } from '@/lib/utils';

interface CertificateData extends Certificate {
  course_difficulty?: string;
}

export default function CertificatePrintPage() {
  const { id } = useParams() as { id: string };
  const router = useRouter();

  const [cert, setCert] = useState<CertificateData | null>(null);
  const [qrDataUrl, setQrDataUrl] = useState<string>('');
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    async function fetchCert() {
      setIsLoading(true);
      try {
        let data: any = null;
        try {
          data = await api.get<Certificate>(`/certificates/${id}/`);
        } catch {
          const verifyRes = await api.get<{ certificate: any }>(`/certificates/verify/${id}/`);
          if (verifyRes && verifyRes.certificate) {
            data = {
              id: verifyRes.certificate.id,
              certificate_code: verifyRes.certificate.certificate_code,
              student_name: verifyRes.certificate.recipient_name,
              course_title: verifyRes.certificate.course_title,
              course_slug: verifyRes.certificate.course_slug,
              course_difficulty: verifyRes.certificate.course_difficulty || 'Advanced',
              grade_percentage: verifyRes.certificate.grade_percentage,
              issue_date: verifyRes.certificate.issue_date,
              is_valid: verifyRes.certificate.is_valid,
              verification_hash: verifyRes.certificate.verification_hash,
            };
          }
        }
        setCert(data);

        // Generate high-resolution verification QR code (400px source for razor-sharp large prints)
        if (data && data.certificate_code) {
          const origin = typeof window !== 'undefined' ? window.location.origin : 'https://techspire.io';
          const verifyUrl = `${origin}/verify/${data.certificate_code}`;
          const qrUrl = await QRCode.toDataURL(verifyUrl, {
            width: 400,
            margin: 1,
            color: {
              dark: '#0A0E17',
              light: '#FFFFFF',
            },
            errorCorrectionLevel: 'M',
          });
          setQrDataUrl(qrUrl);
        }
      } catch (err) {
        console.error('Failed to load certificate for printing', err);
      } finally {
        setIsLoading(false);
      }
    }

    if (id) {
      fetchCert();
    }
  }, [id]);

  const handlePrint = () => {
    window.print();
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-[#07090E] flex items-center justify-center">
        <div className="w-10 h-10 rounded-full border-2 border-cyan-500 border-t-transparent animate-spin" />
      </div>
    );
  }

  if (!cert) {
    return (
      <div className="min-h-screen bg-[#07090E] flex flex-col items-center justify-center p-8 text-center">
        <h2 className="text-xl font-bold text-white mb-2">Certificate Not Found</h2>
        <p className="text-xs text-slate-400 mb-6">Could not load the requested certificate record.</p>
        <Link
          href="/certificates"
          className="px-4 py-2 rounded-xl bg-cyan-500 text-slate-950 font-mono text-xs font-bold"
        >
          Return to Certificates
        </Link>
      </div>
    );
  }

  return (
    <div className="print-page-wrapper min-h-screen bg-[#07090E] text-slate-900 select-none">
      {/* =========================================================================
          1. WEB INTERACTIVE PRESENTATION (SCREEN ONLY)
         ========================================================================= */}
      <div className="print:hidden w-full min-h-screen flex flex-col items-center justify-center p-2 sm:p-4 md:p-6">
        {/* Action Toolbar */}
        <div className="no-print w-full max-w-5xl flex items-center justify-between gap-3 mb-3 z-20">
          <Link
            href="/certificates"
            className="px-4 py-2 rounded-xl bg-slate-900/90 border border-slate-800 text-xs font-mono text-slate-300 hover:text-white flex items-center gap-2 transition-all backdrop-blur-md hover:border-slate-700 shadow-sm"
          >
            <ArrowLeft className="w-4 h-4" />
            <span>Back to Portfolio</span>
          </Link>

          <div className="flex items-center gap-3">
            <span className="text-xs font-mono text-slate-400 hidden sm:inline">
              Official Technical Credential • A4 Landscape
            </span>
            <button
              onClick={handlePrint}
              className="px-6 py-2.5 rounded-xl bg-gradient-to-r from-cyan-500 via-blue-600 to-indigo-600 hover:from-cyan-400 hover:to-indigo-500 text-white font-mono text-xs font-black flex items-center gap-2 shadow-[0_0_25px_rgba(6,182,212,0.35)] transition-all uppercase cursor-pointer"
            >
              <Printer className="w-4 h-4" />
              <span>Print / Save as PDF</span>
            </button>
          </div>
        </div>

        {/* Web Certificate Canvas Screen View */}
        <CertificateScreen cert={cert} qrDataUrl={qrDataUrl} />
      </div>

      {/* =========================================================================
          2. DEDICATED A4 LANDSCAPE PRINT PRESENTATION (PRINT ONLY)
             Fills 96-98% of the 297mm x 210mm page with large, bold typography
         ========================================================================= */}
      <div className="hidden print:flex w-[297mm] h-[210mm] max-w-[297mm] max-h-[210mm] overflow-hidden p-0 m-0 box-border bg-white">
        <CertificatePrint cert={cert} qrDataUrl={qrDataUrl} />
      </div>
    </div>
  );
}

/* =========================================================================
   COMPONENT 1: CertificateScreen (Interactive Web Preview - Large & Bold)
   ========================================================================= */
function CertificateScreen({
  cert,
  qrDataUrl,
}: {
  cert: CertificateData;
  qrDataUrl: string;
}) {
  const levelText = (cert.course_difficulty || 'ADVANCED').toUpperCase();

  return (
    <div
      className="relative bg-[#FCFDFE] text-[#0B0F19] shadow-2xl flex flex-col justify-between overflow-hidden box-border w-full max-w-[960px] aspect-[1.414/1] min-h-[540px] sm:min-h-[620px] p-6 sm:p-8 md:p-10 rounded-sm"
      style={{
        boxShadow: '0 25px 70px rgba(0,0,0,0.7), 0 0 50px rgba(6,182,212,0.2)',
      }}
    >
      {/* Background Guilloche Security Texture */}
      <div
        className="absolute inset-0 pointer-events-none opacity-[0.035]"
        style={{
          backgroundImage: `radial-gradient(#06B6D4 1px, transparent 1px), radial-gradient(#0F172A 1px, #FCFDFE 1px)`,
          backgroundSize: '24px 24px',
          backgroundPosition: '0 0, 12px 12px',
        }}
      />

      {/* SVG Precision Circuit Borders */}
      <CircuitBorderSVG />

      {/* 1. Header Bar */}
      <div className="relative z-10 flex items-center justify-between border-b-[1.5px] border-slate-200 pb-2 px-3">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-[#0A0E17] border border-cyan-500/60 flex items-center justify-center text-cyan-400 shadow-md">
            <Award className="w-6 h-6 text-cyan-400" />
          </div>
          <div className="text-left">
            <span
              className="font-black text-base sm:text-lg tracking-[0.22em] text-[#0A0E17] block leading-none uppercase"
              style={{ fontFamily: "'Montserrat', sans-serif" }}
            >
              TECH<span className="text-[#0284C7]">SPIRE</span>
            </span>
            <span className="text-[9px] sm:text-[10px] font-mono tracking-[0.25em] text-[#64748B] block uppercase mt-0.5 font-bold">
              ACADEMY OF ADVANCED ENGINEERING
            </span>
          </div>
        </div>

        <div className="text-right font-mono">
          <span className="text-[8.5px] sm:text-[9.5px] text-[#64748B] tracking-wider uppercase block font-bold">
            CREDENTIAL ID
          </span>
          <span className="text-sm sm:text-base font-black text-[#0A0E17] tracking-tight">
            {cert.certificate_code}
          </span>
        </div>
      </div>

      {/* 2. Main Heading & Subtitle */}
      <div className="text-center relative z-10 pt-1.5">
        <h1
          className="text-2xl sm:text-3xl md:text-[34px] lg:text-[38px] font-black tracking-[0.16em] text-[#0A0E17] uppercase leading-tight"
          style={{ fontFamily: "'Montserrat', sans-serif" }}
        >
          CERTIFICATE OF COMPLETION
        </h1>
        <div className="inline-flex items-center gap-3 mt-1">
          <span className="h-[2px] w-10 bg-[#0284C7]" />
          <span className="text-[11px] sm:text-xs font-bold tracking-[0.28em] text-[#0284C7] uppercase font-mono">
            Professional Technical Credential
          </span>
          <span className="h-[2px] w-10 bg-[#0284C7]" />
        </div>
      </div>

      {/* 3. Recipient Citation Body */}
      <div className="text-center my-auto py-1 relative z-10 space-y-1 sm:space-y-1.5">
        <p className="text-xs sm:text-sm font-serif italic text-[#475569]">
          This is to certify that
        </p>

        {/* Student Full Name */}
        <div className="py-0.5">
          <h2
            className="text-3xl sm:text-4xl md:text-5xl lg:text-[46px] font-extrabold text-[#0A0E17] tracking-wide block leading-tight"
            style={{ fontFamily: "'Cinzel', 'Playfair Display', serif" }}
          >
            {cert.student_name || 'Software Engineer'}
          </h2>
        </div>

        <p className="text-xs sm:text-sm text-[#475569] max-w-xl mx-auto leading-relaxed">
          has successfully completed the requirements of
        </p>

        {/* Course Title */}
        <h3
          className="text-xl sm:text-2xl md:text-3xl font-black text-[#0369A1] tracking-tight px-4 leading-snug uppercase max-w-3xl mx-auto"
          style={{ fontFamily: "'Montserrat', sans-serif" }}
        >
          {cert.course_title}
        </h3>

        <p className="text-[10px] sm:text-xs font-mono tracking-[0.22em] text-[#64748B] uppercase font-bold">
          Technical Certification Program
        </p>
      </div>

      {/* 4. Metadata Badge Bar */}
      <div className="relative z-10 mx-auto w-full max-w-3xl bg-slate-100/90 border border-slate-300 rounded-lg p-3 my-1 grid grid-cols-4 gap-2 text-center font-mono shadow-xs">
        <div className="border-r border-slate-300 pr-2">
          <span className="text-[9px] text-[#64748B] uppercase block font-bold tracking-wider">LEVEL</span>
          <span className="text-xs sm:text-sm font-black text-[#0A0E17] uppercase block truncate">{levelText}</span>
        </div>
        <div className="border-r border-slate-300 pr-2">
          <span className="text-[9px] text-[#64748B] uppercase block font-bold tracking-wider">FINAL SCORE</span>
          <span className="text-xs sm:text-sm font-black text-[#059669] block">{cert.grade_percentage}%</span>
        </div>
        <div className="border-r border-slate-300 pr-2">
          <span className="text-[9px] text-[#64748B] uppercase block font-bold tracking-wider">ISSUE DATE</span>
          <span className="text-xs sm:text-sm font-black text-[#0A0E17] block truncate">{formatDate(cert.issue_date)}</span>
        </div>
        <div>
          <span className="text-[9px] text-[#64748B] uppercase block font-bold tracking-wider">STATUS</span>
          <span className="text-xs sm:text-sm font-black text-[#0284C7] block">VERIFIED</span>
        </div>
      </div>

      {/* 5. Footer: Verification QR + Seal + Signature */}
      <div className="grid grid-cols-3 items-end gap-3 relative z-10 pt-2 pb-2 sm:pb-3 border-t-[1.5px] border-slate-200 px-3">
        {/* QR Code */}
        <div className="flex items-center gap-3">
          {qrDataUrl ? (
            <img
              src={qrDataUrl}
              alt="Credential Verification QR"
              className="w-14 h-14 sm:w-16 sm:h-16 p-0.5 bg-white border border-slate-300 rounded-lg shadow-xs shrink-0"
            />
          ) : (
            <div className="w-14 h-14 bg-slate-100 border border-slate-300 rounded-lg flex items-center justify-center shrink-0">
              <ShieldCheck className="w-7 h-7 text-slate-400" />
            </div>
          )}
          <div className="text-left font-mono">
            <span
              className="text-[9px] sm:text-[10px] font-black tracking-widest text-[#0A0E17] uppercase block"
              style={{ fontFamily: "'Montserrat', sans-serif" }}
            >
              SCAN TO VERIFY
            </span>
            <span className="text-[8.5px] text-[#059669] font-bold block flex items-center gap-1 mt-0.5">
              <CheckCircle2 className="w-3 h-3 text-[#059669]" />
              <span>Verified Credential</span>
            </span>
            <span className="text-[8px] text-[#64748B] block truncate max-w-[140px] mt-0.5">
              techspire.io/verify/{cert.certificate_code}
            </span>
          </div>
        </div>

        {/* Academy Seal */}
        <div className="flex flex-col items-center justify-center text-center">
          <div className="w-12 h-12 sm:w-14 sm:h-14 rounded-full bg-[#0A0E17] border-2 border-cyan-500 shadow-md flex items-center justify-center text-cyan-400">
            <ShieldCheck className="w-6 h-6 text-cyan-400" />
          </div>
          <span className="text-[8px] font-mono tracking-[0.2em] text-[#0A0E17] font-black uppercase mt-1 block">
            OFFICIAL SEAL
          </span>
        </div>

        {/* Signature */}
        <div className="text-right flex flex-col items-end">
          <div className="w-40 sm:w-52 text-center">
            <span
              className="text-xl sm:text-2xl text-[#0A0E17] block leading-none font-serif italic pb-0.5"
              style={{ fontFamily: "'Pinyon Script', 'Alex Brush', cursive" }}
            >
              Techspire Academy
            </span>
            <div className="border-b-[1.5px] border-slate-800 w-full" />
            <span
              className="text-[9px] sm:text-[10px] font-black text-[#0A0E17] tracking-wider uppercase mt-1 block"
              style={{ fontFamily: "'Montserrat', sans-serif" }}
            >
              Techspire Academy
            </span>
            <span className="text-[8px] font-mono text-[#64748B] tracking-wider uppercase block">
              Authorized Issuer
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}

/* =========================================================================
   COMPONENT 2: CertificatePrint (Strict A4 Landscape Max-Coverage Output)
   ========================================================================= */
function CertificatePrint({
  cert,
  qrDataUrl,
}: {
  cert: CertificateData;
  qrDataUrl: string;
}) {
  const levelText = (cert.course_difficulty || 'ADVANCED').toUpperCase();

  return (
    <div
      className="relative w-[297mm] h-[210mm] max-w-[297mm] max-h-[210mm] bg-[#FCFDFE] text-[#0B0F19] flex flex-col justify-between overflow-hidden box-border p-[6mm_8mm]"
      style={{
        pageBreakInside: 'avoid',
        breakInside: 'avoid',
      }}
    >
      {/* Subtle Guilloche Security Texture */}
      <div
        className="absolute inset-0 pointer-events-none opacity-[0.04]"
        style={{
          backgroundImage: `radial-gradient(#06B6D4 1.2px, transparent 1.2px), radial-gradient(#0F172A 1.2px, #FCFDFE 1.2px)`,
          backgroundSize: '24px 24px',
          backgroundPosition: '0 0, 12px 12px',
        }}
      />

      {/* SVG Precision Circuit Borders (Outer frame pushed to 14/14 for maximum printable area) */}
      <CircuitBorderSVG />

      {/* =========================================================================
          1. TOP HEADER BAR: TECHSPIRE ACADEMY + CREDENTIAL ID
         ========================================================================= */}
      <div className="relative z-10 flex items-center justify-between border-b-[2px] border-slate-300 pb-2 px-4 pt-1">
        <div className="flex items-center gap-3.5">
          <div className="w-[12mm] h-[12mm] rounded-xl bg-[#0A0E17] border-[1.5px] border-cyan-500 flex items-center justify-center text-cyan-400">
            <Award className="w-7 h-7 text-cyan-400" />
          </div>
          <div className="text-left">
            <span
              className="font-black text-[16pt] tracking-[0.22em] text-[#0A0E17] block leading-none uppercase"
              style={{ fontFamily: "'Montserrat', sans-serif" }}
            >
              TECH<span className="text-[#0284C7]">SPIRE</span>
            </span>
            <span className="text-[9.5pt] font-mono tracking-[0.25em] text-[#475569] block uppercase mt-1 font-bold">
              ACADEMY OF ADVANCED ENGINEERING
            </span>
          </div>
        </div>

        <div className="text-right font-mono">
          <span className="text-[9pt] text-[#475569] tracking-wider uppercase block font-bold">
            CREDENTIAL ID
          </span>
          <span className="text-[14pt] font-black text-[#0A0E17] tracking-tight block">
            {cert.certificate_code}
          </span>
        </div>
      </div>

      {/* =========================================================================
          2. MAIN HEADING & SUBTITLE
         ========================================================================= */}
      <div className="text-center relative z-10 pt-1.5">
        <h1
          className="text-[34pt] font-black tracking-[0.18em] text-[#0A0E17] uppercase leading-tight"
          style={{ fontFamily: "'Montserrat', sans-serif" }}
        >
          CERTIFICATE OF COMPLETION
        </h1>
        <div className="inline-flex items-center gap-3.5 mt-1">
          <span className="h-[2px] w-12 bg-[#0284C7]" />
          <span className="text-[11pt] font-bold tracking-[0.28em] text-[#0284C7] uppercase font-mono">
            Professional Technical Credential
          </span>
          <span className="h-[2px] w-12 bg-[#0284C7]" />
        </div>
      </div>

      {/* =========================================================================
          3. RECIPIENT CITATION & COURSE CITATION BODY (LARGE & BOLD)
         ========================================================================= */}
      <div className="text-center my-auto py-1 relative z-10 space-y-1.5">
        <p className="text-[12pt] font-serif italic text-[#475569]">
          This is to certify that
        </p>

        {/* Student Full Name (Large 38-42pt Prestige Serif) */}
        <div className="py-0.5">
          <h2
            className="text-[38pt] font-extrabold text-[#0A0E17] tracking-wide block leading-tight"
            style={{ fontFamily: "'Cinzel', 'Playfair Display', serif" }}
          >
            {cert.student_name || 'Software Engineer'}
          </h2>
        </div>

        <p className="text-[11pt] text-[#475569] max-w-2xl mx-auto leading-relaxed">
          has successfully completed the requirements of
        </p>

        {/* Course Title (24-26pt Bold Technical Heading) */}
        <h3
          className="text-[24pt] font-black text-[#0369A1] tracking-tight px-6 leading-snug uppercase max-w-5xl mx-auto"
          style={{ fontFamily: "'Montserrat', sans-serif" }}
        >
          {cert.course_title}
        </h3>

        <p className="text-[10.5pt] font-mono tracking-[0.22em] text-[#475569] uppercase font-bold">
          Technical Certification Program
        </p>
      </div>

      {/* =========================================================================
          4. METADATA BADGE BAR (WIDE & PROMINENT)
         ========================================================================= */}
      <div className="relative z-10 mx-auto w-full max-w-[270mm] bg-slate-100/95 border-[2px] border-slate-300 rounded-xl p-3 my-1 grid grid-cols-4 gap-2 text-center font-mono">
        <div className="border-r-[1.5px] border-slate-300 pr-2">
          <span className="text-[9pt] text-[#475569] uppercase block font-bold tracking-wider">LEVEL</span>
          <span className="text-[13pt] font-black text-[#0A0E17] uppercase block truncate">{levelText}</span>
        </div>
        <div className="border-r-[1.5px] border-slate-300 pr-2">
          <span className="text-[9pt] text-[#475569] uppercase block font-bold tracking-wider">FINAL SCORE</span>
          <span className="text-[13pt] font-black text-[#059669] block">{cert.grade_percentage}%</span>
        </div>
        <div className="border-r-[1.5px] border-slate-300 pr-2">
          <span className="text-[9pt] text-[#475569] uppercase block font-bold tracking-wider">ISSUE DATE</span>
          <span className="text-[13pt] font-black text-[#0A0E17] block truncate">{formatDate(cert.issue_date)}</span>
        </div>
        <div>
          <span className="text-[9pt] text-[#475569] uppercase block font-bold tracking-wider">STATUS</span>
          <span className="text-[13pt] font-black text-[#0284C7] block">VERIFIED</span>
        </div>
      </div>

      {/* =========================================================================
          5. FOOTER: VERIFICATION QR + SEAL + AUTHORIZED ISSUER SIGNATURE
         ========================================================================= */}
      <div className="grid grid-cols-3 items-end gap-4 relative z-10 pt-2 border-t-[2px] border-slate-300 px-4 pb-1">
        {/* Left: Dynamic QR Code Verification (32mm x 32mm) */}
        <div className="flex items-center gap-3.5">
          {qrDataUrl ? (
            <img
              src={qrDataUrl}
              alt="Credential Verification QR"
              className="w-[32mm] h-[32mm] p-1 bg-white border-[1.5px] border-slate-400 rounded-lg shrink-0"
            />
          ) : (
            <div className="w-[32mm] h-[32mm] bg-slate-100 border-[1.5px] border-slate-400 rounded-lg flex items-center justify-center shrink-0">
              <ShieldCheck className="w-9 h-9 text-slate-400" />
            </div>
          )}
          <div className="text-left font-mono">
            <span
              className="text-[10pt] font-black tracking-widest text-[#0A0E17] uppercase block leading-tight"
              style={{ fontFamily: "'Montserrat', sans-serif" }}
            >
              SCAN TO VERIFY
            </span>
            <span className="text-[9pt] text-[#059669] font-bold block flex items-center gap-1.5 mt-0.5">
              <CheckCircle2 className="w-4 h-4 text-[#059669]" />
              <span>Verified Credential</span>
            </span>
            <span className="text-[8.5pt] text-[#475569] block truncate max-w-[150px] mt-0.5">
              techspire.io/verify/{cert.certificate_code}
            </span>
          </div>
        </div>

        {/* Center: Official Academy Seal Stamp */}
        <div className="flex flex-col items-center justify-center text-center">
          <div className="w-[24mm] h-[24mm] rounded-full bg-[#0A0E17] border-[2.5px] border-cyan-500 flex items-center justify-center text-cyan-400 shadow-md">
            <ShieldCheck className="w-8 h-8 text-cyan-400" />
          </div>
          <span className="text-[8.5pt] font-mono tracking-[0.22em] text-[#0A0E17] font-black uppercase mt-1 block">
            OFFICIAL SEAL
          </span>
        </div>

        {/* Right: Authorized Issuer Signature Section */}
        <div className="text-right flex flex-col items-end">
          <div className="w-[56mm] text-center">
            <span
              className="text-[20pt] text-[#0A0E17] block leading-none font-serif italic pb-1"
              style={{ fontFamily: "'Pinyon Script', 'Alex Brush', cursive" }}
            >
              Techspire Academy
            </span>
            <div className="border-b-[2px] border-slate-900 w-full" />
            <span
              className="text-[10pt] font-black text-[#0A0E17] tracking-wider uppercase mt-1 block"
              style={{ fontFamily: "'Montserrat', sans-serif" }}
            >
              Techspire Academy
            </span>
            <span className="text-[8pt] font-mono text-[#475569] tracking-wider uppercase block">
              Authorized Issuer
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}

/* =========================================================================
   CIRCUIT BORDER SVG (Vector precision border framing certificate perimeter)
   ========================================================================= */
function CircuitBorderSVG() {
  return (
    <svg
      className="absolute inset-0 w-full h-full pointer-events-none z-0"
      viewBox="0 0 1000 707"
      preserveAspectRatio="none"
      xmlns="http://www.w3.org/2000/svg"
    >
      {/* Outer Precision Border */}
      <rect
        x="14"
        y="14"
        width="972"
        height="679"
        fill="none"
        stroke="#0F172A"
        strokeWidth="3.5"
      />
      {/* Inner Electric Cyan Accent Border */}
      <rect
        x="22"
        y="22"
        width="956"
        height="663"
        fill="none"
        stroke="#06B6D4"
        strokeWidth="1.5"
        strokeOpacity="0.85"
      />

      {/* Corner Precision Angular Nodes (Top-Left) */}
      <path d="M 8 42 L 8 8 L 42 8" fill="none" stroke="#06B6D4" strokeWidth="3.5" />
      <circle cx="42" cy="8" r="3.5" fill="#06B6D4" />
      <circle cx="8" cy="42" r="3.5" fill="#06B6D4" />

      {/* Corner Precision Angular Nodes (Top-Right) */}
      <path d="M 958 8 L 992 8 L 992 42" fill="none" stroke="#06B6D4" strokeWidth="3.5" />
      <circle cx="958" cy="8" r="3.5" fill="#06B6D4" />
      <circle cx="992" cy="42" r="3.5" fill="#06B6D4" />

      {/* Corner Precision Angular Nodes (Bottom-Left) */}
      <path d="M 8 665 L 8 699 L 42 699" fill="none" stroke="#06B6D4" strokeWidth="3.5" />
      <circle cx="42" cy="699" r="3.5" fill="#06B6D4" />
      <circle cx="8" cy="665" r="3.5" fill="#06B6D4" />

      {/* Corner Precision Angular Nodes (Bottom-Right) */}
      <path d="M 958 699 L 992 699 L 992 665" fill="none" stroke="#06B6D4" strokeWidth="3.5" />
      <circle cx="958" cy="699" r="3.5" fill="#06B6D4" />
      <circle cx="992" cy="665" r="3.5" fill="#06B6D4" />
    </svg>
  );
}
