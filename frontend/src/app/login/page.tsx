'use client';

import React, { useState, useEffect, Suspense } from 'react';
import Link from 'next/link';
import { useRouter, useSearchParams } from 'next/navigation';
import {
  Lock,
  Mail,
  ArrowRight,
  ShieldCheck,
  Sparkles,
  User,
  AlertCircle,
} from 'lucide-react';
import { useAuth } from '@/lib/auth-context';
import { useToast } from '@/components/Toast';

function LoginContent() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const redirectUrl = searchParams.get('redirect') || '/dashboard';

  const { login, isAuthenticated } = useAuth();
  const { success, error: toastError } = useToast();

  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState('');

  useEffect(() => {
    if (isAuthenticated) {
      router.push(redirectUrl);
    }
  }, [isAuthenticated, redirectUrl, router]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!email || !password) {
      setErrorMsg('Please enter both email and password.');
      return;
    }

    setIsLoading(true);
    setErrorMsg('');

    try {
      const user = await login(email, password);
      success(`Welcome back, ${user.first_name || user.username}!`);
      router.push(redirectUrl);
    } catch (err: any) {
      setErrorMsg(err.message || 'Invalid email or password.');
      toastError(err.message || 'Login failed');
    } finally {
      setIsLoading(false);
    }
  };

  const handleDemoLogin = async (demoEmail: string, demoPass: string) => {
    setEmail(demoEmail);
    setPassword(demoPass);
    setIsLoading(true);
    setErrorMsg('');

    try {
      const user = await login(demoEmail, demoPass);
      success(`Logged in as ${user.role.toUpperCase()} (${user.email})`);
      if (user.role === 'admin') {
        router.push('/admin');
      } else {
        router.push(redirectUrl);
      }
    } catch (err: any) {
      setErrorMsg(err.message || 'Demo login failed');
      toastError(err.message || 'Demo login failed');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-[85vh] bg-[#07090E] flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        {/* Title */}
        <div className="text-center space-y-2">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-cyan-500/10 border border-cyan-500/30 text-xs font-mono text-cyan-400">
            <Sparkles className="w-3.5 h-3.5" />
            <span>Techspire Authentication</span>
          </div>
          <h1 className="text-3xl font-extrabold text-white tracking-tight">
            Sign In to Academy
          </h1>
          <p className="text-xs text-slate-400 font-mono">
            Access your courses, assessment transcripts, and certifications.
          </p>
        </div>

        {/* Demo Accounts Quick-Bar */}
        <div className="p-4 rounded-2xl bg-slate-900/90 border border-slate-800 space-y-2">
          <span className="text-[11px] font-mono text-slate-400 uppercase tracking-wider block">
            1-Click Demo Credentials:
          </span>
          <div className="grid grid-cols-2 gap-2">
            <button
              type="button"
              onClick={() => handleDemoLogin('student@techspire.io', 'student123456')}
              className="px-3 py-2 rounded-xl bg-slate-950 border border-slate-800 hover:border-cyan-500/50 text-xs font-mono text-cyan-300 flex items-center justify-center gap-1.5 transition-all"
            >
              <User className="w-3.5 h-3.5" />
              <span>Student Demo</span>
            </button>
            <button
              type="button"
              onClick={() => handleDemoLogin('admin@techspire.io', 'admin123456')}
              className="px-3 py-2 rounded-xl bg-slate-950 border border-slate-800 hover:border-amber-500/50 text-xs font-mono text-amber-300 flex items-center justify-center gap-1.5 transition-all"
            >
              <ShieldCheck className="w-3.5 h-3.5" />
              <span>Admin Demo</span>
            </button>
          </div>
        </div>

        {/* Login Form */}
        <form
          onSubmit={handleSubmit}
          className="p-8 rounded-3xl bg-slate-900/70 border border-slate-800 shadow-2xl space-y-5"
        >
          {errorMsg && (
            <div className="p-3 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-300 text-xs flex items-center gap-2">
              <AlertCircle className="w-4 h-4 shrink-0" />
              <span>{errorMsg}</span>
            </div>
          )}

          <div className="space-y-1.5">
            <label className="text-xs font-mono text-slate-300">Email or Username</label>
            <div className="relative">
              <Mail className="w-4 h-4 text-slate-500 absolute left-3.5 top-3" />
              <input
                type="text"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="student@techspire.io"
                className="w-full pl-10 pr-4 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-sm text-slate-200 placeholder-slate-600 focus:outline-none focus:border-cyan-500"
              />
            </div>
          </div>

          <div className="space-y-1.5">
            <div className="flex items-center justify-between">
              <label className="text-xs font-mono text-slate-300">Password</label>
            </div>
            <div className="relative">
              <Lock className="w-4 h-4 text-slate-500 absolute left-3.5 top-3" />
              <input
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                className="w-full pl-10 pr-4 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-sm text-slate-200 placeholder-slate-600 focus:outline-none focus:border-cyan-500"
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={isLoading}
            className="w-full py-3.5 rounded-xl font-mono text-xs font-bold text-slate-950 bg-gradient-to-r from-cyan-400 to-cyan-300 hover:from-cyan-300 hover:to-cyan-200 shadow-[0_0_20px_rgba(6,182,212,0.4)] transition-all flex items-center justify-center gap-2 uppercase tracking-wider disabled:opacity-50"
          >
            <span>{isLoading ? 'Authenticating...' : 'Sign In'}</span>
            <ArrowRight className="w-4 h-4" />
          </button>

          <p className="text-center text-xs text-slate-400 pt-2">
            Don't have an account?{' '}
            <Link href="/register" className="text-cyan-400 hover:underline font-medium">
              Create student account
            </Link>
          </p>
        </form>
      </div>
    </div>
  );
}

export default function LoginPage() {
  return (
    <Suspense
      fallback={
        <div className="min-h-screen bg-[#07090E] flex items-center justify-center">
          <div className="w-10 h-10 rounded-full border-2 border-cyan-500 border-t-transparent animate-spin" />
        </div>
      }
    >
      <LoginContent />
    </Suspense>
  );
}
