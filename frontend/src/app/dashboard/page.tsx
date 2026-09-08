'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import {
  BookOpen,
  CheckCircle2,
  Award,
  TrendingUp,
  Play,
  Clock,
  Sparkles,
  ArrowRight,
  ShieldCheck,
  ChevronRight,
  Flame,
} from 'lucide-react';
import { api } from '@/lib/api';
import { useAuth } from '@/lib/auth-context';
import { useToast } from '@/components/Toast';
import { DashboardOverview } from '@/lib/types';
import { CourseCard } from '@/components/CourseCard';

export default function StudentDashboardPage() {
  const router = useRouter();
  const { user, isAuthenticated, isLoading: authLoading } = useAuth();
  const { error: toastError } = useToast();

  const [dashboardData, setDashboardData] = useState<DashboardOverview | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      router.push('/login?redirect=/dashboard');
      return;
    }

    async function loadDashboard() {
      try {
        const data = await api.get<DashboardOverview>('/dashboard/overview/');
        setDashboardData(data);
      } catch (err: any) {
        toastError(err.message || 'Failed to load cockpit data');
      } finally {
        setIsLoading(false);
      }
    }

    if (isAuthenticated) {
      loadDashboard();
    }
  }, [isAuthenticated, authLoading]);

  if (authLoading || isLoading) {
    return (
      <div className="min-h-[85vh] bg-[#07090E] flex items-center justify-center">
        <div className="flex flex-col items-center gap-4">
          <div className="w-10 h-10 rounded-full border-2 border-cyan-500 border-t-transparent animate-spin" />
          <span className="text-xs font-mono text-slate-400">Loading Student Cockpit...</span>
        </div>
      </div>
    );
  }

  const stats = dashboardData?.stats || {
    total_enrolled: 0,
    completed_courses: 0,
    certificates_earned: 0,
    average_score: 0,
    learning_streak_days: 1,
  };

  const continueItem = dashboardData?.continue_learning;

  return (
    <div className="min-h-screen bg-[#07090E] py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto space-y-12">
        {/* =====================================================================
            1. COCKPIT WELCOME & USER GREETING
           ===================================================================== */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 p-8 rounded-3xl bg-gradient-to-r from-slate-900 via-slate-950 to-[#0B0F17] border border-slate-800 shadow-xl">
          <div className="space-y-2">
            <div className="flex items-center gap-2 text-xs font-mono text-cyan-400 uppercase tracking-widest">
              <Sparkles className="w-4 h-4" />
              <span>Learning Command Center</span>
            </div>
            <h1 className="text-2xl sm:text-4xl font-extrabold text-white">
              Welcome back, {user?.first_name || user?.username || 'Engineer'}
            </h1>
            <p className="text-xs sm:text-sm text-slate-400 font-mono">
              {user?.headline || 'Active Software Engineer'} • {user?.email}
            </p>
          </div>

          <div className="flex items-center gap-3">
            <div className="flex items-center gap-2 px-4 py-2.5 rounded-2xl bg-amber-500/10 border border-amber-500/30 text-amber-300 font-mono text-xs font-bold">
              <Flame className="w-4 h-4 text-amber-400 fill-amber-400" />
              <span>{stats.learning_streak_days} Day Streak</span>
            </div>

            <Link
              href="/courses"
              className="px-5 py-2.5 rounded-2xl bg-cyan-400 text-slate-950 font-mono text-xs font-bold uppercase tracking-wider hover:bg-cyan-300 transition-colors"
            >
              Browse Catalog
            </Link>
          </div>
        </div>

        {/* =====================================================================
            2. COCKPIT TELEMETRY METRICS
           ===================================================================== */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="p-6 rounded-2xl bg-slate-900/80 border border-slate-800 flex flex-col justify-between">
            <div className="flex items-center justify-between text-slate-400 text-xs font-mono">
              <span>Enrolled Tracks</span>
              <BookOpen className="w-4 h-4 text-cyan-400" />
            </div>
            <div className="text-3xl font-extrabold text-white mt-4 font-mono">
              {stats.total_enrolled}
            </div>
          </div>

          <div className="p-6 rounded-2xl bg-slate-900/80 border border-slate-800 flex flex-col justify-between">
            <div className="flex items-center justify-between text-slate-400 text-xs font-mono">
              <span>Completed</span>
              <CheckCircle2 className="w-4 h-4 text-emerald-400" />
            </div>
            <div className="text-3xl font-extrabold text-white mt-4 font-mono">
              {stats.completed_courses}
            </div>
          </div>

          <div className="p-6 rounded-2xl bg-slate-900/80 border border-slate-800 flex flex-col justify-between">
            <div className="flex items-center justify-between text-slate-400 text-xs font-mono">
              <span>Certificates Minted</span>
              <Award className="w-4 h-4 text-amber-400" />
            </div>
            <div className="text-3xl font-extrabold text-white mt-4 font-mono">
              {stats.certificates_earned}
            </div>
          </div>

          <div className="p-6 rounded-2xl bg-slate-900/80 border border-slate-800 flex flex-col justify-between">
            <div className="flex items-center justify-between text-slate-400 text-xs font-mono">
              <span>Exam Average</span>
              <TrendingUp className="w-4 h-4 text-indigo-400" />
            </div>
            <div className="text-3xl font-extrabold text-white mt-4 font-mono">
              {stats.average_score}%
            </div>
          </div>
        </div>

        {/* =====================================================================
            3. CONTINUE LEARNING HERO COCKPIT CARD
           ===================================================================== */}
        {continueItem && continueItem.course && (
          <div className="p-8 rounded-3xl bg-gradient-to-r from-cyan-950/40 via-slate-900 to-slate-950 border border-cyan-500/40 shadow-2xl relative overflow-hidden">
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center relative z-10">
              <div className="lg:col-span-8 space-y-4">
                <div className="inline-flex items-center gap-2 px-3 py-1 rounded-md bg-cyan-500/20 text-cyan-300 border border-cyan-500/30 text-xs font-mono uppercase font-semibold">
                  <Play className="w-3 h-3 fill-cyan-300" />
                  <span>Resume Current Track</span>
                </div>

                <h2 className="text-2xl sm:text-3xl font-bold text-white">
                  {continueItem.course.title}
                </h2>

                {continueItem.next_up_chapter && (
                  <p className="text-sm text-slate-300 font-mono">
                    Next up: <span className="text-cyan-400">{continueItem.next_up_chapter.module_title}</span> • {continueItem.next_up_chapter.title}
                  </p>
                )}

                {/* Progress Bar */}
                <div className="space-y-1.5 pt-2 max-w-lg">
                  <div className="flex items-center justify-between text-xs font-mono text-slate-400">
                    <span>Course Progress</span>
                    <span className="text-cyan-400 font-bold">{continueItem.progress_percentage}%</span>
                  </div>
                  <div className="w-full h-2.5 rounded-full bg-slate-800 overflow-hidden">
                    <div
                      className="h-full bg-gradient-to-r from-cyan-400 to-indigo-500 rounded-full transition-all duration-500"
                      style={{ width: `${Math.max(continueItem.progress_percentage, 5)}%` }}
                    />
                  </div>
                </div>
              </div>

              <div className="lg:col-span-4 flex justify-end">
                {continueItem.next_up_chapter ? (
                  <Link
                    href={`/learn/${continueItem.course.slug}/${continueItem.next_up_chapter.slug}`}
                    className="w-full sm:w-auto px-8 py-4 rounded-2xl font-mono text-xs font-bold text-slate-950 bg-gradient-to-r from-cyan-400 to-cyan-300 hover:from-cyan-300 hover:to-cyan-200 shadow-[0_0_25px_rgba(6,182,212,0.4)] flex items-center justify-center gap-2 uppercase tracking-wider"
                  >
                    <Play className="w-4 h-4 fill-slate-950" />
                    <span>Continue Lesson</span>
                  </Link>
                ) : (
                  <Link
                    href={`/courses/${continueItem.course.slug}`}
                    className="w-full sm:w-auto px-8 py-4 rounded-2xl font-mono text-xs font-bold text-slate-950 bg-cyan-400 hover:bg-cyan-300"
                  >
                    Open Curriculum
                  </Link>
                )}
              </div>
            </div>
          </div>
        )}

        {/* =====================================================================
            4. ENROLLED COURSES GRID & RECENT TIMELINE
           ===================================================================== */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          {/* Enrolled Tracks */}
          <div className="lg:col-span-8 space-y-6">
            <div className="flex items-center justify-between">
              <h3 className="text-xl font-bold text-white flex items-center gap-2">
                <BookOpen className="w-5 h-5 text-cyan-400" />
                <span>My Active Curricula</span>
              </h3>
              <Link href="/courses" className="text-xs font-mono text-cyan-400 hover:text-cyan-300 flex items-center gap-1">
                <span>Browse More</span>
                <ChevronRight className="w-3.5 h-3.5" />
              </Link>
            </div>

            {dashboardData?.enrolled_courses && dashboardData.enrolled_courses.length > 0 ? (
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                {dashboardData.enrolled_courses.map((enrollment) => (
                  <div
                    key={enrollment.id}
                    className="p-6 rounded-2xl bg-slate-900/80 border border-slate-800 flex flex-col justify-between hover:border-slate-700 transition-all"
                  >
                    <div>
                      <span className="text-[10px] font-mono uppercase px-2 py-0.5 rounded bg-slate-800 text-cyan-300 border border-slate-700">
                        {enrollment.course.difficulty}
                      </span>
                      <h4 className="text-base font-bold text-white mt-2 line-clamp-1">
                        {enrollment.course.title}
                      </h4>
                    </div>

                    <div className="mt-4 pt-3 border-t border-slate-800/80 space-y-2">
                      <div className="flex items-center justify-between text-xs font-mono">
                        <span className="text-slate-400">Progress</span>
                        <span className="text-cyan-400 font-bold">{enrollment.progress_percentage}%</span>
                      </div>
                      <div className="w-full h-1.5 rounded-full bg-slate-800 overflow-hidden">
                        <div
                          className="h-full bg-cyan-400 rounded-full"
                          style={{ width: `${Math.max(enrollment.progress_percentage, 5)}%` }}
                        />
                      </div>

                      <div className="pt-2 flex justify-end">
                        <Link
                          href={`/courses/${enrollment.course.slug}`}
                          className="text-xs font-mono text-cyan-400 hover:underline inline-flex items-center gap-1"
                        >
                          <span>Go to Workspace</span>
                          <ArrowRight className="w-3 h-3" />
                        </Link>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="p-12 rounded-2xl bg-slate-900/40 border border-slate-800 text-center space-y-3">
                <p className="text-sm text-slate-400">You haven't enrolled in any tracks yet.</p>
                <Link
                  href="/courses"
                  className="inline-block px-5 py-2.5 rounded-xl bg-cyan-400 text-slate-950 font-mono text-xs font-bold uppercase"
                >
                  Explore 9 Free Curricula
                </Link>
              </div>
            )}
          </div>

          {/* Recent Activity Feed */}
          <div className="lg:col-span-4 p-6 rounded-3xl bg-slate-900/60 border border-slate-800 space-y-6">
            <h3 className="text-base font-bold text-white flex items-center gap-2">
              <Clock className="w-4 h-4 text-indigo-400" />
              <span>Recent Activity Feed</span>
            </h3>

            {dashboardData?.recent_activity && dashboardData.recent_activity.length > 0 ? (
              <div className="space-y-4">
                {dashboardData.recent_activity.map((act) => (
                  <div
                    key={act.id}
                    className="p-3.5 rounded-xl bg-slate-950 border border-slate-800/80 text-xs space-y-1"
                  >
                    <div className="flex items-center justify-between text-slate-500 font-mono text-[10px]">
                      <span>Completed Lesson</span>
                      <span>{new Date(act.completed_at).toLocaleDateString()}</span>
                    </div>
                    <p className="font-semibold text-slate-200">{act.chapter_title}</p>
                    <p className="text-cyan-400 text-[11px] font-mono">{act.course_title}</p>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-xs text-slate-500">No activity recorded yet. Start a lesson to build your momentum!</p>
            )}
          </div>
        </div>

        {/* =====================================================================
            5. PURCHASE & BILLING HISTORY SECTION
           ===================================================================== */}
        <div className="space-y-6">
          <div className="flex items-center justify-between">
            <h3 className="text-xl font-bold text-white flex items-center gap-2">
              <ShieldCheck className="w-5 h-5 text-emerald-400" />
              <span>Purchase History & Credential Invoices</span>
            </h3>
            <span className="text-xs font-mono text-slate-400">
              Official Tax Invoices & Payment IDs
            </span>
          </div>

          <BillingHistorySection />
        </div>
      </div>
    </div>
  );
}

function BillingHistorySection() {
  const [payments, setPayments] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadHistory() {
      try {
        const data = await api.get<any>('/payments/history/');
        const items = Array.isArray(data) ? data : Array.isArray(data?.results) ? data.results : [];
        setPayments(items);
      } catch {
        // Handled
      } finally {
        setLoading(false);
      }
    }
    loadHistory();
  }, []);

  if (loading) {
    return (
      <div className="p-8 rounded-2xl bg-slate-900/60 border border-slate-800 text-center text-xs font-mono text-slate-400">
        Loading billing transactions...
      </div>
    );
  }

  if (payments.length === 0) {
    return (
      <div className="p-8 rounded-2xl bg-slate-900/40 border border-slate-800 text-center space-y-2">
        <p className="text-xs font-mono text-slate-400">No payment records found.</p>
        <p className="text-[11px] text-slate-500">
          When you purchase premium tracks, official invoices with Razorpay transaction receipts will appear here.
        </p>
      </div>
    );
  }

  return (
    <div className="rounded-2xl bg-slate-900/80 border border-slate-800 overflow-hidden shadow-xl">
      <div className="overflow-x-auto">
        <table className="w-full text-left text-xs font-mono">
          <thead className="bg-slate-950/80 border-b border-slate-800 text-slate-400 uppercase tracking-wider text-[10px]">
            <tr>
              <th className="p-4">Track / Item</th>
              <th className="p-4">Amount Paid</th>
              <th className="p-4">Transaction ID</th>
              <th className="p-4">Order ID</th>
              <th className="p-4">Date</th>
              <th className="p-4">Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60">
            {payments.map((p) => (
              <tr key={p.id} className="hover:bg-slate-800/40 transition-colors">
                <td className="p-4 font-bold text-white max-w-xs truncate">
                  {p.course_title}
                </td>
                <td className="p-4 text-emerald-400 font-bold">
                  ₹{p.amount_in_rupees || (p.amount ? p.amount / 100 : 0)}
                </td>
                <td className="p-4 text-slate-300 text-[11px] font-mono">
                  {p.razorpay_payment_id}
                </td>
                <td className="p-4 text-slate-400 text-[11px] font-mono">
                  {p.order_id}
                </td>
                <td className="p-4 text-slate-400">
                  {new Date(p.created_at).toLocaleDateString()}
                </td>
                <td className="p-4">
                  <span className="px-2.5 py-0.5 rounded bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-[10px] font-bold uppercase">
                    {p.status}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
