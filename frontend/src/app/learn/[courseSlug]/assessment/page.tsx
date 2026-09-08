'use client';

import React, { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import Link from 'next/link';
import confetti from 'canvas-confetti';
import {
  Timer,
  CheckCircle2,
  AlertCircle,
  Award,
  ChevronRight,
  ChevronLeft,
  RotateCcw,
  Check,
  X,
  ShieldCheck,
  FileCheck,
  Share2,
} from 'lucide-react';
import { api } from '@/lib/api';
import { useAuth } from '@/lib/auth-context';
import { useToast } from '@/components/Toast';
import { CodeBlock } from '@/components/CodeBlock';
import { AssessmentDetail, AssessmentAttempt } from '@/lib/types';

export default function AssessmentExamPage() {
  const { courseSlug } = useParams() as { courseSlug: string };
  const router = useRouter();
  const { isAuthenticated } = useAuth();
  const { success, error: toastError } = useToast();

  const [assessment, setAssessment] = useState<AssessmentDetail | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Exam taking states
  const [currentQuestionIdx, setCurrentQuestionIdx] = useState(0);
  const [answers, setAnswers] = useState<Record<string, number>>({}); // { question_id: option_id }
  const [timeLeftSeconds, setTimeLeftSeconds] = useState(1200); // 20 minutes default
  const [submittedResult, setSubmittedResult] = useState<{
    passed: boolean;
    score: number;
    total_points: number;
    percentage: number;
    passing_score: number;
    certificate_code?: string;
    certificate_id?: string;
    attempt?: AssessmentAttempt;
  } | null>(null);

  useEffect(() => {
    async function loadAssessment() {
      if (!isAuthenticated) {
        router.push(`/login?redirect=/learn/${courseSlug}/assessment`);
        return;
      }

      setIsLoading(true);
      try {
        const data = await api.get<AssessmentDetail>(`/assessments/course/${courseSlug}/`);
        setAssessment(data);
        if (data.time_limit_minutes) {
          setTimeLeftSeconds(data.time_limit_minutes * 60);
        }
      } catch (err: any) {
        toastError(err.message || 'Failed to load assessment');
      } finally {
        setIsLoading(false);
      }
    }

    if (courseSlug) {
      loadAssessment();
    }
  }, [courseSlug, isAuthenticated]);

  // Timer Countdown
  useEffect(() => {
    if (submittedResult || isLoading || !assessment) return;

    const interval = setInterval(() => {
      setTimeLeftSeconds((prev) => {
        if (prev <= 1) {
          clearInterval(interval);
          handleSubmitExam();
          return 0;
        }
        return prev - 1;
      });
    }, 1000);

    return () => clearInterval(interval);
  }, [submittedResult, isLoading, assessment]);

  const handleSelectOption = (questionId: number, optionId: number) => {
    if (submittedResult) return; // Locked once submitted
    setAnswers((prev) => ({
      ...prev,
      [String(questionId)]: optionId,
    }));
  };

  const handleSubmitExam = async () => {
    if (!assessment) return;

    setIsSubmitting(true);
    try {
      const timeSpent = assessment.time_limit_minutes * 60 - timeLeftSeconds;
      const res = await api.post<any>(`/assessments/${assessment.id}/submit/`, {
        answers,
        time_spent_seconds: Math.max(timeSpent, 5),
      });

      setSubmittedResult(res);

      if (res.passed) {
        // Trigger celebratory confetti
        confetti({
          particleCount: 120,
          spread: 80,
          origin: { y: 0.6 },
          colors: ['#06B6D4', '#6366F1', '#10B981', '#F59E0B'],
        });
        success(`Congratulations! You passed with ${res.percentage}% score!`);
      } else {
        toastError(`Score: ${res.percentage}%. Minimum passing threshold is ${res.passing_score}%.`);
      }
    } catch (err: any) {
      toastError(err.message || 'Failed to submit exam');
    } finally {
      setIsSubmitting(false);
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-[85vh] bg-[#07090E] flex items-center justify-center">
        <div className="flex flex-col items-center gap-4">
          <div className="w-10 h-10 rounded-full border-2 border-cyan-500 border-t-transparent animate-spin" />
          <span className="text-xs font-mono text-slate-400">Loading Assessment Environment...</span>
        </div>
      </div>
    );
  }

  if (!assessment) {
    return (
      <div className="min-h-[80vh] flex flex-col items-center justify-center p-8 text-center bg-[#07090E]">
        <h2 className="text-xl font-bold text-white mb-2">No Assessment Available</h2>
        <p className="text-xs text-slate-400 mb-6">This course does not currently have an active examination.</p>
        <Link
          href={`/courses/${courseSlug}`}
          className="px-4 py-2 rounded-xl bg-cyan-500 text-slate-950 font-mono text-xs font-bold"
        >
          Return to Course
        </Link>
      </div>
    );
  }

  const currentQ = assessment.questions[currentQuestionIdx];
  const totalQuestions = assessment.questions.length;
  const answeredCount = Object.keys(answers).length;

  const formatTimer = (secs: number) => {
    const m = Math.floor(secs / 60);
    const s = secs % 60;
    return `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`;
  };

  return (
    <div className="min-h-screen bg-[#07090E] text-slate-100 py-10 px-4 sm:px-6 lg:px-8">
      <div className="max-w-5xl mx-auto space-y-8">
        {/* =====================================================================
            TOP EXAM HUD
           ===================================================================== */}
        <div className="p-6 rounded-2xl bg-slate-900/90 border border-slate-800 flex flex-col sm:flex-row items-center justify-between gap-4 shadow-xl">
          <div>
            <div className="flex items-center gap-2 text-xs font-mono text-cyan-400 uppercase tracking-wider">
              <Award className="w-4 h-4" />
              <span>Official Certification Exam</span>
            </div>
            <h1 className="text-xl font-bold text-white mt-1">{assessment.title}</h1>
            <p className="text-xs text-slate-400 font-mono mt-0.5">
              Passing threshold: {assessment.passing_score}% • {totalQuestions} Questions
            </p>
          </div>

          {!submittedResult && (
            <div className="flex items-center gap-4">
              {/* Live Timer */}
              <div
                className={`flex items-center gap-2 px-4 py-2 rounded-xl border font-mono text-sm font-bold ${
                  timeLeftSeconds < 180
                    ? 'bg-rose-500/10 border-rose-500/40 text-rose-400 animate-pulse'
                    : 'bg-slate-950 border-slate-800 text-cyan-300'
                }`}
              >
                <Timer className="w-4 h-4" />
                <span>{formatTimer(timeLeftSeconds)}</span>
              </div>

              {/* Progress counter */}
              <div className="text-xs font-mono text-slate-400">
                <span>
                  {answeredCount}/{totalQuestions} Answered
                </span>
              </div>
            </div>
          )}
        </div>

        {/* =====================================================================
            POST-SUBMISSION SCORE RESULTS DASHBOARD
           ===================================================================== */}
        {submittedResult && (
          <div
            className={`p-8 rounded-3xl border shadow-2xl space-y-6 ${
              submittedResult.passed
                ? 'bg-gradient-to-br from-emerald-950/40 via-slate-900 to-slate-950 border-emerald-500/40'
                : 'bg-gradient-to-br from-rose-950/40 via-slate-900 to-slate-950 border-rose-500/40'
            }`}
          >
            <div className="flex flex-col sm:flex-row items-center justify-between gap-6">
              <div className="space-y-2 text-center sm:text-left">
                <span
                  className={`text-xs font-mono font-bold uppercase tracking-widest px-3 py-1 rounded-md border ${
                    submittedResult.passed
                      ? 'bg-emerald-500/20 text-emerald-300 border-emerald-500/40'
                      : 'bg-rose-500/20 text-rose-300 border-rose-500/40'
                  }`}
                >
                  {submittedResult.passed ? 'EXAMINATION PASSED' : 'EXAMINATION FAILED'}
                </span>

                <h2 className="text-3xl font-extrabold text-white mt-2">
                  Final Score: {submittedResult.percentage}% ({submittedResult.score}/
                  {submittedResult.total_points} pts)
                </h2>
                <p className="text-xs text-slate-400 max-w-xl">
                  {submittedResult.passed
                    ? 'Congratulations! Your score exceeds the certification standard. Your official credential has been minted and cryptographically signed.'
                    : `You scored ${submittedResult.percentage}%. The minimum required score is ${submittedResult.passing_score}%. Review your answers below and retake when ready.`}
                </p>
              </div>

              {/* Action Buttons */}
              <div className="flex flex-col gap-3 w-full sm:w-auto">
                {submittedResult.passed && submittedResult.certificate_code && (
                  <Link
                    href={`/verify/${submittedResult.certificate_code}`}
                    className="px-6 py-3 rounded-xl font-mono text-xs font-bold text-slate-950 bg-gradient-to-r from-emerald-400 to-cyan-400 shadow-[0_0_25px_rgba(16,185,129,0.3)] text-center uppercase tracking-wider"
                  >
                    View Official Certificate
                  </Link>
                )}

                <button
                  onClick={() => {
                    setSubmittedResult(null);
                    setAnswers({});
                    setTimeLeftSeconds(assessment.time_limit_minutes * 60);
                  }}
                  className="px-6 py-3 rounded-xl font-mono text-xs font-semibold text-slate-200 bg-slate-900 border border-slate-800 hover:bg-slate-800 text-center flex items-center justify-center gap-2"
                >
                  <RotateCcw className="w-4 h-4" />
                  <span>Retake Examination</span>
                </button>
              </div>
            </div>
          </div>
        )}

        {/* =====================================================================
            QUESTION NAVIGATION MATRIX
           ===================================================================== */}
        <div className="flex items-center gap-2 flex-wrap p-4 rounded-2xl bg-slate-900/60 border border-slate-800">
          <span className="text-xs font-mono text-slate-400 mr-2">Jump to:</span>
          {assessment.questions.map((q, idx) => {
            const isAnswered = Boolean(answers[String(q.id)]);
            const isCurrent = idx === currentQuestionIdx;

            return (
              <button
                key={q.id}
                onClick={() => setCurrentQuestionIdx(idx)}
                className={`w-8 h-8 rounded-lg font-mono text-xs font-bold transition-all ${
                  isCurrent
                    ? 'bg-cyan-400 text-slate-950 shadow-[0_0_15px_rgba(6,182,212,0.4)]'
                    : isAnswered
                    ? 'bg-slate-800 text-cyan-300 border border-cyan-500/30'
                    : 'bg-slate-950 text-slate-500 border border-slate-800 hover:text-slate-300'
                }`}
              >
                {idx + 1}
              </button>
            );
          })}
        </div>

        {/* =====================================================================
            ACTIVE QUESTION & OPTIONS CARD
           ===================================================================== */}
        {currentQ && (
          <div className="p-8 rounded-3xl bg-slate-900/90 border border-slate-800 space-y-8 shadow-2xl">
            {/* Question Heading */}
            <div className="space-y-3">
              <div className="flex items-center justify-between text-xs font-mono text-slate-400">
                <span>
                  Question {currentQuestionIdx + 1} of {totalQuestions}
                </span>
                <span className="text-cyan-400">{currentQ.points} Points</span>
              </div>

              <h3 className="text-lg sm:text-xl font-bold text-slate-100 leading-snug">
                {currentQ.question_text}
              </h3>
            </div>

            {/* Code Context if present */}
            {currentQ.code_context && (
              <CodeBlock
                code={currentQ.code_context}
                language={currentQ.code_language || 'python'}
                title="Code snippet to evaluate"
              />
            )}

            {/* Options List */}
            <div className="space-y-3">
              {currentQ.options.map((option) => {
                const isSelected = answers[String(currentQ.id)] === option.id;

                return (
                  <button
                    key={option.id}
                    onClick={() => handleSelectOption(currentQ.id, option.id)}
                    disabled={Boolean(submittedResult)}
                    className={`w-full p-4 rounded-2xl border text-left text-sm font-medium transition-all flex items-center justify-between gap-4 ${
                      isSelected
                        ? 'bg-cyan-500/15 border-cyan-500 text-cyan-200 shadow-[0_0_20px_rgba(6,182,212,0.15)]'
                        : 'bg-slate-950 border-slate-800/80 text-slate-300 hover:border-slate-700 hover:bg-slate-900'
                    }`}
                  >
                    <span className="leading-relaxed">{option.option_text}</span>
                    <div
                      className={`w-5 h-5 rounded-full border flex items-center justify-center shrink-0 ${
                        isSelected
                          ? 'border-cyan-400 bg-cyan-400 text-slate-950'
                          : 'border-slate-700'
                      }`}
                    >
                      {isSelected && <Check className="w-3.5 h-3.5 stroke-[3]" />}
                    </div>
                  </button>
                );
              })}
            </div>

            {/* Post-Submission Answer Explanation (If Test Completed) */}
            {submittedResult?.attempt?.answers && (
              <div className="p-5 rounded-2xl bg-slate-950 border border-slate-800/90 text-xs text-slate-400 space-y-2">
                <span className="font-mono text-cyan-400 uppercase font-bold">
                  Evaluation Explanation:
                </span>
                <p className="leading-relaxed">
                  {submittedResult.attempt.answers[currentQuestionIdx]?.explanation ||
                    'Server answer validated.'}
                </p>
              </div>
            )}

            {/* Bottom Nav / Submit Button */}
            <div className="flex items-center justify-between pt-6 border-t border-slate-800">
              <button
                onClick={() => setCurrentQuestionIdx((prev) => Math.max(prev - 1, 0))}
                disabled={currentQuestionIdx === 0}
                className="px-4 py-2.5 rounded-xl font-mono text-xs text-slate-400 hover:text-white bg-slate-950 border border-slate-800 disabled:opacity-30"
              >
                Previous Question
              </button>

              {currentQuestionIdx < totalQuestions - 1 ? (
                <button
                  onClick={() => setCurrentQuestionIdx((prev) => Math.min(prev + 1, totalQuestions - 1))}
                  className="px-5 py-2.5 rounded-xl font-mono text-xs font-bold text-slate-950 bg-cyan-400 hover:bg-cyan-300 transition-all flex items-center gap-1.5"
                >
                  <span>Next Question</span>
                  <ChevronRight className="w-4 h-4" />
                </button>
              ) : !submittedResult ? (
                <button
                  onClick={handleSubmitExam}
                  disabled={isSubmitting}
                  className="px-6 py-2.5 rounded-xl font-mono text-xs font-bold text-slate-950 bg-gradient-to-r from-emerald-400 to-cyan-400 hover:shadow-[0_0_25px_rgba(16,185,129,0.4)] transition-all uppercase tracking-wider disabled:opacity-50"
                >
                  {isSubmitting ? 'Evaluating...' : 'Submit Examination'}
                </button>
              ) : null}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
