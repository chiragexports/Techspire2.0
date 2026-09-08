'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import {
  ShieldCheck,
  Users,
  BookOpen,
  Award,
  TrendingUp,
  Activity,
  PlusCircle,
  Search,
  ExternalLink,
  Layers,
  FileCode,
  ArrowRight,
} from 'lucide-react';
import { api } from '@/lib/api';
import { useAuth } from '@/lib/auth-context';
import { useToast } from '@/components/Toast';
import { AdminAnalytics } from '@/lib/types';
import { formatDate } from '@/lib/utils';

export default function AdminDashboardPage() {
  const router = useRouter();
  const { user, isAdmin, isAuthenticated, isLoading: authLoading } = useAuth();
  const { error: toastError } = useToast();

  const [analytics, setAnalytics] = useState<AdminAnalytics | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    if (!authLoading) {
      if (!isAuthenticated || !isAdmin) {
        router.push('/login?redirect=/admin');
        return;
      }
    }

    async function loadAnalytics() {
      try {
        const data = await api.get<AdminAnalytics>('/admin/analytics/overview/');
        setAnalytics(data);
      } catch (err: any) {
        toastError(err.message || 'Failed to load admin analytics');
      } finally {
        setIsLoading(false);
      }
    }

    if (isAuthenticated && isAdmin) {
      loadAnalytics();
    }
  }, [isAuthenticated, isAdmin, authLoading]);

  if (authLoading || isLoading) {
    return (
      <div className="min-h-[85vh] bg-[#07090E] flex items-center justify-center">
        <div className="flex flex-col items-center gap-4">
          <div className="w-10 h-10 rounded-full border-2 border-amber-500 border-t-transparent animate-spin" />
          <span className="text-xs font-mono text-slate-400">Loading Admin Control Suite...</span>
        </div>
      </div>
    );
  }

  const metrics = analytics?.metrics || {
    total_students: 0,
    total_courses: 0,
    total_chapters: 0,
    total_enrollments: 0,
    total_certificates: 0,
    total_attempts: 0,
    pass_rate: 0,
    completion_rate: 0,
  };

  return (
    <div className="min-h-screen bg-[#07090E] py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto space-y-12">
        {/* Header */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 p-8 rounded-3xl bg-gradient-to-r from-amber-950/30 via-slate-900 to-slate-950 border border-amber-500/30 shadow-xl">
          <div className="space-y-2">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-amber-500/10 border border-amber-500/30 text-xs font-mono text-amber-300">
              <ShieldCheck className="w-4 h-4" />
              <span>Techspire Principal Administration Suite</span>
            </div>
            <h1 className="text-2xl sm:text-4xl font-extrabold text-white">
              Academy Operations Hub
            </h1>
            <p className="text-xs sm:text-sm text-slate-400 font-mono">
              Live telemetry across students, curricula, examinations, and digital credentials.
            </p>
          </div>

          <div className="flex flex-wrap items-center gap-3">
            <Link
              href="/admin/payments"
              className="px-4 py-2.5 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-xs font-mono text-emerald-400 hover:bg-emerald-500/20 flex items-center gap-1.5 font-bold"
            >
              <TrendingUp className="w-3.5 h-3.5" />
              <span>Payments & Revenue</span>
            </Link>
            <Link
              href="/admin/courses"
              className="px-4 py-2.5 rounded-xl bg-slate-900 border border-slate-800 text-xs font-mono text-slate-200 hover:text-white hover:border-slate-700 flex items-center gap-1.5"
            >
              <Layers className="w-3.5 h-3.5 text-cyan-400" />
              <span>Curriculum Studio</span>
            </Link>
            <Link
              href="/admin/students"
              className="px-4 py-2.5 rounded-xl bg-amber-400 text-slate-950 font-mono text-xs font-bold uppercase hover:bg-amber-300 flex items-center gap-1.5"
            >
              <Users className="w-3.5 h-3.5" />
              <span>Inspect Students</span>
            </Link>
          </div>
        </div>

        {/* Telemetry Metrics Cards */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="p-6 rounded-2xl bg-slate-900/80 border border-slate-800 flex flex-col justify-between">
            <div className="flex items-center justify-between text-slate-400 text-xs font-mono">
              <span>Total Students</span>
              <Users className="w-4 h-4 text-cyan-400" />
            </div>
            <div className="text-3xl font-extrabold text-white mt-4 font-mono">
              {metrics.total_students}
            </div>
          </div>

          <div className="p-6 rounded-2xl bg-slate-900/80 border border-slate-800 flex flex-col justify-between">
            <div className="flex items-center justify-between text-slate-400 text-xs font-mono">
              <span>Enrollments</span>
              <BookOpen className="w-4 h-4 text-indigo-400" />
            </div>
            <div className="text-3xl font-extrabold text-white mt-4 font-mono">
              {metrics.total_enrollments}
            </div>
          </div>

          <div className="p-6 rounded-2xl bg-slate-900/80 border border-slate-800 flex flex-col justify-between">
            <div className="flex items-center justify-between text-slate-400 text-xs font-mono">
              <span>Certificates Minted</span>
              <Award className="w-4 h-4 text-amber-400" />
            </div>
            <div className="text-3xl font-extrabold text-white mt-4 font-mono">
              {metrics.total_certificates}
            </div>
          </div>

          <div className="p-6 rounded-2xl bg-slate-900/80 border border-slate-800 flex flex-col justify-between">
            <div className="flex items-center justify-between text-slate-400 text-xs font-mono">
              <span>Assessment Pass Rate</span>
              <TrendingUp className="w-4 h-4 text-emerald-400" />
            </div>
            <div className="text-3xl font-extrabold text-white mt-4 font-mono">
              {metrics.pass_rate}%
            </div>
          </div>
        </div>

        {/* Popular Tracks & Recent Activity */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          {/* Top Courses */}
          <div className="lg:col-span-6 p-6 rounded-3xl bg-slate-900/80 border border-slate-800 space-y-4">
            <h3 className="text-base font-bold text-white flex items-center gap-2">
              <Layers className="w-4 h-4 text-cyan-400" />
              <span>Curriculum Engagement Rank</span>
            </h3>

            <div className="space-y-3">
              {analytics?.top_courses && analytics.top_courses.length > 0 ? (
                analytics.top_courses.map((c, idx) => (
                  <div
                    key={c.id}
                    className="p-4 rounded-xl bg-slate-950 border border-slate-800/80 flex items-center justify-between gap-4"
                  >
                    <div className="flex items-center gap-3 truncate">
                      <span className="font-mono text-xs font-bold text-slate-500 w-5">
                        #{idx + 1}
                      </span>
                      <span className="text-sm font-semibold text-slate-200 truncate">
                        {c.title}
                      </span>
                    </div>

                    <div className="flex items-center gap-3 shrink-0 text-xs font-mono">
                      <span className="text-cyan-400 font-bold">{c.student_count} Students</span>
                      <Link
                        href={`/courses/${c.slug}`}
                        className="text-slate-400 hover:text-white"
                      >
                        <ExternalLink className="w-3.5 h-3.5" />
                      </Link>
                    </div>
                  </div>
                ))
              ) : (
                <p className="text-xs text-slate-500">No course data available.</p>
              )}
            </div>
          </div>

          {/* Recent Minted Certificates */}
          <div className="lg:col-span-6 p-6 rounded-3xl bg-slate-900/80 border border-slate-800 space-y-4">
            <h3 className="text-base font-bold text-white flex items-center gap-2">
              <Award className="w-4 h-4 text-amber-400" />
              <span>Recent Digital Credentials</span>
            </h3>

            <div className="space-y-3">
              {analytics?.recent_certificates && analytics.recent_certificates.length > 0 ? (
                analytics.recent_certificates.map((cert) => (
                  <div
                    key={cert.id}
                    className="p-4 rounded-xl bg-slate-950 border border-slate-800/80 flex items-center justify-between gap-4 text-xs font-mono"
                  >
                    <div>
                      <p className="font-bold text-slate-200">{cert.student_name}</p>
                      <p className="text-slate-400 text-[11px]">{cert.course_title}</p>
                    </div>

                    <div className="text-right">
                      <span className="text-emerald-400 font-bold">{cert.grade_percentage}%</span>
                      <Link
                        href={`/verify/${cert.certificate_code}`}
                        className="text-cyan-400 block hover:underline text-[10px]"
                      >
                        {cert.certificate_code}
                      </Link>
                    </div>
                  </div>
                ))
              ) : (
                <p className="text-xs text-slate-500">No certificates issued yet.</p>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
