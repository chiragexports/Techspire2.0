'use client';

import React, { useState, useEffect, Suspense } from 'react';
import { useParams, useRouter, useSearchParams } from 'next/navigation';
import Link from 'next/link';
import {
  CheckCircle2,
  ArrowRight,
  ShieldCheck,
  Award,
  BookOpen,
  Receipt,
  Sparkles,
  Layers,
} from 'lucide-react';
import { api } from '@/lib/api';
import { Course } from '@/lib/types';

function PaymentSuccessContent() {
  const { slug } = useParams() as { slug: string };
  const searchParams = useSearchParams();
  const router = useRouter();

  const paymentId = searchParams.get('payment_id') || 'pay_live_2026_verified';
  const orderId = searchParams.get('order_id') || 'order_2026_verified';
  const rawAmount = searchParams.get('amount');

  const [course, setCourse] = useState<Course | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    async function fetchCourse() {
      try {
        const data = await api.get<Course>(`/courses/${slug}/`);
        setCourse(data);
      } catch (err) {
        console.error('Failed to load course details', err);
      } finally {
        setIsLoading(false);
      }
    }
    if (slug) {
      fetchCourse();
    }
  }, [slug]);

  const firstChapter = course?.modules?.[0]?.chapters?.[0];
  const amountDisplay = rawAmount
    ? `₹${Number(rawAmount).toLocaleString()}`
    : course?.price_in_rupees
    ? `₹${course.price_in_rupees.toLocaleString()}`
    : '₹1,499';

  return (
    <div className="min-h-screen bg-[#07090E] flex flex-col items-center justify-center p-4 sm:p-6 select-none">
      <div className="w-full max-w-xl rounded-3xl bg-slate-950 border border-slate-800 shadow-2xl p-8 sm:p-10 space-y-8 text-center relative overflow-hidden">
        {/* Glow ambient background */}
        <div className="absolute -top-24 left-1/2 -translate-x-1/2 w-64 h-64 rounded-full bg-cyan-500/20 blur-[100px] pointer-events-none" />

        {/* Success Icon Badge */}
        <div className="relative z-10 flex flex-col items-center space-y-3">
          <div className="w-16 h-16 rounded-2xl bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center text-emerald-400 shadow-[0_0_30px_rgba(16,185,129,0.25)]">
            <CheckCircle2 className="w-9 h-9 text-emerald-400" />
          </div>
          <span className="text-xs font-mono uppercase tracking-[0.25em] text-emerald-400 font-bold">
            Transaction Complete
          </span>
          <h1 className="text-2xl sm:text-3xl font-black text-white tracking-tight">
            Payment Successful!
          </h1>
          <p className="text-xs sm:text-sm text-slate-400 max-w-sm">
            Your course access and engineering workspace have been permanently unlocked.
          </p>
        </div>

        {/* Receipt Details Card */}
        <div className="relative z-10 p-5 rounded-2xl bg-slate-900/90 border border-slate-800 text-left space-y-3 font-mono text-xs shadow-inner">
          <div className="flex items-center justify-between pb-2.5 border-b border-slate-800">
            <span className="text-slate-400">Course Track</span>
            <span className="font-bold text-slate-200 text-right truncate max-w-[200px]">
              {course?.title || 'Technical Track'}
            </span>
          </div>

          <div className="flex items-center justify-between pb-2.5 border-b border-slate-800">
            <span className="text-slate-400">Amount Paid</span>
            <span className="font-bold text-emerald-400 text-sm">{amountDisplay}</span>
          </div>

          <div className="flex items-center justify-between pb-2.5 border-b border-slate-800">
            <span className="text-slate-400">Payment ID</span>
            <span className="font-mono text-slate-300 text-[11px] truncate max-w-[180px]">
              {paymentId}
            </span>
          </div>

          <div className="flex items-center justify-between pb-2.5 border-b border-slate-800">
            <span className="text-slate-400">Order ID</span>
            <span className="font-mono text-slate-300 text-[11px] truncate max-w-[180px]">
              {orderId}
            </span>
          </div>

          <div className="flex items-center justify-between">
            <span className="text-slate-400">Status</span>
            <span className="px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 font-bold text-[10px]">
              PAID • LIFETIME ACCESS
            </span>
          </div>
        </div>

        {/* Actions */}
        <div className="relative z-10 space-y-3">
          {firstChapter ? (
            <Link
              href={`/learn/${slug}/${firstChapter.slug}`}
              className="w-full py-4 rounded-xl font-mono text-xs font-black text-slate-950 bg-gradient-to-r from-cyan-400 via-cyan-300 to-teal-300 hover:from-cyan-300 hover:to-teal-200 shadow-[0_0_30px_rgba(6,182,212,0.45)] transition-all flex items-center justify-center gap-2 uppercase tracking-wider"
            >
              <span>Start Learning Now</span>
              <ArrowRight className="w-4 h-4" />
            </Link>
          ) : (
            <Link
              href="/dashboard"
              className="w-full py-4 rounded-xl font-mono text-xs font-black text-slate-950 bg-gradient-to-r from-cyan-400 via-cyan-300 to-teal-300 hover:from-cyan-300 hover:to-teal-200 shadow-[0_0_30px_rgba(6,182,212,0.45)] transition-all flex items-center justify-center gap-2 uppercase tracking-wider"
            >
              <span>Go to Learning Dashboard</span>
              <ArrowRight className="w-4 h-4" />
            </Link>
          )}

          <Link
            href="/dashboard"
            className="block py-2.5 text-xs font-mono text-slate-400 hover:text-white transition-colors"
          >
            View in Student Portfolio
          </Link>
        </div>
      </div>
    </div>
  );
}

export default function PaymentSuccessPage() {
  return (
    <Suspense
      fallback={
        <div className="min-h-screen bg-[#07090E] flex items-center justify-center">
          <div className="w-10 h-10 rounded-full border-2 border-cyan-500 border-t-transparent animate-spin" />
        </div>
      }
    >
      <PaymentSuccessContent />
    </Suspense>
  );
}
