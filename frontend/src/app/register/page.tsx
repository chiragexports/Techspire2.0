'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import {
  Lock,
  Mail,
  User,
  ArrowRight,
  Sparkles,
  AlertCircle,
  CheckCircle2,
} from 'lucide-react';
import { useAuth } from '@/lib/auth-context';
import { useToast } from '@/components/Toast';

export default function RegisterPage() {
  const router = useRouter();
  const { register, isAuthenticated } = useAuth();
  const { success, error: toastError } = useToast();

  const [email, setEmail] = useState('');
  const [username, setUsername] = useState('');
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [password, setPassword] = useState('');
  const [passwordConfirm, setPasswordConfirm] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState('');

  useEffect(() => {
    if (isAuthenticated) {
      router.push('/dashboard');
    }
  }, [isAuthenticated, router]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!email || !password || !passwordConfirm) {
      setErrorMsg('Please complete all required fields.');
      return;
    }

    if (password !== passwordConfirm) {
      setErrorMsg('Passwords do not match.');
      return;
    }

    if (password.length < 6) {
      setErrorMsg('Password must be at least 6 characters.');
      return;
    }

    setIsLoading(true);
    setErrorMsg('');

    try {
      const uname = username.trim() || email.split('@')[0];
      await register(email, uname, password, firstName, lastName);
      success('Account created! Welcome to Techspire Academy.');
      router.push('/dashboard');
    } catch (err: any) {
      setErrorMsg(err.message || 'Registration failed.');
      toastError(err.message || 'Registration failed');
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
            <span>Join Techspire Academy</span>
          </div>
          <h1 className="text-3xl font-extrabold text-white tracking-tight">
            Create Engineer Account
          </h1>
          <p className="text-xs text-slate-400 font-mono">
            Get instant access to 9 full curricula, assessments, and certifications.
          </p>
        </div>

        {/* Register Form */}
        <form
          onSubmit={handleSubmit}
          className="p-8 rounded-3xl bg-slate-900/70 border border-slate-800 shadow-2xl space-y-4"
        >
          {errorMsg && (
            <div className="p-3 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-300 text-xs flex items-center gap-2">
              <AlertCircle className="w-4 h-4 shrink-0" />
              <span>{errorMsg}</span>
            </div>
          )}

          <div className="grid grid-cols-2 gap-3">
            <div className="space-y-1">
              <label className="text-xs font-mono text-slate-300">First Name</label>
              <input
                type="text"
                value={firstName}
                onChange={(e) => setFirstName(e.target.value)}
                placeholder="Alex"
                className="w-full px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-sm text-slate-200 placeholder-slate-600 focus:outline-none focus:border-cyan-500"
              />
            </div>
            <div className="space-y-1">
              <label className="text-xs font-mono text-slate-300">Last Name</label>
              <input
                type="text"
                value={lastName}
                onChange={(e) => setLastName(e.target.value)}
                placeholder="Rivera"
                className="w-full px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-sm text-slate-200 placeholder-slate-600 focus:outline-none focus:border-cyan-500"
              />
            </div>
          </div>

          <div className="space-y-1">
            <label className="text-xs font-mono text-slate-300">Email Address *</label>
            <div className="relative">
              <Mail className="w-4 h-4 text-slate-500 absolute left-3.5 top-3" />
              <input
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="alex@techspire.io"
                className="w-full pl-10 pr-4 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-sm text-slate-200 placeholder-slate-600 focus:outline-none focus:border-cyan-500"
              />
            </div>
          </div>

          <div className="space-y-1">
            <label className="text-xs font-mono text-slate-300">Username</label>
            <div className="relative">
              <User className="w-4 h-4 text-slate-500 absolute left-3.5 top-3" />
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="alex_dev"
                className="w-full pl-10 pr-4 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-sm text-slate-200 placeholder-slate-600 focus:outline-none focus:border-cyan-500"
              />
            </div>
          </div>

          <div className="space-y-1">
            <label className="text-xs font-mono text-slate-300">Password *</label>
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

          <div className="space-y-1">
            <label className="text-xs font-mono text-slate-300">Confirm Password *</label>
            <div className="relative">
              <Lock className="w-4 h-4 text-slate-500 absolute left-3.5 top-3" />
              <input
                type="password"
                required
                value={passwordConfirm}
                onChange={(e) => setPasswordConfirm(e.target.value)}
                placeholder="••••••••"
                className="w-full pl-10 pr-4 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-sm text-slate-200 placeholder-slate-600 focus:outline-none focus:border-cyan-500"
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={isLoading}
            className="w-full py-3.5 rounded-xl font-mono text-xs font-bold text-slate-950 bg-gradient-to-r from-cyan-400 to-cyan-300 hover:from-cyan-300 hover:to-cyan-200 shadow-[0_0_20px_rgba(6,182,212,0.4)] transition-all flex items-center justify-center gap-2 uppercase tracking-wider disabled:opacity-50 mt-2"
          >
            <span>{isLoading ? 'Creating Account...' : 'Get Started Free'}</span>
            <ArrowRight className="w-4 h-4" />
          </button>

          <p className="text-center text-xs text-slate-400 pt-2">
            Already registered?{' '}
            <Link href="/login" className="text-cyan-400 hover:underline font-medium">
              Sign in
            </Link>
          </p>
        </form>
      </div>
    </div>
  );
}
