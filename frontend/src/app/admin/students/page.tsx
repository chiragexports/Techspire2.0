'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import {
  Users,
  Search,
  ShieldCheck,
  Mail,
  Award,
  BookOpen,
  ArrowLeft,
  Calendar,
  CheckCircle2,
} from 'lucide-react';
import { api } from '@/lib/api';
import { useAuth } from '@/lib/auth-context';
import { useToast } from '@/components/Toast';
import { formatDate } from '@/lib/utils';

interface AdminUserItem {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  role: string;
  headline?: string;
  is_active: boolean;
  created_at: string;
  total_enrollments: number;
  total_certificates: number;
  total_attempts: number;
}

export default function AdminStudentsPage() {
  const router = useRouter();
  const { isAdmin, isAuthenticated, isLoading: authLoading } = useAuth();
  const { error: toastError } = useToast();

  const [students, setStudents] = useState<AdminUserItem[]>([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [roleFilter, setRoleFilter] = useState('');
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    if (!authLoading) {
      if (!isAuthenticated || !isAdmin) {
        router.push('/login?redirect=/admin/students');
        return;
      }
    }

    async function loadStudents() {
      setIsLoading(true);
      try {
        let query = '/auth/admin/users/?';
        if (searchTerm) query += `search=${encodeURIComponent(searchTerm)}&`;
        if (roleFilter) query += `role=${encodeURIComponent(roleFilter)}&`;

        const data = await api.get<{ results?: AdminUserItem[] } | AdminUserItem[]>(query);
        setStudents(Array.isArray(data) ? data : data.results || []);
      } catch (err: any) {
        toastError(err.message || 'Failed to load student registry');
      } finally {
        setIsLoading(false);
      }
    }

    if (isAuthenticated && isAdmin) {
      loadStudents();
    }
  }, [searchTerm, roleFilter, isAuthenticated, isAdmin, authLoading]);

  if (authLoading || isLoading) {
    return (
      <div className="min-h-[85vh] bg-[#07090E] flex items-center justify-center">
        <div className="w-10 h-10 rounded-full border-2 border-amber-500 border-t-transparent animate-spin" />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#07090E] py-10 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto space-y-8">
        {/* Header */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <Link
              href="/admin"
              className="p-2 rounded-xl bg-slate-900 border border-slate-800 text-slate-400 hover:text-white"
            >
              <ArrowLeft className="w-4 h-4" />
            </Link>
            <div>
              <h1 className="text-2xl font-bold text-white">Student & User Registry</h1>
              <p className="text-xs text-slate-400 font-mono">
                Inspect registered students, enrollment progression, and examination attempts.
              </p>
            </div>
          </div>

          {/* Search & Filter Bar */}
          <div className="flex items-center gap-3">
            <div className="relative">
              <Search className="w-3.5 h-3.5 text-slate-500 absolute left-3 top-3" />
              <input
                type="text"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                placeholder="Search students..."
                className="pl-9 pr-4 py-2 rounded-xl bg-slate-900 border border-slate-800 text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-cyan-500"
              />
            </div>

            <select
              value={roleFilter}
              onChange={(e) => setRoleFilter(e.target.value)}
              className="px-3 py-2 rounded-xl bg-slate-900 border border-slate-800 text-xs font-mono text-slate-300 focus:outline-none focus:border-cyan-500"
            >
              <option value="">All Roles</option>
              <option value="student">Students</option>
              <option value="admin">Administrators</option>
            </select>
          </div>
        </div>

        {/* Students Table */}
        <div className="rounded-3xl bg-slate-900/80 border border-slate-800 overflow-hidden shadow-xl">
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs font-mono">
              <thead className="bg-slate-950/80 text-slate-400 border-b border-slate-800">
                <tr>
                  <th className="p-4 pl-6">Student / Engineer</th>
                  <th className="p-4">Role</th>
                  <th className="p-4">Enrollments</th>
                  <th className="p-4">Exam Attempts</th>
                  <th className="p-4">Certificates</th>
                  <th className="p-4 pr-6">Joined Date</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60 text-slate-300">
                {students.map((st) => (
                  <tr key={st.id} className="hover:bg-slate-800/30 transition-colors">
                    <td className="p-4 pl-6">
                      <div className="flex items-center gap-3">
                        <div className="w-8 h-8 rounded-lg bg-gradient-to-tr from-cyan-500 to-indigo-600 flex items-center justify-center font-bold text-white text-xs">
                          {st.first_name ? st.first_name[0].toUpperCase() : st.username[0].toUpperCase()}
                        </div>
                        <div>
                          <p className="font-sans font-bold text-white text-sm">
                            {st.first_name ? `${st.first_name} ${st.last_name}` : st.username}
                          </p>
                          <p className="text-slate-400 text-[11px]">{st.email}</p>
                        </div>
                      </div>
                    </td>
                    <td className="p-4">
                      <span
                        className={`px-2 py-0.5 rounded text-[10px] uppercase font-bold ${
                          st.role === 'admin'
                            ? 'bg-amber-500/10 border border-amber-500/30 text-amber-400'
                            : 'bg-cyan-500/10 border border-cyan-500/30 text-cyan-400'
                        }`}
                      >
                        {st.role}
                      </span>
                    </td>
                    <td className="p-4 text-cyan-300 font-bold">{st.total_enrollments} Tracks</td>
                    <td className="p-4 text-indigo-300 font-bold">{st.total_attempts} Tests</td>
                    <td className="p-4 text-amber-300 font-bold">{st.total_certificates} Minted</td>
                    <td className="p-4 pr-6 text-slate-400">{formatDate(st.created_at)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}
