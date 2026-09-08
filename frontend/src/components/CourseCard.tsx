import React from 'react';
import Link from 'next/link';
import { Clock, BookOpen, ChevronRight, Award, Layers } from 'lucide-react';
import { Course } from '@/lib/types';

interface CourseCardProps {
  course: Course;
}

export function CourseCard({ course }: CourseCardProps) {
  const difficultyStyles = {
    beginner: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30',
    intermediate: 'bg-cyan-500/10 text-cyan-400 border-cyan-500/30',
    advanced: 'bg-indigo-500/10 text-indigo-400 border-indigo-500/30',
  };

  const isEnrolled = course.is_enrolled;
  const progress = course.progress_percentage || 0;

  return (
    <div className="group relative rounded-2xl bg-gradient-to-b from-slate-900/90 to-slate-950 border border-slate-800/80 hover:border-cyan-500/50 hover:shadow-[0_10px_35px_rgba(6,182,212,0.15)] transition-all duration-300 flex flex-col justify-between overflow-hidden">
      {/* Top Accent Gradient Bar */}
      <div
        className="h-1.5 w-full bg-gradient-to-r from-cyan-500 via-indigo-500 to-transparent"
        style={{
          background: `linear-gradient(90deg, ${course.color_accent || '#06B6D4'}, #6366F1, transparent)`,
        }}
      />

      <div className="p-6 flex-1 flex flex-col justify-between">
        <div>
          {/* Badges Bar */}
          <div className="flex items-center justify-between gap-2 mb-4">
            <span
              className={`text-[11px] font-mono font-semibold uppercase px-2.5 py-1 rounded-md border ${
                difficultyStyles[course.difficulty] || difficultyStyles.beginner
              }`}
            >
              {course.difficulty}
            </span>

            <div className="flex items-center gap-1.5 text-xs text-slate-400 font-mono">
              <Layers className="w-3.5 h-3.5 text-slate-500" />
              <span>{course.category_name || 'Curriculum'}</span>
            </div>
          </div>

          {/* Title & Tagline */}
          <Link href={`/courses/${course.slug}`}>
            <h3 className="text-xl font-bold text-slate-100 group-hover:text-cyan-300 transition-colors line-clamp-1">
              {course.title}
            </h3>
          </Link>
          <p className="text-sm text-slate-400 mt-2 line-clamp-2 leading-relaxed">
            {course.tagline || course.description}
          </p>
        </div>

        {/* Progress Section if Enrolled */}
        {isEnrolled ? (
          <div className="mt-4 pt-3 border-t border-slate-800/60">
            <div className="flex items-center justify-between text-xs font-mono mb-1.5">
              <span className="text-slate-400">Your Progress</span>
              <span className="text-cyan-400 font-bold">{progress}%</span>
            </div>
            <div className="w-full h-2 rounded-full bg-slate-800 overflow-hidden">
              <div
                className="h-full bg-gradient-to-r from-cyan-500 to-indigo-500 rounded-full transition-all duration-500"
                style={{ width: `${Math.max(progress, 4)}%` }}
              />
            </div>
          </div>
        ) : (
          /* Real Database Price Display */
          <div className="mt-4 pt-3 border-t border-slate-800/60 flex items-center justify-between">
            <div className="flex items-baseline gap-2">
              {course.is_free ? (
                <span className="text-base font-black text-emerald-400 font-mono">
                  FREE
                </span>
              ) : (
                <>
                  <span className="text-lg font-black text-white font-mono tracking-tight">
                    ₹{(course.price_in_rupees || (course.price_in_paise ? course.price_in_paise / 100 : 1499)).toLocaleString()}
                  </span>
                  {course.original_price_in_rupees && course.original_price_in_rupees > (course.price_in_rupees || 0) && (
                    <span className="text-xs text-slate-500 line-through font-mono">
                      ₹{course.original_price_in_rupees.toLocaleString()}
                    </span>
                  )}
                </>
              )}
            </div>

            {course.discount_amount_in_rupees && course.discount_amount_in_rupees > 0 && !course.is_free && (
              <span className="text-[10px] font-mono font-bold uppercase px-2 py-0.5 rounded bg-emerald-500/10 border border-emerald-500/30 text-emerald-400">
                SAVE ₹{course.discount_amount_in_rupees.toLocaleString()}
              </span>
            )}
          </div>
        )}

        {/* Meta Stats & Footer */}
        <div className="mt-4 pt-3 border-t border-slate-800/60 flex items-center justify-between">
          <div className="flex items-center gap-3.5 text-xs text-slate-400">
            <div className="flex items-center gap-1">
              <Clock className="w-3.5 h-3.5 text-cyan-400" />
              <span>{course.estimated_hours}h</span>
            </div>
            <div className="flex items-center gap-1">
              <BookOpen className="w-3.5 h-3.5 text-indigo-400" />
              <span>{course.total_chapters} Lessons</span>
            </div>
            {course.has_assessment !== false && (
              <div className="flex items-center gap-1 hidden sm:flex">
                <Award className="w-3.5 h-3.5 text-amber-400" />
                <span>Certificate</span>
              </div>
            )}
          </div>

          <Link
            href={`/courses/${course.slug}`}
            className="inline-flex items-center gap-1 text-xs font-bold font-mono text-cyan-400 group-hover:text-cyan-300 group-hover:translate-x-0.5 transition-all"
          >
            <span>{isEnrolled ? 'Continue' : 'View Course'}</span>
            <ChevronRight className="w-4 h-4" />
          </Link>
        </div>
      </div>
    </div>
  );
}
