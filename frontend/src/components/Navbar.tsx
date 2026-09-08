'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import {
  Search,
  Menu,
  X,
  User as UserIcon,
  LogOut,
  LayoutDashboard,
  Award,
  ShieldCheck,
  BookOpen,
  ChevronDown,
} from 'lucide-react';
import { TechspireLogo } from './TechspireLogo';
import { useAuth } from '@/lib/auth-context';

export function Navbar() {
  const pathname = usePathname();
  const { user, isAuthenticated, isAdmin, logout } = useAuth();
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const [isUserMenuOpen, setIsUserMenuOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [isScrolled, setIsScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 20);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  // Close menus on route change
  useEffect(() => {
    setIsMobileMenuOpen(false);
    setIsUserMenuOpen(false);
  }, [pathname]);

  const navLinks = [
    { label: 'Courses', href: '/courses' },
    { label: 'Curriculum', href: '/#curriculum' },
    { label: 'Certificates', href: '/certificates' },
    { label: 'Verify', href: '/verify/TECHSPIRE-2026-SAMPLE' },
  ];

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      window.location.href = `/courses?search=${encodeURIComponent(searchQuery.trim())}`;
    }
  };

  // Hide Navbar completely on dedicated certificate print pages
  if (pathname?.includes('/print')) {
    return null;
  }

  return (
    <header
      className={`sticky top-0 z-40 w-full transition-all duration-300 ${
        isScrolled
          ? 'bg-slate-950/90 backdrop-blur-xl border-b border-slate-800/80 shadow-lg shadow-black/40'
          : 'bg-slate-950/60 backdrop-blur-md border-b border-slate-900/60'
      }`}
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-20 flex items-center justify-between gap-4">
        {/* Brand Logo */}
        <TechspireLogo size="md" />

        {/* Search Bar (Desktop) */}
        <form
          onSubmit={handleSearchSubmit}
          className="hidden md:flex items-center relative max-w-xs w-full"
        >
          <Search className="w-4 h-4 text-slate-500 absolute left-3.5 pointer-events-none" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search curricula, algorithms, SQL..."
            className="w-full pl-9 pr-4 py-1.5 rounded-full bg-slate-900/90 border border-slate-800 text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-cyan-500 focus:ring-1 focus:ring-cyan-500/50 transition-all"
          />
        </form>

        {/* Desktop Navigation Links */}
        <nav className="hidden lg:flex items-center gap-1">
          {navLinks.map((link) => {
            const isActive = pathname === link.href;
            return (
              <Link
                key={link.label}
                href={link.href}
                className={`px-3.5 py-2 rounded-lg text-sm font-medium transition-all ${
                  isActive
                    ? 'text-cyan-400 bg-cyan-500/10 border border-cyan-500/20'
                    : 'text-slate-300 hover:text-white hover:bg-slate-900/60'
                }`}
              >
                {link.label}
              </Link>
            );
          })}
        </nav>

        {/* Right CTA / Auth Profile */}
        <div className="hidden sm:flex items-center gap-3">
          {isAuthenticated && user ? (
            <div className="relative">
              <button
                onClick={() => setIsUserMenuOpen(!isUserMenuOpen)}
                className="flex items-center gap-2.5 px-3 py-1.5 rounded-xl bg-slate-900 border border-slate-800 hover:border-slate-700 transition-all text-left"
              >
                <div className="w-7 h-7 rounded-lg bg-gradient-to-tr from-cyan-500 to-indigo-600 flex items-center justify-center text-xs font-bold text-white shadow-sm">
                  {user.first_name ? user.first_name[0].toUpperCase() : user.username[0].toUpperCase()}
                </div>
                <div className="flex flex-col">
                  <span className="text-xs font-semibold text-slate-200 leading-tight max-w-[110px] truncate">
                    {user.first_name || user.username}
                  </span>
                  <span className="text-[10px] font-mono text-cyan-400 uppercase">
                    {user.role}
                  </span>
                </div>
                <ChevronDown className="w-3.5 h-3.5 text-slate-400" />
              </button>

              {/* User Dropdown HUD */}
              {isUserMenuOpen && (
                <div className="absolute right-0 mt-2 w-56 rounded-2xl bg-slate-900/95 border border-slate-800 shadow-2xl backdrop-blur-xl py-2 z-50 animate-in fade-in slide-in-from-top-2">
                  <div className="px-4 py-2 border-b border-slate-800">
                    <p className="text-xs font-semibold text-slate-200">{user.email}</p>
                    <p className="text-[11px] text-slate-400 font-mono mt-0.5">{user.headline || 'Engineer'}</p>
                  </div>

                  <Link
                    href="/dashboard"
                    className="flex items-center gap-2.5 px-4 py-2 text-xs text-slate-300 hover:text-white hover:bg-slate-800/80 transition-colors"
                  >
                    <LayoutDashboard className="w-4 h-4 text-cyan-400" />
                    <span>Learning Dashboard</span>
                  </Link>

                  <Link
                    href="/profile"
                    className="flex items-center gap-2.5 px-4 py-2 text-xs text-slate-300 hover:text-white hover:bg-slate-800/80 transition-colors"
                  >
                    <UserIcon className="w-4 h-4 text-indigo-400" />
                    <span>My Profile</span>
                  </Link>

                  <Link
                    href="/certificates"
                    className="flex items-center gap-2.5 px-4 py-2 text-xs text-slate-300 hover:text-white hover:bg-slate-800/80 transition-colors"
                  >
                    <Award className="w-4 h-4 text-amber-400" />
                    <span>My Certificates</span>
                  </Link>

                  {isAdmin && (
                    <Link
                      href="/admin"
                      className="flex items-center gap-2.5 px-4 py-2 text-xs text-amber-300 bg-amber-500/10 hover:bg-amber-500/20 border-y border-amber-500/20 transition-colors my-1"
                    >
                      <ShieldCheck className="w-4 h-4 text-amber-400" />
                      <span className="font-semibold">Admin Studio</span>
                    </Link>
                  )}

                  <button
                    onClick={logout}
                    className="w-full flex items-center gap-2.5 px-4 py-2 text-xs text-rose-400 hover:bg-rose-500/10 transition-colors border-t border-slate-800 mt-1"
                  >
                    <LogOut className="w-4 h-4" />
                    <span>Sign Out</span>
                  </button>
                </div>
              )}
            </div>
          ) : (
            <div className="flex items-center gap-2.5">
              <Link
                href="/login"
                className="px-4 py-2 rounded-xl text-xs font-semibold text-slate-300 hover:text-white hover:bg-slate-900 border border-slate-800/80 transition-all"
              >
                Sign In
              </Link>
              <Link
                href="/register"
                className="px-4 py-2 rounded-xl text-xs font-semibold text-slate-950 bg-gradient-to-r from-cyan-400 to-cyan-300 hover:from-cyan-300 hover:to-cyan-200 shadow-[0_0_20px_rgba(6,182,212,0.3)] transition-all font-mono uppercase tracking-wider"
              >
                Get Started
              </Link>
            </div>
          )}
        </div>

        {/* Mobile Hamburger Trigger */}
        <button
          onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
          className="lg:hidden p-2 rounded-xl bg-slate-900 border border-slate-800 text-slate-300 hover:text-white"
          aria-label="Toggle Navigation Menu"
        >
          {isMobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
        </button>
      </div>

      {/* Mobile Drawer */}
      {isMobileMenuOpen && (
        <div className="lg:hidden border-b border-slate-800 bg-slate-950/98 backdrop-blur-2xl px-4 pt-3 pb-6 animate-in slide-in-from-top-4">
          <form onSubmit={handleSearchSubmit} className="mb-4">
            <div className="relative">
              <Search className="w-4 h-4 text-slate-500 absolute left-3 top-2.5" />
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search curricula..."
                className="w-full pl-9 pr-4 py-2 rounded-xl bg-slate-900 border border-slate-800 text-sm text-slate-200 placeholder-slate-500 focus:outline-none focus:border-cyan-500"
              />
            </div>
          </form>

          <div className="flex flex-col gap-1">
            {navLinks.map((link) => (
              <Link
                key={link.label}
                href={link.href}
                className="px-3 py-2 rounded-xl text-sm font-medium text-slate-200 hover:bg-slate-900 transition-colors"
              >
                {link.label}
              </Link>
            ))}

            {isAuthenticated ? (
              <>
                <div className="my-2 border-t border-slate-800" />
                <Link
                  href="/dashboard"
                  className="flex items-center gap-2.5 px-3 py-2 rounded-xl text-sm text-cyan-400 font-medium hover:bg-slate-900"
                >
                  <LayoutDashboard className="w-4 h-4" />
                  <span>Learning Cockpit</span>
                </Link>
                <Link
                  href="/profile"
                  className="flex items-center gap-2.5 px-3 py-2 rounded-xl text-sm text-slate-300 hover:bg-slate-900"
                >
                  <UserIcon className="w-4 h-4 text-indigo-400" />
                  <span>My Profile</span>
                </Link>
                {isAdmin && (
                  <Link
                    href="/admin"
                    className="flex items-center gap-2.5 px-3 py-2 rounded-xl text-sm text-amber-300 font-semibold bg-amber-500/10"
                  >
                    <ShieldCheck className="w-4 h-4" />
                    <span>Admin Studio</span>
                  </Link>
                )}
                <button
                  onClick={logout}
                  className="flex items-center gap-2.5 px-3 py-2 rounded-xl text-sm text-rose-400 hover:bg-rose-500/10 text-left mt-2"
                >
                  <LogOut className="w-4 h-4" />
                  <span>Sign Out</span>
                </button>
              </>
            ) : (
              <div className="flex flex-col gap-2 mt-4 pt-3 border-t border-slate-800">
                <Link
                  href="/login"
                  className="w-full text-center py-2.5 rounded-xl text-sm font-semibold bg-slate-900 border border-slate-800 text-slate-200"
                >
                  Sign In
                </Link>
                <Link
                  href="/register"
                  className="w-full text-center py-2.5 rounded-xl text-sm font-semibold bg-cyan-400 text-slate-950 font-mono uppercase tracking-wider"
                >
                  Get Started Free
                </Link>
              </div>
            )}
          </div>
        </div>
      )}
    </header>
  );
}
