'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import {
  Layers,
  BookOpen,
  Edit,
  Save,
  Plus,
  Trash2,
  ChevronRight,
  Code2,
  CheckCircle2,
  ArrowLeft,
} from 'lucide-react';
import { api } from '@/lib/api';
import { useAuth } from '@/lib/auth-context';
import { useToast } from '@/components/Toast';
import { Course, ChapterDetail } from '@/lib/types';

export default function AdminCoursesManagerPage() {
  const router = useRouter();
  const { isAdmin, isAuthenticated, isLoading: authLoading } = useAuth();
  const { success, error: toastError } = useToast();

  const [courses, setCourses] = useState<Course[]>([]);
  const [selectedCourse, setSelectedCourse] = useState<Course | null>(null);
  const [selectedChapter, setSelectedChapter] = useState<any | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);

  // Edit fields for selected chapter
  const [chapterTitle, setChapterTitle] = useState('');
  const [chapterContent, setChapterContent] = useState('');
  const [chapterCode, setChapterCode] = useState('');
  const [chapterLang, setChapterLang] = useState('python');

  const loadCourses = async () => {
    try {
      const data = await api.get<{ results?: Course[] } | Course[]>('/courses/');
      const list = Array.isArray(data) ? data : data.results || [];
      setCourses(list);
      if (list.length > 0) {
        const targetSlug = selectedCourse?.slug || list[0].slug;
        const fullCourse = await api.get<Course>(`/courses/${targetSlug}/`);
        setSelectedCourse(fullCourse);
        const firstCh = fullCourse.modules?.[0]?.chapters?.[0];
        if (firstCh && !selectedChapter) {
          loadChapterDetail(fullCourse.slug, firstCh.slug);
        }
      }
    } catch (err: any) {
      toastError(err.message || 'Failed to load courses');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    if (!authLoading) {
      if (!isAuthenticated || !isAdmin) {
        router.push('/login?redirect=/admin/courses');
        return;
      }
    }

    if (isAuthenticated && isAdmin) {
      loadCourses();
    }
  }, [isAuthenticated, isAdmin, authLoading]);

  const handleSelectCourse = async (courseSlug: string) => {
    try {
      setIsLoading(true);
      const fullCourse = await api.get<Course>(`/courses/${courseSlug}/`);
      setSelectedCourse(fullCourse);
      const firstCh = fullCourse.modules?.[0]?.chapters?.[0];
      if (firstCh) {
        loadChapterDetail(fullCourse.slug, firstCh.slug);
      } else {
        setSelectedChapter(null);
      }
    } catch (err: any) {
      toastError(err.message || 'Failed to load course details');
    } finally {
      setIsLoading(false);
    }
  };

  const loadChapterDetail = async (cSlug: string, chSlug: string) => {
    try {
      const data = await api.get<ChapterDetail>(`/courses/${cSlug}/chapters/${chSlug}/`);
      setSelectedChapter(data);
      setChapterTitle(data.title);
      setChapterContent(data.content_markdown);
      setChapterCode(data.code_snippet || '');
      setChapterLang(data.code_language || 'python');
    } catch (err: any) {
      toastError(err.message || 'Failed to load chapter content');
    }
  };

  const handleSaveChapter = async () => {
    if (!selectedChapter) return;
    setIsSaving(true);
    try {
      await api.patch(`/admin/chapters/${selectedChapter.id}/`, {
        title: chapterTitle,
        content_markdown: chapterContent,
        code_snippet: chapterCode,
        code_language: chapterLang,
      });
      success('Chapter content updated successfully!');
    } catch (err: any) {
      toastError(err.message || 'Failed to save changes');
    } finally {
      setIsSaving(false);
    }
  };

  if (authLoading || isLoading) {
    return (
      <div className="min-h-[85vh] bg-[#07090E] flex items-center justify-center">
        <div className="w-10 h-10 rounded-full border-2 border-cyan-500 border-t-transparent animate-spin" />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#07090E] py-10 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto space-y-8">
        {/* Top Header */}
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Link
              href="/admin"
              className="p-2 rounded-xl bg-slate-900 border border-slate-800 text-slate-400 hover:text-white"
            >
              <ArrowLeft className="w-4 h-4" />
            </Link>
            <div>
              <h1 className="text-2xl font-bold text-white">Curriculum & Chapter Studio</h1>
              <p className="text-xs text-slate-400 font-mono">
                Manage curricula, syllabus outlines, and technical lesson markdown content.
              </p>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <button
              onClick={handleSaveChapter}
              disabled={isSaving || !selectedChapter}
              className="px-5 py-2.5 rounded-xl font-mono text-xs font-bold text-slate-950 bg-cyan-400 hover:bg-cyan-300 flex items-center gap-1.5 uppercase disabled:opacity-40"
            >
              <Save className="w-4 h-4" />
              <span>{isSaving ? 'Saving...' : 'Save Lesson Changes'}</span>
            </button>
          </div>
        </div>

        {/* 3-Pane Editor Layout */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
          {/* Left Column: Course & Chapter Selector */}
          <div className="lg:col-span-4 p-5 rounded-2xl bg-slate-900/80 border border-slate-800 space-y-6">
            {/* Course Selector Dropdown */}
            <div className="space-y-1.5">
              <label className="text-xs font-mono text-slate-400">Select Curriculum Track</label>
              <select
                value={selectedCourse?.slug || ''}
                onChange={(e) => handleSelectCourse(e.target.value)}
                className="w-full px-3 py-2 rounded-xl bg-slate-950 border border-slate-800 text-xs font-mono text-cyan-300 focus:outline-none focus:border-cyan-500"
              >
                {courses.map((c) => (
                  <option key={c.id} value={c.slug}>
                    {c.title}
                  </option>
                ))}
              </select>
            </div>

            {/* Course Pricing & Commercial Configuration */}
            {selectedCourse && (
              <CoursePricingEditor course={selectedCourse} onCourseUpdated={loadCourses} />
            )}

            {/* Chapters Tree */}
            <div className="space-y-4">
              <span className="text-[11px] font-mono uppercase text-slate-400 font-bold block">
                Modules & Lessons
              </span>

              {selectedCourse?.modules?.map((mod, modIdx) => (
                <div key={mod.id} className="space-y-1.5">
                  <span className="text-[10px] font-mono text-slate-500 uppercase">
                    MOD {modIdx + 1}: {mod.title}
                  </span>
                  <div className="space-y-1">
                    {mod.chapters.map((ch) => (
                      <button
                        key={ch.id}
                        onClick={() => loadChapterDetail(selectedCourse.slug, ch.slug)}
                        className={`w-full px-3 py-2 rounded-lg text-left text-xs font-mono transition-all flex items-center justify-between ${
                          selectedChapter?.id === ch.id
                            ? 'bg-cyan-500/20 text-cyan-300 border border-cyan-500/40 font-bold'
                            : 'text-slate-400 hover:text-slate-200 hover:bg-slate-950'
                        }`}
                      >
                        <span className="truncate">{ch.title}</span>
                        <ChevronRight className="w-3.5 h-3.5 shrink-0 ml-1 opacity-60" />
                      </button>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Right Column: Active Chapter Content Editor */}
          <div className="lg:col-span-8 p-6 rounded-2xl bg-slate-900/80 border border-slate-800 space-y-6">
            {selectedChapter ? (
              <div className="space-y-4">
                {/* Title */}
                <div className="space-y-1.5">
                  <label className="text-xs font-mono text-slate-400">Lesson Title</label>
                  <input
                    type="text"
                    value={chapterTitle}
                    onChange={(e) => setChapterTitle(e.target.value)}
                    className="w-full px-4 py-2 rounded-xl bg-slate-950 border border-slate-800 text-sm font-bold text-white focus:outline-none focus:border-cyan-500"
                  />
                </div>

                {/* Markdown Notes Editor */}
                <div className="space-y-1.5">
                  <label className="text-xs font-mono text-slate-400">
                    Lesson Technical Markdown Notes
                  </label>
                  <textarea
                    rows={12}
                    value={chapterContent}
                    onChange={(e) => setChapterContent(e.target.value)}
                    className="w-full p-4 rounded-xl bg-slate-950 border border-slate-800 text-xs font-mono text-slate-200 leading-relaxed focus:outline-none focus:border-cyan-500"
                  />
                </div>

                {/* Code Snippet Editor */}
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                  <div className="sm:col-span-2 space-y-1.5">
                    <label className="text-xs font-mono text-slate-400">
                      Executable Code Sandbox
                    </label>
                    <textarea
                      rows={6}
                      value={chapterCode}
                      onChange={(e) => setChapterCode(e.target.value)}
                      placeholder="def example(): ..."
                      className="w-full p-3 rounded-xl bg-[#0B0F17] border border-slate-800 text-xs font-mono text-cyan-200 focus:outline-none focus:border-cyan-500"
                    />
                  </div>
                  <div className="space-y-1.5">
                    <label className="text-xs font-mono text-slate-400">Language</label>
                    <select
                      value={chapterLang}
                      onChange={(e) => setChapterLang(e.target.value)}
                      className="w-full px-3 py-2 rounded-xl bg-slate-950 border border-slate-800 text-xs font-mono text-slate-200 focus:outline-none focus:border-cyan-500"
                    >
                      <option value="python">Python</option>
                      <option value="c">C</option>
                      <option value="cpp">C++</option>
                      <option value="sql">SQL</option>
                    </select>
                  </div>
                </div>
              </div>
            ) : (
              <div className="p-16 text-center text-xs text-slate-500 font-mono">
                Select a lesson module on the left pane to edit its curriculum content.
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

function CoursePricingEditor({
  course,
  onCourseUpdated,
}: {
  course: Course;
  onCourseUpdated: () => void;
}) {
  const { success, error: toastError } = useToast();

  const [priceInRupees, setPriceInRupees] = useState<number>(
    course.price_in_rupees || (course.price_in_paise ? course.price_in_paise / 100 : 1499)
  );
  const [originalPriceInRupees, setOriginalPriceInRupees] = useState<number>(
    course.original_price_in_rupees || (course.original_price_in_paise ? course.original_price_in_paise / 100 : 1999)
  );
  const [isFree, setIsFree] = useState<boolean>(course.is_free || false);
  const [isUpdating, setIsUpdating] = useState(false);

  useEffect(() => {
    setPriceInRupees(course.price_in_rupees || (course.price_in_paise ? course.price_in_paise / 100 : 1499));
    setOriginalPriceInRupees(course.original_price_in_rupees || (course.original_price_in_paise ? course.original_price_in_paise / 100 : 1999));
    setIsFree(course.is_free || false);
  }, [course]);

  const discountAmount = originalPriceInRupees > priceInRupees ? originalPriceInRupees - priceInRupees : 0;
  const discountPercent = originalPriceInRupees > 0 ? Math.round((discountAmount / originalPriceInRupees) * 100) : 0;

  const handleSavePricing = async () => {
    if (!isFree && priceInRupees < 0) {
      toastError('Price cannot be negative.');
      return;
    }

    if (!isFree && originalPriceInRupees < priceInRupees) {
      toastError('Original price cannot be less than selling price.');
      return;
    }

    setIsUpdating(true);
    try {
      await api.patch(`/admin/courses/${course.id}/`, {
        price_in_paise: isFree ? 0 : Math.round(priceInRupees * 100),
        original_price_in_paise: isFree ? 0 : Math.round(originalPriceInRupees * 100),
        discount_price_in_paise: isFree ? 0 : Math.round(priceInRupees * 100),
        is_free: isFree,
      });
      success(`Pricing updated for ${course.title}!`);
      onCourseUpdated();
    } catch (err: any) {
      toastError(err.message || 'Failed to update course pricing');
    } finally {
      setIsUpdating(false);
    }
  };

  return (
    <div className="p-4 rounded-xl bg-slate-950 border border-slate-800 space-y-3 font-mono text-xs shadow-inner">
      <div className="flex items-center justify-between border-b border-slate-800 pb-2">
        <span className="font-bold text-slate-300 uppercase tracking-wider text-[11px]">
          Commerce & Pricing
        </span>
        <label className="flex items-center gap-1.5 cursor-pointer">
          <input
            type="checkbox"
            checked={isFree}
            onChange={(e) => setIsFree(e.target.checked)}
            className="rounded bg-slate-900 border-slate-700 text-cyan-500 focus:ring-0"
          />
          <span className="text-[10px] text-slate-400">Free Course</span>
        </label>
      </div>

      {!isFree && (
        <div className="space-y-3">
          <div className="grid grid-cols-2 gap-2">
            <div>
              <label className="text-[10px] text-slate-400 block mb-1">Selling Price (₹)</label>
              <input
                type="number"
                min="0"
                value={priceInRupees}
                onChange={(e) => setPriceInRupees(Number(e.target.value))}
                className="w-full px-2.5 py-1.5 rounded-lg bg-slate-900 border border-slate-800 text-white font-bold focus:outline-none focus:border-cyan-500"
              />
            </div>
            <div>
              <label className="text-[10px] text-slate-400 block mb-1">Original Price (₹)</label>
              <input
                type="number"
                min="0"
                value={originalPriceInRupees}
                onChange={(e) => setOriginalPriceInRupees(Number(e.target.value))}
                className="w-full px-2.5 py-1.5 rounded-lg bg-slate-900 border border-slate-800 text-slate-400 focus:outline-none focus:border-cyan-500"
              />
            </div>
          </div>

          {discountAmount > 0 && (
            <div className="p-2 rounded bg-emerald-500/10 border border-emerald-500/20 text-[10px] text-emerald-400 flex items-center justify-between">
              <span>Customer Saves: ₹{discountAmount.toLocaleString()}</span>
              <span className="font-bold">{discountPercent}% OFF</span>
            </div>
          )}
        </div>
      )}

      <button
        onClick={handleSavePricing}
        disabled={isUpdating}
        className="w-full py-2 rounded-lg bg-cyan-500/20 hover:bg-cyan-500/30 text-cyan-300 border border-cyan-500/40 font-bold uppercase tracking-wider text-[10px] transition-all disabled:opacity-50 cursor-pointer"
      >
        {isUpdating ? 'Saving...' : 'Update Pricing in Database'}
      </button>
    </div>
  );
}
