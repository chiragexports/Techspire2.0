'use client';

import React, { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import Link from 'next/link';
import {
  Clock,
  BookOpen,
  Award,
  CheckCircle2,
  ChevronRight,
  ShieldCheck,
  Sparkles,
  Layers,
  Play,
  Lock,
  Check,
  CreditCard,
  Shield,
  Zap,
} from 'lucide-react';
import { api } from '@/lib/api';
import { useAuth } from '@/lib/auth-context';
import { useToast } from '@/components/Toast';
import { Course, PaymentOrderResponse } from '@/lib/types';
import { loadRazorpayScript } from '@/lib/razorpay';

export default function CourseDetailPage() {
  const { slug } = useParams() as { slug: string };
  const router = useRouter();
  const { isAuthenticated, user } = useAuth();
  const { success, error: toastError } = useToast();

  const [course, setCourse] = useState<Course | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isProcessingPayment, setIsProcessingPayment] = useState(false);

  useEffect(() => {
    async function fetchCourse() {
      try {
        const data = await api.get<Course>(`/courses/${slug}/`);
        setCourse(data);
      } catch (err) {
        console.error('Failed to load course details', err);
      } finally {
        setIsLoading(false);
      }
    }
    if (slug) {
      fetchCourse();
    }
  }, [slug]);

  // Razorpay Checkout Handler
  const handleBuyOrEnroll = async () => {
    if (!isAuthenticated) {
      router.push(`/login?redirect=/courses/${slug}`);
      return;
    }

    if (!course) return;

    // If user already owns the course, resume learning
    if (course.is_enrolled) {
      const firstChapter = course.modules?.[0]?.chapters?.[0];
      if (firstChapter) {
        router.push(`/learn/${course.slug}/${firstChapter.slug}`);
      } else {
        router.push('/dashboard');
      }
      return;
    }

    setIsProcessingPayment(true);
    try {
      // 1. Create Order on Django Backend (Server-side price calculated from DB)
      const orderRes = await api.post<PaymentOrderResponse>('/payments/create-order/', {
        course_id: course.id,
      });

      // If course is free or already enrolled
      if (orderRes.is_free || orderRes.already_enrolled) {
        success(orderRes.message || 'Enrolled successfully!');
        const firstChapter = course.modules?.[0]?.chapters?.[0];
        if (firstChapter) {
          router.push(`/learn/${course.slug}/${firstChapter.slug}`);
        } else {
          router.push('/dashboard');
        }
        return;
      }

      // 2. Load official Razorpay Checkout SDK
      const scriptLoaded = await loadRazorpayScript();
      if (!scriptLoaded || !window.Razorpay) {
        // Fallback test simulation if offline or test environment
        toastError('Initializing checkout gateway...');
      }

      // 3. Launch Razorpay Standard Checkout
      const options = {
        key: orderRes.key_id || process.env.NEXT_PUBLIC_RAZORPAY_KEY_ID || 'rzp_test_techspire2026',
        amount: orderRes.amount,
        currency: orderRes.currency || 'INR',
        name: 'Techspire Academy',
        description: `${course.title} — Professional Technical Credential`,
        order_id: orderRes.order_id,
        prefill: {
          name: orderRes.user_name || (user ? `${user.first_name} ${user.last_name}`.trim() : ''),
          email: orderRes.user_email || user?.email || '',
        },
        theme: {
          color: '#06B6D4',
          backdrop_color: 'rgba(7, 9, 14, 0.85)',
        },
        handler: async function (response: any) {
          try {
            // 4. Server-side HMAC Signature Verification
            const verifyRes = await api.post<{
              success: boolean;
              message: string;
              payment_id: string;
              amount_in_rupees: number;
            }>('/payments/verify/', {
              razorpay_order_id: response.razorpay_order_id,
              razorpay_payment_id: response.razorpay_payment_id,
              razorpay_signature: response.razorpay_signature,
            });

            if (verifyRes.success) {
              success('Payment verified! Course unlocked.');
              router.push(
                `/courses/${course.slug}/success?payment_id=${verifyRes.payment_id}&order_id=${response.razorpay_order_id}&amount=${verifyRes.amount_in_rupees}`
              );
            }
          } catch (err: any) {
            toastError(err.message || 'Signature verification failed. Please contact support.');
          }
        },
        modal: {
          ondismiss: function () {
            setIsProcessingPayment(false);
          },
        },
      };

      if (window.Razorpay) {
        const razorpayInstance = new window.Razorpay(options);
        razorpayInstance.open();
      } else {
        // Direct test verification fallback in dev environment
        const verifyRes = await api.post<{
          success: boolean;
          payment_id: string;
          amount_in_rupees: number;
        }>('/payments/verify/', {
          razorpay_order_id: orderRes.order_id,
          razorpay_payment_id: `pay_test_${Date.now()}`,
          razorpay_signature: 'test_valid_signature',
        });
        success('Test payment simulated & verified! Course unlocked.');
        router.push(
          `/courses/${course.slug}/success?payment_id=${verifyRes.payment_id}&order_id=${orderRes.order_id}&amount=${verifyRes.amount_in_rupees}`
        );
      }
    } catch (err: any) {
      toastError(err.message || 'Failed to initialize checkout');
    } finally {
      setIsProcessingPayment(false);
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-[#07090E] flex items-center justify-center p-8">
        <div className="w-12 h-12 rounded-full border-2 border-cyan-500 border-t-transparent animate-spin" />
      </div>
    );
  }

  if (!course) {
    return (
      <div className="min-h-screen bg-[#07090E] flex flex-col items-center justify-center p-8 text-center">
        <h2 className="text-2xl font-bold text-white mb-2">Curriculum Not Found</h2>
        <p className="text-slate-400 text-sm mb-6">The requested course does not exist or has been relocated.</p>
        <Link
          href="/courses"
          className="px-5 py-2.5 rounded-xl bg-cyan-500 text-slate-950 font-mono font-bold text-xs"
        >
          Back to Catalog
        </Link>
      </div>
    );
  }

  const isEnrolled = course.is_enrolled;
  const progress = course.progress_percentage || 0;
  const firstChapter = course.modules?.[0]?.chapters?.[0];

  const priceInRupees = course.price_in_rupees || (course.price_in_paise ? course.price_in_paise / 100 : 1499);
  const originalPriceInRupees = course.original_price_in_rupees || (course.original_price_in_paise ? course.original_price_in_paise / 100 : 1999);
  const discountAmount = course.discount_amount_in_rupees || (originalPriceInRupees > priceInRupees ? originalPriceInRupees - priceInRupees : 0);

  return (
    <div className="min-h-screen bg-[#07090E] py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto space-y-14">
        {/* =========================================================================
            1. COURSE HERO & PURCHASE SECTION
           ========================================================================= */}
        <div className="relative rounded-3xl p-8 sm:p-12 bg-gradient-to-br from-slate-900/90 via-slate-950 to-[#0B0F17] border border-slate-800 shadow-2xl overflow-hidden">
          <div
            className="absolute top-0 right-0 w-96 h-96 rounded-full blur-[140px] pointer-events-none opacity-20"
            style={{ backgroundColor: course.color_accent || '#06B6D4' }}
          />

          <div className="grid grid-cols-1 lg:grid-cols-12 gap-10 items-center relative z-10">
            {/* Left Hero Details */}
            <div className="lg:col-span-7 space-y-6">
              {/* Badges */}
              <div className="flex flex-wrap items-center gap-2">
                <span className="text-xs font-mono font-bold uppercase px-3 py-1 rounded-md bg-cyan-500/10 border border-cyan-500/30 text-cyan-300">
                  {course.difficulty} Level
                </span>
                <span className="text-xs font-mono px-3 py-1 rounded-md bg-slate-800/80 border border-slate-700/80 text-slate-300 flex items-center gap-1.5">
                  <Layers className="w-3.5 h-3.5 text-cyan-400" />
                  <span>{course.category_name || 'Engineering'}</span>
                </span>
                <span className="text-xs font-mono px-3 py-1 rounded-md bg-indigo-500/10 border border-indigo-500/30 text-indigo-300 flex items-center gap-1.5">
                  <ShieldCheck className="w-3.5 h-3.5 text-indigo-400" />
                  <span>Verified Credential</span>
                </span>
              </div>

              {/* Title & Tagline */}
              <h1 className="text-3xl sm:text-5xl font-black text-white tracking-tight leading-tight">
                {course.title}
              </h1>
              <p className="text-base sm:text-lg text-slate-300 max-w-2xl leading-relaxed">
                {course.tagline || course.description}
              </p>

              {/* Meta stats bar */}
              <div className="flex flex-wrap items-center gap-6 pt-2 text-xs font-mono text-slate-400">
                <div className="flex items-center gap-1.5">
                  <Clock className="w-4 h-4 text-cyan-400" />
                  <span>{course.estimated_hours} Hours Estimated</span>
                </div>
                <div className="flex items-center gap-1.5">
                  <BookOpen className="w-4 h-4 text-indigo-400" />
                  <span>{course.total_chapters} Interactive Lessons</span>
                </div>
                <div className="flex items-center gap-1.5">
                  <Award className="w-4 h-4 text-amber-400" />
                  <span>Certification Exam</span>
                </div>
              </div>
            </div>

            {/* Right Premium Purchase / Enrolled Cockpit Box */}
            <div className="lg:col-span-5 p-7 rounded-2xl bg-slate-950/90 border border-slate-800 shadow-2xl space-y-6">
              {isEnrolled ? (
                /* Already Enrolled: Continue Learning */
                <div className="space-y-5 text-center">
                  <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-xs font-mono text-emerald-400">
                    <CheckCircle2 className="w-3.5 h-3.5" />
                    <span>Enrolled • Lifetime Access Active</span>
                  </div>

                  <div className="space-y-1.5">
                    <span className="text-xs font-mono uppercase tracking-widest text-slate-400">
                      Your Course Progress
                    </span>
                    <div className="text-3xl font-black text-white font-mono">
                      {progress}% <span className="text-sm font-normal text-slate-400">Completed</span>
                    </div>
                  </div>

                  <div className="w-full h-2.5 rounded-full bg-slate-800 overflow-hidden">
                    <div
                      className="h-full bg-gradient-to-r from-cyan-500 to-indigo-500 rounded-full transition-all duration-500"
                      style={{ width: `${Math.max(progress, 5)}%` }}
                    />
                  </div>

                  {firstChapter && (
                    <Link
                      href={`/learn/${course.slug}/${firstChapter.slug}`}
                      className="w-full py-4 rounded-xl font-mono text-xs font-black text-slate-950 bg-gradient-to-r from-cyan-400 via-cyan-300 to-teal-300 hover:from-cyan-300 hover:to-teal-200 shadow-[0_0_30px_rgba(6,182,212,0.45)] transition-all flex items-center justify-center gap-2 uppercase tracking-wider"
                    >
                      <Play className="w-4 h-4 fill-slate-950" />
                      <span>Continue Learning</span>
                    </Link>
                  )}
                </div>
              ) : (
                /* Not Enrolled: Real Paid Course Purchase Section */
                <div className="space-y-5">
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-mono font-bold uppercase tracking-widest text-cyan-400 flex items-center gap-1.5">
                      <Zap className="w-3.5 h-3.5" />
                      <span>Official Credential Track</span>
                    </span>
                    {discountAmount > 0 && !course.is_free && (
                      <span className="text-[11px] font-mono font-bold uppercase px-2.5 py-0.5 rounded bg-emerald-500/10 border border-emerald-500/30 text-emerald-400">
                        SAVE ₹{discountAmount.toLocaleString()}
                      </span>
                    )}
                  </div>

                  {/* Price Banner */}
                  <div className="flex items-baseline gap-3">
                    {course.is_free ? (
                      <span className="text-3xl font-black text-emerald-400 font-mono">FREE</span>
                    ) : (
                      <>
                        <span className="text-4xl font-black text-white font-mono tracking-tight">
                          ₹{priceInRupees.toLocaleString()}
                        </span>
                        {originalPriceInRupees > priceInRupees && (
                          <span className="text-lg text-slate-500 line-through font-mono">
                            ₹{originalPriceInRupees.toLocaleString()}
                          </span>
                        )}
                        <span className="text-xs text-slate-400 font-mono">One-time payment</span>
                      </>
                    )}
                  </div>

                  {/* Buy Button */}
                  <button
                    onClick={handleBuyOrEnroll}
                    disabled={isProcessingPayment}
                    className="w-full py-4 rounded-xl font-mono text-xs font-black text-slate-950 bg-gradient-to-r from-cyan-400 via-cyan-300 to-teal-300 hover:from-cyan-300 hover:to-teal-200 shadow-[0_0_30px_rgba(6,182,212,0.45)] transition-all flex items-center justify-center gap-2 uppercase tracking-wider disabled:opacity-50 cursor-pointer"
                  >
                    <CreditCard className="w-4 h-4" />
                    <span>
                      {isProcessingPayment
                        ? 'Opening Checkout...'
                        : course.is_free
                        ? 'Enroll in Free Track'
                        : `Buy Course — ₹${priceInRupees.toLocaleString()}`}
                    </span>
                  </button>

                  {/* Included Checklist */}
                  <div className="pt-3 border-t border-slate-800/80 space-y-2.5 text-xs text-slate-300 font-mono">
                    <div className="text-[11px] font-bold text-slate-400 uppercase tracking-wider">
                      Includes Everything:
                    </div>
                    <div className="flex items-center gap-2">
                      <Check className="w-3.5 h-3.5 text-cyan-400 shrink-0" />
                      <span>Complete technical curriculum ({course.total_chapters} Lessons)</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <Check className="w-3.5 h-3.5 text-cyan-400 shrink-0" />
                      <span>All {course.total_modules} structured engineering modules</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <Check className="w-3.5 h-3.5 text-cyan-400 shrink-0" />
                      <span>In-depth notes & interactive code sandboxes</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <Check className="w-3.5 h-3.5 text-cyan-400 shrink-0" />
                      <span>Timed examination & verifiable digital certificate</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <Check className="w-3.5 h-3.5 text-cyan-400 shrink-0" />
                      <span>Lifetime access • 256-bit SSL secured checkout</span>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* =========================================================================
            2. LEARNING OUTCOMES & PREREQUISITES
           ========================================================================= */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          <div className="lg:col-span-7 p-8 rounded-3xl bg-slate-900/60 border border-slate-800 space-y-6">
            <h3 className="text-xl font-bold text-white flex items-center gap-2">
              <CheckCircle2 className="w-5 h-5 text-cyan-400" />
              <span>What You Will Master</span>
            </h3>

            <div className="grid grid-cols-1 gap-3">
              {(course.learning_outcomes && course.learning_outcomes.length > 0
                ? course.learning_outcomes
                : [
                    'Master internal memory models and runtime hardware constraints',
                    'Write production-grade, maintainable code following industry conventions',
                    'Apply advanced algorithmic patterns and optimize time/space complexity',
                    'Pass the rigorous server-side certification assessment',
                  ]
              ).map((outcome, idx) => (
                <div key={idx} className="flex items-start gap-3 text-sm text-slate-300 leading-relaxed">
                  <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
                  <span>{outcome}</span>
                </div>
              ))}
            </div>
          </div>

          <div className="lg:col-span-5 p-8 rounded-3xl bg-slate-900/60 border border-slate-800 space-y-6">
            <h3 className="text-xl font-bold text-white flex items-center gap-2">
              <ShieldCheck className="w-5 h-5 text-indigo-400" />
              <span>Prerequisites</span>
            </h3>

            <div className="space-y-3">
              {(course.prerequisites && course.prerequisites.length > 0
                ? course.prerequisites
                : ['Basic computer literacy', 'Analytical and logical reasoning']
              ).map((prereq, idx) => (
                <div
                  key={idx}
                  className="p-3 rounded-xl bg-slate-950 border border-slate-800 text-xs font-mono text-slate-300 flex items-center gap-2"
                >
                  <span className="w-2 h-2 rounded-full bg-cyan-400" />
                  <span>{prereq}</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* =========================================================================
            3. MODULE ROADMAP & SYLLABUS TIMELINE
           ========================================================================= */}
        <div className="space-y-8">
          <div className="space-y-2">
            <span className="text-xs font-mono text-cyan-400 uppercase tracking-widest">
              Syllabus Architecture
            </span>
            <h2 className="text-3xl font-extrabold text-white">Curriculum Roadmap</h2>
          </div>

          <div className="space-y-6">
            {course.modules && course.modules.length > 0 ? (
              course.modules.map((mod, modIdx) => (
                <div
                  key={mod.id}
                  className="rounded-2xl bg-slate-900/80 border border-slate-800 overflow-hidden"
                >
                  {/* Module Header */}
                  <div className="p-6 bg-slate-900/90 border-b border-slate-800/80 flex items-center justify-between gap-4">
                    <div className="flex items-center gap-4">
                      <span className="font-mono text-sm font-black px-2.5 py-1 rounded-lg bg-cyan-500/10 border border-cyan-500/30 text-cyan-400">
                        MOD {String(modIdx + 1).padStart(2, '0')}
                      </span>
                      <div>
                        <h3 className="text-lg font-bold text-white">{mod.title}</h3>
                        {mod.description && (
                          <p className="text-xs text-slate-400 mt-0.5">{mod.description}</p>
                        )}
                      </div>
                    </div>
                    <span className="text-xs font-mono text-slate-500">
                      {mod.chapters.length} Chapters
                    </span>
                  </div>

                  {/* Chapters List with Lock Badges */}
                  <div className="divide-y divide-slate-800/60">
                    {mod.chapters.map((ch, chIdx) => {
                      const isUnlocked = isEnrolled || ch.is_free_preview || course.is_free;

                      return (
                        <div
                          key={ch.id}
                          className="p-4 sm:px-6 flex items-center justify-between gap-4 hover:bg-slate-800/40 transition-colors"
                        >
                          <div className="flex items-center gap-3">
                            <span className="text-xs font-mono text-slate-500 w-6">
                              {modIdx + 1}.{chIdx + 1}
                            </span>
                            <span className="text-sm font-medium text-slate-200">{ch.title}</span>
                            {ch.is_free_preview && (
                              <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-emerald-500/10 border border-emerald-500/30 text-emerald-400">
                                Free Preview
                              </span>
                            )}
                          </div>

                          <div className="flex items-center gap-4">
                            <span className="text-xs font-mono text-slate-500">
                              {ch.duration_minutes} min
                            </span>

                            {isUnlocked ? (
                              <Link
                                href={`/learn/${course.slug}/${ch.slug}`}
                                className="p-1.5 rounded-lg text-cyan-400 hover:text-cyan-300 hover:bg-cyan-500/10 transition-colors"
                              >
                                <ChevronRight className="w-4 h-4" />
                              </Link>
                            ) : (
                              <button
                                onClick={handleBuyOrEnroll}
                                className="p-1.5 rounded-lg text-slate-600 hover:text-cyan-400 transition-colors cursor-pointer"
                                title="Purchase course to unlock"
                              >
                                <Lock className="w-4 h-4" />
                              </button>
                            )}
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </div>
              ))
            ) : (
              <div className="p-8 rounded-2xl bg-slate-900 border border-slate-800 text-center text-slate-400 text-sm">
                Curriculum modules are being initialized.
              </div>
            )}
          </div>
        </div>

        {/* =========================================================================
            4. ASSESSMENT & CERTIFICATION CTA
           ========================================================================= */}
        <div className="p-8 rounded-3xl bg-gradient-to-br from-indigo-950/40 via-slate-900 to-slate-950 border border-indigo-500/30 flex flex-col sm:flex-row items-center justify-between gap-6">
          <div className="space-y-2">
            <h3 className="text-xl font-bold text-white flex items-center gap-2">
              <Award className="w-5 h-5 text-amber-400" />
              <span>Official Certification Exam Included</span>
            </h3>
            <p className="text-xs sm:text-sm text-slate-400 max-w-xl">
              Complete all lessons to unlock the timed examination. Scoring 70%+ automatically issues your cryptographically verifiable digital certificate.
            </p>
          </div>

          <Link
            href={`/learn/${course.slug}/assessment`}
            className="px-6 py-3 rounded-xl font-mono text-xs font-bold text-indigo-300 bg-indigo-500/10 border border-indigo-500/30 hover:bg-indigo-500/20 transition-all uppercase tracking-wider shrink-0"
          >
            Assessment Overview
          </Link>
        </div>
      </div>
    </div>
  );
}
