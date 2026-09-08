'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import {
  User as UserIcon,
  Mail,
  Calendar,
  Award,
  BookOpen,
  CheckCircle2,
  Edit3,
  Check,
  X,
  ExternalLink,
  Globe,
  Link2,
} from 'lucide-react';
import { api } from '@/lib/api';
import { useAuth } from '@/lib/auth-context';
import { useToast } from '@/components/Toast';
import { Certificate } from '@/lib/types';
import { formatDate } from '@/lib/utils';

export default function ProfilePage() {
  const router = useRouter();
  const { user, isAuthenticated, isLoading: authLoading, updateProfile } = useAuth();
  const { success, error: toastError } = useToast();

  const [certificates, setCertificates] = useState<Certificate[]>([]);
  const [isLoadingCerts, setIsLoadingCerts] = useState(true);
  const [isEditing, setIsEditing] = useState(false);
  const [isSaving, setIsSaving] = useState(false);

  // Edit form state
  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    headline: '',
    bio: '',
    github: '',
    linkedin: '',
  });

  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      router.push('/login?redirect=/profile');
      return;
    }

    if (user) {
      setFormData({
        first_name: user.first_name || '',
        last_name: user.last_name || '',
        headline: user.headline || '',
        bio: user.bio || '',
        github: user.github || '',
        linkedin: user.linkedin || '',
      });
    }

    async function loadCerts() {
      try {
        const data = await api.get<Certificate[]>('/certificates/my-certificates/');
        setCertificates(Array.isArray(data) ? data : []);
      } catch {
        // Ignored
      } finally {
        setIsLoadingCerts(false);
      }
    }

    if (isAuthenticated) {
      loadCerts();
    }
  }, [user, isAuthenticated, authLoading]);

  const handleSaveProfile = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSaving(true);
    try {
      await updateProfile(formData);
      setIsEditing(false);
      success('Profile updated successfully!');
    } catch (err: any) {
      toastError(err.message || 'Failed to update profile');
    } finally {
      setIsSaving(false);
    }
  };

  if (authLoading || !user) {
    return (
      <div className="min-h-[85vh] bg-[#07090E] flex items-center justify-center">
        <div className="w-10 h-10 rounded-full border-2 border-cyan-500 border-t-transparent animate-spin" />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#07090E] py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-5xl mx-auto space-y-10">
        {/* Profile Card Header */}
        <div className="p-8 sm:p-10 rounded-3xl bg-gradient-to-br from-slate-900 via-slate-950 to-[#0B0F17] border border-slate-800 shadow-2xl relative overflow-hidden">
          <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-6 relative z-10">
            <div className="flex items-center gap-5">
              <div className="w-16 h-16 sm:w-20 sm:h-20 rounded-2xl bg-gradient-to-tr from-cyan-500 to-indigo-600 flex items-center justify-center text-2xl font-black text-white shadow-xl">
                {user.first_name ? user.first_name[0].toUpperCase() : user.username[0].toUpperCase()}
              </div>

              <div className="space-y-1">
                <h1 className="text-2xl sm:text-3xl font-extrabold text-white">
                  {user.first_name ? `${user.first_name} ${user.last_name}` : user.username}
                </h1>
                <p className="text-sm font-mono text-cyan-400">
                  {user.headline || 'Software Engineer'}
                </p>
                <div className="flex items-center gap-4 text-xs font-mono text-slate-400 pt-1">
                  <span className="flex items-center gap-1">
                    <Mail className="w-3.5 h-3.5 text-slate-500" />
                    <span>{user.email}</span>
                  </span>
                  <span className="flex items-center gap-1">
                    <Calendar className="w-3.5 h-3.5 text-slate-500" />
                    <span>Joined {formatDate(user.created_at)}</span>
                  </span>
                </div>
              </div>
            </div>

            <button
              onClick={() => setIsEditing(!isEditing)}
              className="px-4 py-2 rounded-xl font-mono text-xs font-semibold text-slate-300 hover:text-white bg-slate-900 border border-slate-800 hover:border-slate-700 flex items-center gap-1.5 transition-all"
            >
              <Edit3 className="w-3.5 h-3.5" />
              <span>{isEditing ? 'Cancel Edit' : 'Edit Profile'}</span>
            </button>
          </div>

          {/* Social Links & Bio */}
          <div className="mt-8 pt-6 border-t border-slate-800/80 space-y-4 text-sm text-slate-300">
            {user.bio ? (
              <p className="leading-relaxed text-slate-400 max-w-3xl">{user.bio}</p>
            ) : (
              <p className="text-xs text-slate-500 italic">No biography provided yet.</p>
            )}

            <div className="flex items-center gap-4 pt-2">
              {user.github && (
                <a
                  href={user.github}
                  target="_blank"
                  rel="noreferrer"
                  className="flex items-center gap-1.5 text-xs font-mono text-slate-400 hover:text-cyan-400 transition-colors"
                >
                  <Globe className="w-4 h-4" />
                  <span>GitHub Profile</span>
                </a>
              )}
              {user.linkedin && (
                <a
                  href={user.linkedin}
                  target="_blank"
                  rel="noreferrer"
                  className="flex items-center gap-1.5 text-xs font-mono text-slate-400 hover:text-cyan-400 transition-colors"
                >
                  <Link2 className="w-4 h-4" />
                  <span>LinkedIn Profile</span>
                </a>
              )}
            </div>
          </div>
        </div>

        {/* Edit Form Modal/Drawer */}
        {isEditing && (
          <form
            onSubmit={handleSaveProfile}
            className="p-8 rounded-3xl bg-slate-900 border border-slate-800 space-y-6 animate-in slide-in-from-top-4"
          >
            <h3 className="text-lg font-bold text-white">Update Engineer Profile</h3>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div className="space-y-1.5">
                <label className="text-xs font-mono text-slate-400">First Name</label>
                <input
                  type="text"
                  value={formData.first_name}
                  onChange={(e) => setFormData({ ...formData, first_name: e.target.value })}
                  className="w-full px-3.5 py-2 rounded-xl bg-slate-950 border border-slate-800 text-sm text-slate-200 focus:border-cyan-500 focus:outline-none"
                />
              </div>

              <div className="space-y-1.5">
                <label className="text-xs font-mono text-slate-400">Last Name</label>
                <input
                  type="text"
                  value={formData.last_name}
                  onChange={(e) => setFormData({ ...formData, last_name: e.target.value })}
                  className="w-full px-3.5 py-2 rounded-xl bg-slate-950 border border-slate-800 text-sm text-slate-200 focus:border-cyan-500 focus:outline-none"
                />
              </div>

              <div className="sm:col-span-2 space-y-1.5">
                <label className="text-xs font-mono text-slate-400">Headline</label>
                <input
                  type="text"
                  value={formData.headline}
                  onChange={(e) => setFormData({ ...formData, headline: e.target.value })}
                  placeholder="e.g. Distributed Systems & Algorithms Engineer"
                  className="w-full px-3.5 py-2 rounded-xl bg-slate-950 border border-slate-800 text-sm text-slate-200 focus:border-cyan-500 focus:outline-none"
                />
              </div>

              <div className="sm:col-span-2 space-y-1.5">
                <label className="text-xs font-mono text-slate-400">Bio</label>
                <textarea
                  rows={3}
                  value={formData.bio}
                  onChange={(e) => setFormData({ ...formData, bio: e.target.value })}
                  placeholder="Brief summary of your background and technical interests..."
                  className="w-full px-3.5 py-2 rounded-xl bg-slate-950 border border-slate-800 text-sm text-slate-200 focus:border-cyan-500 focus:outline-none"
                />
              </div>

              <div className="space-y-1.5">
                <label className="text-xs font-mono text-slate-400">GitHub Profile URL</label>
                <input
                  type="url"
                  value={formData.github}
                  onChange={(e) => setFormData({ ...formData, github: e.target.value })}
                  placeholder="https://github.com/username"
                  className="w-full px-3.5 py-2 rounded-xl bg-slate-950 border border-slate-800 text-sm text-slate-200 focus:border-cyan-500 focus:outline-none"
                />
              </div>

              <div className="space-y-1.5">
                <label className="text-xs font-mono text-slate-400">LinkedIn Profile URL</label>
                <input
                  type="url"
                  value={formData.linkedin}
                  onChange={(e) => setFormData({ ...formData, linkedin: e.target.value })}
                  placeholder="https://linkedin.com/in/username"
                  className="w-full px-3.5 py-2 rounded-xl bg-slate-950 border border-slate-800 text-sm text-slate-200 focus:border-cyan-500 focus:outline-none"
                />
              </div>
            </div>

            <div className="flex justify-end gap-3 pt-4 border-t border-slate-800">
              <button
                type="button"
                onClick={() => setIsEditing(false)}
                className="px-4 py-2 rounded-xl font-mono text-xs text-slate-400 bg-slate-950 border border-slate-800"
              >
                Cancel
              </button>
              <button
                type="submit"
                disabled={isSaving}
                className="px-6 py-2 rounded-xl font-mono text-xs font-bold text-slate-950 bg-cyan-400 hover:bg-cyan-300 uppercase"
              >
                {isSaving ? 'Saving...' : 'Save Profile Changes'}
              </button>
            </div>
          </form>
        )}

        {/* Certificates Section */}
        <div className="space-y-6">
          <h2 className="text-xl font-bold text-white flex items-center gap-2">
            <Award className="w-5 h-5 text-amber-400" />
            <span>Earned Credentials & Certifications</span>
          </h2>

          {certificates.length > 0 ? (
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
              {certificates.map((cert) => (
                <div
                  key={cert.id}
                  className="p-6 rounded-2xl bg-gradient-to-br from-slate-900 to-slate-950 border border-amber-500/30 shadow-lg flex flex-col justify-between"
                >
                  <div className="space-y-2">
                    <div className="flex items-center justify-between text-[11px] font-mono">
                      <span className="text-amber-400 uppercase font-bold">Verified Credential</span>
                      <span className="text-slate-400">{formatDate(cert.issue_date)}</span>
                    </div>

                    <h3 className="text-lg font-bold text-white">{cert.course_title}</h3>
                    <p className="text-xs font-mono text-cyan-300">Grade: {cert.grade_percentage}%</p>
                    <p className="text-[10px] font-mono text-slate-500 truncate">{cert.certificate_code}</p>
                  </div>

                  <div className="mt-6 pt-4 border-t border-slate-800/80 flex items-center justify-between">
                    <Link
                      href={`/verify/${cert.certificate_code}`}
                      className="text-xs font-mono text-cyan-400 hover:underline inline-flex items-center gap-1"
                    >
                      <span>Public Verification</span>
                      <ExternalLink className="w-3.5 h-3.5" />
                    </Link>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="p-10 rounded-2xl bg-slate-900/40 border border-slate-800 text-center space-y-3">
              <p className="text-xs text-slate-400">You haven't earned any certificates yet. Complete a curriculum track to earn yours!</p>
              <Link
                href="/courses"
                className="inline-block px-4 py-2 rounded-xl bg-cyan-400 text-slate-950 font-mono text-xs font-bold uppercase"
              >
                Explore Curricula
              </Link>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
