'use client';

import React, { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import Link from 'next/link';
import {
  ChevronLeft,
  ChevronRight,
  CheckCircle2,
  Circle,
  Menu,
  X,
  BookOpen,
  Award,
  Terminal,
  HelpCircle,
  Lightbulb,
  Check,
  Share2,
  Lock as LockIcon,
} from 'lucide-react';
import { api } from '@/lib/api';
import { useAuth } from '@/lib/auth-context';
import { useToast } from '@/components/Toast';
import { CodeBlock } from '@/components/CodeBlock';
import { ChapterDetail, Course } from '@/lib/types';

export default function LearningWorkspacePage() {
  const params = useParams() as { courseSlug: string; chapterSlug: string };
  const { courseSlug, chapterSlug } = params;
  const router = useRouter();
  const { isAuthenticated } = useAuth();
  const { success, error: toastError } = useToast();

  const [chapter, setChapter] = useState<ChapterDetail | null>(null);
  const [course, setCourse] = useState<Course | null>(null);
  const [completedChapterIds, setCompletedChapterIds] = useState<number[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [paymentRequired, setPaymentRequired] = useState<{
    required: boolean;
    course_title?: string;
    price_in_rupees?: number;
  }>({ required: false });
  const [isMarking, setIsMarking] = useState(false);
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [activeTabMobile, setActiveTabMobile] = useState<'content' | 'syllabus' | 'practice'>('content');

  // Load chapter and course syllabus data
  useEffect(() => {
    async function loadWorkspaceData() {
      setIsLoading(true);
      setPaymentRequired({ required: false });
      try {
        const [chapterData, courseData] = await Promise.all([
          api.get<ChapterDetail>(`/courses/${courseSlug}/chapters/${chapterSlug}/`).catch((err: any) => {
            if (err?.code === 'payment_required' || err?.message?.includes('Payment required')) {
              setPaymentRequired({
                required: true,
                course_title: err.course_title,
                price_in_rupees: err.price_in_rupees,
              });
            }
            throw err;
          }),
          api.get<Course>(`/courses/${courseSlug}/`),
        ]);

        setChapter(chapterData);
        setCourse(courseData);

        // If user is authenticated, fetch progress status
        if (isAuthenticated) {
          try {
            const progressData = await api.get<{ completed_chapters: number[] }>(
              `/progress/course/${courseSlug}/`
            );
            setCompletedChapterIds(progressData.completed_chapters || []);
          } catch {
            // Handled
          }
        }
      } catch (err: any) {
        if (!err?.code && !err?.message?.includes('Payment required')) {
          toastError(err.message || 'Failed to load lesson workspace');
        }
      } finally {
        setIsLoading(false);
      }
    }

    if (courseSlug && chapterSlug) {
      loadWorkspaceData();
    }
  }, [courseSlug, chapterSlug, isAuthenticated]);

  const handleToggleComplete = async () => {
    if (!isAuthenticated) {
      toastError('Please sign in to save lesson progress.');
      return;
    }

    if (!chapter) return;

    const willBeCompleted = !completedChapterIds.includes(chapter.id);
    setIsMarking(true);

    try {
      const res = await api.post<{
        success: boolean;
        is_completed: boolean;
        course_progress_percentage: number;
      }>('/progress/mark-chapter/', {
        chapter_id: chapter.id,
        is_completed: willBeCompleted,
      });

      if (willBeCompleted) {
        setCompletedChapterIds((prev) => [...prev, chapter.id]);
        success(`Lesson completed! Progress: ${res.course_progress_percentage}%`);
      } else {
        setCompletedChapterIds((prev) => prev.filter((id) => id !== chapter.id));
      }
    } catch (err: any) {
      toastError(err.message || 'Failed to update progress');
    } finally {
      setIsMarking(false);
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-[85vh] bg-[#07090E] flex items-center justify-center">
        <div className="flex flex-col items-center gap-4">
          <div className="w-10 h-10 rounded-full border-2 border-cyan-500 border-t-transparent animate-spin" />
          <span className="text-xs font-mono text-slate-400">Initializing Learning Workspace...</span>
        </div>
      </div>
    );
  }

  // Paywall Interstitial Screen
  if (paymentRequired.required) {
    return (
      <div className="min-h-[85vh] flex flex-col items-center justify-center p-6 text-center bg-[#07090E] select-none">
        <div className="w-full max-w-lg p-8 sm:p-10 rounded-3xl bg-slate-950 border border-slate-800 shadow-2xl space-y-6 relative overflow-hidden">
          <div className="absolute -top-20 left-1/2 -translate-x-1/2 w-60 h-60 rounded-full bg-cyan-500/20 blur-[90px] pointer-events-none" />

          <div className="w-16 h-16 rounded-2xl bg-cyan-500/10 border border-cyan-500/30 flex items-center justify-center text-cyan-400 mx-auto shadow-[0_0_30px_rgba(6,182,212,0.25)]">
            <LockIcon className="w-8 h-8 text-cyan-400" />
          </div>

          <div className="space-y-2">
            <span className="text-xs font-mono font-bold uppercase tracking-widest text-cyan-400">
              Premium Lesson Content
            </span>
            <h2 className="text-2xl sm:text-3xl font-black text-white tracking-tight">
              Course Purchase Required
            </h2>
            <p className="text-xs sm:text-sm text-slate-400 max-w-sm mx-auto leading-relaxed">
              This chapter contains proprietary engineering notes, code sandboxes, and practice assignments.
            </p>
          </div>

          <div className="p-4 rounded-xl bg-slate-900/90 border border-slate-800 font-mono text-xs flex items-center justify-between">
            <span className="text-slate-400">One-time Enrollment</span>
            <span className="text-base font-black text-white">
              ₹{(paymentRequired.price_in_rupees || 1499).toLocaleString()}
            </span>
          </div>

          <div className="space-y-3">
            <Link
              href={`/courses/${courseSlug}`}
              className="w-full py-3.5 rounded-xl font-mono text-xs font-black text-slate-950 bg-gradient-to-r from-cyan-400 via-cyan-300 to-teal-300 hover:from-cyan-300 hover:to-teal-200 shadow-[0_0_25px_rgba(6,182,212,0.4)] transition-all flex items-center justify-center gap-2 uppercase tracking-wider"
            >
              <span>Unlock Track & Start Learning</span>
            </Link>

            <Link
              href={`/courses/${courseSlug}`}
              className="block text-xs font-mono text-slate-400 hover:text-white transition-colors"
            >
              View Full Syllabus Roadmap
            </Link>
          </div>
        </div>
      </div>
    );
  }

  if (!chapter || !course) {
    return (
      <div className="min-h-[80vh] flex flex-col items-center justify-center p-8 text-center bg-[#07090E]">
        <h2 className="text-xl font-bold text-white mb-2">Lesson Unavailable</h2>
        <p className="text-xs text-slate-400 mb-6">Could not locate the requested lesson module.</p>
        <Link
          href={`/courses/${courseSlug}`}
          className="px-4 py-2 rounded-xl bg-cyan-500 text-slate-950 font-mono text-xs font-bold"
        >
          Return to Course
        </Link>
      </div>
    );
  }

  const isCurrentChapterCompleted = completedChapterIds.includes(chapter.id);

  return (
    <div className="min-h-screen bg-[#07090E] text-slate-100 flex flex-col">
      {/* =========================================================================
          WORKSPACE TOP NAVIGATION BAR
         ========================================================================= */}
      <div className="h-14 bg-slate-950/90 border-b border-slate-800/90 px-4 sm:px-6 flex items-center justify-between gap-4 sticky top-20 z-30 backdrop-blur-xl">
        <div className="flex items-center gap-3">
          <Link
            href={`/courses/${course.slug}`}
            className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-900 transition-colors"
            title="Course Syllabus"
          >
            <ChevronLeft className="w-5 h-5" />
          </Link>
          <div className="flex flex-col">
            <span className="text-xs font-mono font-semibold text-cyan-400 max-w-[200px] sm:max-w-md truncate">
              {course.title}
            </span>
            <span className="text-[11px] text-slate-400 truncate max-w-[200px] sm:max-w-md">
              {chapter.module_title} • {chapter.title}
            </span>
          </div>
        </div>

        {/* Action Right */}
        <div className="flex items-center gap-3">
          <button
            onClick={handleToggleComplete}
            disabled={isMarking}
            className={`px-3.5 py-1.5 rounded-xl font-mono text-xs font-semibold flex items-center gap-2 transition-all ${
              isCurrentChapterCompleted
                ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/30'
                : 'bg-cyan-500/10 text-cyan-300 border border-cyan-500/30 hover:bg-cyan-500/20'
            }`}
          >
            {isCurrentChapterCompleted ? (
              <>
                <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                <span className="hidden sm:inline">Completed</span>
              </>
            ) : (
              <>
                <Circle className="w-4 h-4" />
                <span className="hidden sm:inline">Mark Complete</span>
              </>
            )}
          </button>

          <button
            onClick={() => setIsSidebarOpen(!isSidebarOpen)}
            className="lg:hidden p-1.5 rounded-lg bg-slate-900 border border-slate-800 text-slate-300"
            aria-label="Toggle Syllabus Outline"
          >
            <Menu className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* =========================================================================
          3-COLUMN RESPONSIVE WORKSPACE LAYOUT
         ========================================================================= */}
      <div className="flex-1 flex max-w-full overflow-hidden">
        {/* =====================================================================
            LEFT PANE: COLLAPSIBLE SYLLABUS TREE
           ===================================================================== */}
        <aside
          className={`fixed inset-y-0 left-0 z-40 w-72 bg-slate-950/98 border-r border-slate-800/90 flex flex-col transform transition-transform duration-300 lg:static lg:translate-x-0 ${
            isSidebarOpen ? 'translate-x-0' : '-translate-x-full'
          }`}
        >
          {/* Syllabus Header */}
          <div className="p-4 border-b border-slate-800 flex items-center justify-between">
            <div className="flex items-center gap-2">
              <BookOpen className="w-4 h-4 text-cyan-400" />
              <span className="text-xs font-mono font-bold uppercase tracking-wider text-slate-200">
                Syllabus
              </span>
            </div>
            <button
              onClick={() => setIsSidebarOpen(false)}
              className="lg:hidden text-slate-400 hover:text-white"
            >
              <X className="w-4 h-4" />
            </button>
          </div>

          {/* Module & Chapters Scrollable List */}
          <div className="flex-1 overflow-y-auto p-4 space-y-6">
            {course.modules?.map((mod, modIdx) => (
              <div key={mod.id} className="space-y-2">
                <div className="text-[11px] font-mono font-bold text-slate-400 uppercase tracking-wider">
                  MOD {modIdx + 1}: {mod.title}
                </div>
                <div className="space-y-1">
                  {mod.chapters.map((ch) => {
                    const isCompleted = completedChapterIds.includes(ch.id);
                    const isCurrent = ch.slug === chapter.slug;

                    return (
                      <Link
                        key={ch.id}
                        href={`/learn/${course.slug}/${ch.slug}`}
                        onClick={() => setIsSidebarOpen(false)}
                        className={`flex items-center justify-between px-3 py-2 rounded-xl text-xs transition-all ${
                          isCurrent
                            ? 'bg-cyan-500/15 text-cyan-300 border border-cyan-500/40 font-semibold'
                            : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900'
                        }`}
                      >
                        <div className="flex items-center gap-2.5 truncate">
                          {isCompleted ? (
                            <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
                          ) : (
                            <Circle className="w-3.5 h-3.5 text-slate-600 shrink-0" />
                          )}
                          <span className="truncate">{ch.title}</span>
                        </div>
                        <span className="text-[10px] font-mono text-slate-500 shrink-0 ml-2">
                          {ch.duration_minutes}m
                        </span>
                      </Link>
                    );
                  })}
                </div>
              </div>
            ))}

            {/* Assessment Link in Syllabus */}
            <div className="pt-4 border-t border-slate-800">
              <Link
                href={`/learn/${course.slug}/assessment`}
                className="flex items-center gap-2.5 px-3 py-2.5 rounded-xl bg-amber-500/10 border border-amber-500/30 text-amber-300 text-xs font-mono font-semibold hover:bg-amber-500/20 transition-all"
              >
                <Award className="w-4 h-4 text-amber-400" />
                <span>Certification Exam</span>
              </Link>
            </div>
          </div>
        </aside>

        {/* =====================================================================
            CENTER PANE: RICH TECHNICAL CONTENT & NOTES
           ===================================================================== */}
        <main className="flex-1 overflow-y-auto p-4 sm:p-8 lg:p-12 max-w-4xl mx-auto w-full">
          {/* Chapter Heading Banner */}
          <div className="space-y-3 pb-6 border-b border-slate-800">
            <div className="flex items-center gap-2 text-xs font-mono text-cyan-400">
              <span>{chapter.module_title}</span>
              <span>•</span>
              <span>{chapter.duration_minutes} min read</span>
            </div>
            <h1 className="text-2xl sm:text-4xl font-extrabold text-white tracking-tight">
              {chapter.title}
            </h1>
          </div>

          {/* Technical Markdown Notes */}
          <div className="techspire-markdown mt-8">
            <div
              dangerouslySetInnerHTML={{
                __html: formatMarkdown(chapter.content_markdown),
              }}
            />
          </div>

          {/* Code Snippet Box (If Present) */}
          {chapter.code_snippet && (
            <div className="my-8">
              <CodeBlock
                code={chapter.code_snippet}
                language={chapter.code_language || 'python'}
                title={`${chapter.title} • Executable Sandbox`}
              />
            </div>
          )}

          {/* Key Takeaways Card */}
          {chapter.key_takeaways && chapter.key_takeaways.length > 0 && (
            <div className="my-10 p-6 rounded-2xl bg-gradient-to-br from-cyan-950/30 to-slate-900/60 border border-cyan-500/30 space-y-4 shadow-lg">
              <div className="flex items-center gap-2 text-xs font-mono font-bold text-cyan-300 uppercase tracking-wider">
                <Lightbulb className="w-4 h-4 text-cyan-400" />
                <span>Key Architectural Takeaways</span>
              </div>
              <ul className="space-y-2.5 text-xs sm:text-sm text-slate-300">
                {chapter.key_takeaways.map((item, idx) => (
                  <li key={idx} className="flex items-start gap-2.5">
                    <Check className="w-4 h-4 text-cyan-400 shrink-0 mt-0.5" />
                    <span>{item}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Practice Questions Section */}
          {chapter.practice_questions && chapter.practice_questions.length > 0 && (
            <div className="my-10 space-y-4">
              <div className="flex items-center gap-2 text-xs font-mono font-bold text-indigo-300 uppercase tracking-wider">
                <HelpCircle className="w-4 h-4 text-indigo-400" />
                <span>Concept Check & Practice Questions</span>
              </div>

              <div className="space-y-4">
                {chapter.practice_questions.map((pq, idx) => (
                  <details
                    key={idx}
                    className="p-5 rounded-2xl bg-slate-900/80 border border-slate-800 text-sm group"
                  >
                    <summary className="font-semibold text-slate-200 cursor-pointer list-none flex items-center justify-between">
                      <span>
                        Q{idx + 1}: {pq.question}
                      </span>
                      <span className="text-xs font-mono text-cyan-400 group-open:rotate-90 transition-transform">
                        ▼
                      </span>
                    </summary>
                    <div className="mt-4 pt-3 border-t border-slate-800/80 text-slate-400 text-xs sm:text-sm leading-relaxed">
                      <strong className="text-emerald-400 font-mono">Answer: </strong>
                      {pq.answer}
                    </div>
                  </details>
                ))}
              </div>
            </div>
          )}

          {/* Bottom Next / Prev Navigation Bar */}
          <div className="mt-14 pt-8 border-t border-slate-800 flex flex-col sm:flex-row items-center justify-between gap-4">
            {chapter.prev_chapter ? (
              <Link
                href={`/learn/${course.slug}/${chapter.prev_chapter.slug}`}
                className="w-full sm:w-auto px-5 py-3 rounded-xl bg-slate-900 border border-slate-800 hover:border-slate-700 text-xs font-mono text-slate-300 hover:text-white flex items-center justify-center gap-2 transition-all"
              >
                <ChevronLeft className="w-4 h-4" />
                <span>Previous: {chapter.prev_chapter.title}</span>
              </Link>
            ) : (
              <div />
            )}

            {chapter.next_chapter ? (
              <Link
                href={`/learn/${course.slug}/${chapter.next_chapter.slug}`}
                className="w-full sm:w-auto px-6 py-3 rounded-xl font-mono text-xs font-bold text-slate-950 bg-gradient-to-r from-cyan-400 to-cyan-300 hover:from-cyan-300 hover:to-cyan-200 shadow-[0_0_20px_rgba(6,182,212,0.3)] flex items-center justify-center gap-2 transition-all"
              >
                <span>Next: {chapter.next_chapter.title}</span>
                <ChevronRight className="w-4 h-4" />
              </Link>
            ) : (
              <Link
                href={`/learn/${course.slug}/assessment`}
                className="w-full sm:w-auto px-6 py-3 rounded-xl font-mono text-xs font-bold text-slate-950 bg-gradient-to-r from-amber-400 to-amber-300 shadow-[0_0_20px_rgba(245,158,11,0.3)] flex items-center justify-center gap-2 transition-all"
              >
                <Award className="w-4 h-4" />
                <span>Take Certification Exam</span>
              </Link>
            )}
          </div>
        </main>
      </div>
    </div>
  );
}

// Simple HTML converter for standard markdown syntax
function formatMarkdown(md: string): string {
  if (!md) return '';
  let html = md
    .replace(/### (.*?)\n/g, '<h3>$1</h3>')
    .replace(/## (.*?)\n/g, '<h2>$1</h2>')
    .replace(/# (.*?)\n/g, '<h1>$1</h1>')
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
    .replace(/`([^`]+)`/g, '<code>$1</code>')
    .replace(/\n\n/g, '</p><p>')
    .replace(/\n/g, '<br/>');

  return `<p>${html}</p>`;
}
