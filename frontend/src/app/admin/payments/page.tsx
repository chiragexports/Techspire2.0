'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import {
  CreditCard,
  DollarSign,
  TrendingUp,
  ArrowUpRight,
  Search,
  Filter,
  RefreshCw,
  ArrowLeft,
  CheckCircle2,
  XCircle,
  AlertCircle,
  Users,
  BookOpen,
  Calendar,
} from 'lucide-react';
import { api } from '@/lib/api';
import { useAuth } from '@/lib/auth-context';
import { AdminPaymentAnalytics, AdminPaymentItem } from '@/lib/types';

export default function AdminPaymentsPage() {
  const router = useRouter();
  const { user, isAuthenticated, isLoading: authLoading } = useAuth();

  const [stats, setStats] = useState<AdminPaymentAnalytics | null>(null);
  const [payments, setPayments] = useState<AdminPaymentItem[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('');

  const isAdmin = user?.role === 'admin' || user?.is_staff || user?.is_superuser;

  useEffect(() => {
    if (!authLoading && (!isAuthenticated || !isAdmin)) {
      router.push('/login?redirect=/admin/payments');
      return;
    }

    if (isAuthenticated && isAdmin) {
      loadPaymentData();
    }
  }, [isAuthenticated, isAdmin, authLoading]);

  async function loadPaymentData() {
    setIsLoading(true);
    try {
      const [statsData, listData] = await Promise.all([
        api.get<AdminPaymentAnalytics>('/payments/admin/stats/'),
        api.get<any>('/payments/admin/list/'),
      ]);
      setStats(statsData);
      const items = Array.isArray(listData)
        ? listData
        : Array.isArray(listData?.results)
        ? listData.results
        : [];
      setPayments(items);
    } catch (err) {
      console.error('Failed to load admin payment data', err);
    } finally {
      setIsLoading(false);
    }
  }

  const safePayments = Array.isArray(payments) ? payments : [];
  const filteredPayments = safePayments.filter((p) => {
    const matchesSearch =
      !searchTerm ||
      p.student_email?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      p.student_name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      p.course_title?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      p.razorpay_payment_id?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      p.order_id?.toLowerCase().includes(searchTerm.toLowerCase());

    const matchesStatus = !statusFilter || p.status === statusFilter;

    return matchesSearch && matchesStatus;
  });

  if (authLoading || isLoading) {
    return (
      <div className="min-h-screen bg-[#07090E] flex items-center justify-center">
        <div className="w-10 h-10 rounded-full border-2 border-cyan-500 border-t-transparent animate-spin" />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#07090E] py-10 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto space-y-10">
        {/* Navigation & Header */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div className="space-y-1">
            <div className="flex items-center gap-3">
              <Link
                href="/admin"
                className="p-2 rounded-xl bg-slate-900 border border-slate-800 text-slate-400 hover:text-white transition-colors"
              >
                <ArrowLeft className="w-4 h-4" />
              </Link>
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-cyan-500/10 border border-cyan-500/30 text-xs font-mono text-cyan-400">
                <CreditCard className="w-3.5 h-3.5" />
                <span>Financial Telemetry</span>
              </div>
            </div>
            <h1 className="text-3xl font-extrabold text-white tracking-tight">
              Payments & Revenue Control
            </h1>
            <p className="text-xs text-slate-400">
              Real-time Razorpay transaction auditing, revenue telemetry, and course sales.
            </p>
          </div>

          <div className="flex items-center gap-3">
            <button
              onClick={loadPaymentData}
              className="px-4 py-2 rounded-xl bg-slate-900 border border-slate-800 hover:border-slate-700 text-xs font-mono text-slate-300 hover:text-white flex items-center gap-2 transition-all"
            >
              <RefreshCw className="w-3.5 h-3.5" />
              <span>Refresh Telemetry</span>
            </button>
            <Link
              href="/admin/courses"
              className="px-4 py-2 rounded-xl bg-cyan-500 text-slate-950 font-mono text-xs font-bold uppercase hover:bg-cyan-400 transition-colors"
            >
              Manage Course Pricing
            </Link>
          </div>
        </div>

        {/* =========================================================================
            1. REVENUE METRICS CARDS
           ========================================================================= */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {/* Total Revenue */}
          <div className="p-6 rounded-2xl bg-gradient-to-br from-slate-900 via-slate-950 to-slate-900 border border-slate-800 flex flex-col justify-between shadow-lg">
            <div className="flex items-center justify-between text-xs font-mono text-slate-400">
              <span>Total Revenue</span>
              <DollarSign className="w-4 h-4 text-emerald-400" />
            </div>
            <div className="mt-4">
              <div className="text-3xl font-black text-white font-mono">
                ₹{(stats?.total_revenue_in_rupees || 0).toLocaleString()}
              </div>
              <span className="text-[11px] font-mono text-emerald-400 mt-1 block">
                {stats?.successful_payments || 0} Successful Transactions
              </span>
            </div>
          </div>

          {/* This Month's Revenue */}
          <div className="p-6 rounded-2xl bg-gradient-to-br from-slate-900 via-slate-950 to-slate-900 border border-slate-800 flex flex-col justify-between shadow-lg">
            <div className="flex items-center justify-between text-xs font-mono text-slate-400">
              <span>Month Revenue</span>
              <TrendingUp className="w-4 h-4 text-cyan-400" />
            </div>
            <div className="mt-4">
              <div className="text-3xl font-black text-cyan-400 font-mono">
                ₹{(stats?.month_revenue_in_rupees || 0).toLocaleString()}
              </div>
              <span className="text-[11px] font-mono text-slate-400 mt-1 block">
                Current Calendar Month
              </span>
            </div>
          </div>

          {/* Today's Revenue */}
          <div className="p-6 rounded-2xl bg-gradient-to-br from-slate-900 via-slate-950 to-slate-900 border border-slate-800 flex flex-col justify-between shadow-lg">
            <div className="flex items-center justify-between text-xs font-mono text-slate-400">
              <span>Today's Revenue</span>
              <Calendar className="w-4 h-4 text-indigo-400" />
            </div>
            <div className="mt-4">
              <div className="text-3xl font-black text-white font-mono">
                ₹{(stats?.today_revenue_in_rupees || 0).toLocaleString()}
              </div>
              <span className="text-[11px] font-mono text-indigo-400 mt-1 block">
                Live 24-Hour Window
              </span>
            </div>
          </div>

          {/* Paid Enrollments */}
          <div className="p-6 rounded-2xl bg-gradient-to-br from-slate-900 via-slate-950 to-slate-900 border border-slate-800 flex flex-col justify-between shadow-lg">
            <div className="flex items-center justify-between text-xs font-mono text-slate-400">
              <span>Active Paid Students</span>
              <Users className="w-4 h-4 text-amber-400" />
            </div>
            <div className="mt-4">
              <div className="text-3xl font-black text-amber-400 font-mono">
                {stats?.paid_enrollments || 0}
              </div>
              <span className="text-[11px] font-mono text-slate-400 mt-1 block">
                {stats?.total_orders || 0} Total Orders Generated
              </span>
            </div>
          </div>
        </div>

        {/* =========================================================================
            2. TOP-SELLING COURSES TABLE
           ========================================================================= */}
        {stats?.top_selling_courses && stats.top_selling_courses.length > 0 && (
          <div className="p-6 rounded-2xl bg-slate-900/80 border border-slate-800 space-y-4">
            <h3 className="text-sm font-bold text-white font-mono uppercase tracking-wider flex items-center gap-2">
              <BookOpen className="w-4 h-4 text-cyan-400" />
              <span>Top Revenue Curricula</span>
            </h3>

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
              {stats.top_selling_courses.map((tc) => (
                <div
                  key={tc.course_id}
                  className="p-4 rounded-xl bg-slate-950 border border-slate-800/80 flex items-center justify-between"
                >
                  <div className="space-y-0.5 max-w-[180px]">
                    <p className="text-xs font-bold text-white truncate">{tc.course_title}</p>
                    <span className="text-[10px] font-mono text-slate-400">
                      {tc.total_sales} Sales
                    </span>
                  </div>
                  <div className="text-right font-mono font-bold text-emerald-400 text-sm">
                    ₹{tc.revenue_in_rupees.toLocaleString()}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* =========================================================================
            3. PAYMENTS TRANSACTION AUDIT TABLE & FILTERS
           ========================================================================= */}
        <div className="p-6 rounded-2xl bg-slate-900/80 border border-slate-800 space-y-5">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
            <h3 className="text-base font-bold text-white flex items-center gap-2">
              <CreditCard className="w-4 h-4 text-cyan-400" />
              <span>Transaction Audit Ledger</span>
            </h3>

            {/* Filter controls */}
            <div className="flex flex-wrap items-center gap-3">
              <div className="relative">
                <Search className="w-3.5 h-3.5 text-slate-500 absolute left-3 top-3" />
                <input
                  type="text"
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  placeholder="Search student, order, payment ID..."
                  className="pl-9 pr-3 py-1.5 rounded-xl bg-slate-950 border border-slate-800 text-xs font-mono text-slate-200 placeholder-slate-500 focus:outline-none focus:border-cyan-500 w-64"
                />
              </div>

              <select
                value={statusFilter}
                onChange={(e) => setStatusFilter(e.target.value)}
                className="px-3 py-1.5 rounded-xl bg-slate-950 border border-slate-800 text-xs font-mono text-slate-300 focus:outline-none focus:border-cyan-500"
              >
                <option value="">All Statuses</option>
                <option value="captured">Captured (Paid)</option>
                <option value="created">Created</option>
                <option value="failed">Failed</option>
                <option value="refunded">Refunded</option>
              </select>
            </div>
          </div>

          {/* Table */}
          {filteredPayments.length > 0 ? (
            <div className="overflow-x-auto rounded-xl border border-slate-800">
              <table className="w-full text-left text-xs font-mono">
                <thead className="bg-slate-950 border-b border-slate-800 text-slate-400 uppercase tracking-wider text-[10px]">
                  <tr>
                    <th className="p-3.5">Student</th>
                    <th className="p-3.5">Course Track</th>
                    <th className="p-3.5">Amount</th>
                    <th className="p-3.5">Payment ID</th>
                    <th className="p-3.5">Order ID</th>
                    <th className="p-3.5">Date</th>
                    <th className="p-3.5">Status</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/60 bg-slate-900/40">
                  {filteredPayments.map((p) => (
                    <tr key={p.id} className="hover:bg-slate-800/40 transition-colors">
                      <td className="p-3.5">
                        <span className="font-bold text-slate-200 block">{p.student_name}</span>
                        <span className="text-[10px] text-slate-400">{p.student_email}</span>
                      </td>
                      <td className="p-3.5 font-bold text-white max-w-xs truncate">
                        {p.course_title}
                      </td>
                      <td className="p-3.5 font-bold text-emerald-400">
                        ₹{(p.amount_in_rupees || (p.amount ? p.amount / 100 : 0)).toLocaleString()}
                      </td>
                      <td className="p-3.5 text-slate-300 text-[11px] select-all">
                        {p.razorpay_payment_id}
                      </td>
                      <td className="p-3.5 text-slate-400 text-[11px] select-all">
                        {p.order_id}
                      </td>
                      <td className="p-3.5 text-slate-400 whitespace-nowrap">
                        {new Date(p.created_at).toLocaleString()}
                      </td>
                      <td className="p-3.5">
                        <span
                          className={`px-2.5 py-0.5 rounded text-[10px] font-bold uppercase border ${
                            p.status === 'captured'
                              ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-400'
                              : p.status === 'failed'
                              ? 'bg-rose-500/10 border-rose-500/30 text-rose-400'
                              : 'bg-amber-500/10 border-amber-500/30 text-amber-400'
                          }`}
                        >
                          {p.status}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <div className="p-12 text-center text-xs font-mono text-slate-500 border border-slate-800 rounded-xl">
              No transactions match the selected filter criteria.
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
