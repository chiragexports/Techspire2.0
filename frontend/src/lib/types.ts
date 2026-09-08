export type UserRole = 'student' | 'instructor' | 'admin';

export interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  role: UserRole;
  avatar?: string | null;
  headline?: string | null;
  bio?: string | null;
  github?: string | null;
  linkedin?: string | null;
  created_at: string;
  updated_at?: string;
  is_staff?: boolean;
  is_superuser?: boolean;
}

export interface Category {
  id: number;
  name: string;
  slug: string;
  icon: string;
  description?: string;
  courses_count?: number;
}

export interface ChapterOutline {
  id: number;
  title: string;
  slug: string;
  order: number;
  duration_minutes: number;
  is_free_preview: boolean;
  is_completed?: boolean;
}

export interface ChapterDetail {
  id: number;
  title: string;
  slug: string;
  order: number;
  duration_minutes: number;
  is_free_preview: boolean;
  content_markdown: string;
  code_snippet?: string;
  code_language: string;
  key_takeaways: string[];
  practice_questions: Array<{
    question: string;
    answer: string;
  }>;
  module_id: number;
  module_title: string;
  course_slug: string;
  course_title: string;
  is_completed: boolean;
  next_chapter?: { id: number; title: string; slug: string } | null;
  prev_chapter?: { id: number; title: string; slug: string } | null;
  created_at: string;
  updated_at: string;
}

export interface Module {
  id: number;
  title: string;
  description?: string;
  order: number;
  chapters: ChapterOutline[];
}

export type DifficultyLevel = 'beginner' | 'intermediate' | 'advanced';

export interface Course {
  id: number;
  title: string;
  slug: string;
  tagline: string;
  description: string;
  category: number | Category;
  category_name?: string;
  difficulty: DifficultyLevel;
  estimated_hours: number;
  cover_image?: string | null;
  badge_icon: string;
  color_accent: string;
  price_in_paise?: number;
  original_price_in_paise?: number;
  discount_price_in_paise?: number;
  currency?: string;
  is_free?: boolean;
  price_in_rupees?: number;
  original_price_in_rupees?: number;
  discount_amount_in_rupees?: number;
  discount_percentage?: number;
  total_modules: number;
  total_chapters: number;
  is_enrolled?: boolean;
  progress_percentage?: number;
  has_assessment?: boolean;
  prerequisites?: string[];
  learning_outcomes?: string[];
  modules?: Module[];
  created_at: string;
}

export interface PaymentOrderResponse {
  order_id: string;
  amount: number;
  amount_in_rupees: number;
  currency: string;
  key_id: string;
  course_title: string;
  course_slug: string;
  user_name: string;
  user_email: string;
  message?: string;
  already_enrolled?: boolean;
  is_free?: boolean;
  enrolled?: boolean;
}

export interface PaymentHistoryItem {
  id: string;
  razorpay_payment_id: string;
  order_id: string;
  course_title: string;
  course_slug: string;
  course_cover?: string;
  course_difficulty?: string;
  amount: number;
  amount_in_rupees: number;
  currency: string;
  status: 'created' | 'authorized' | 'captured' | 'failed' | 'refunded';
  method?: string;
  captured_at?: string;
  created_at: string;
}

export interface AdminPaymentItem {
  id: string;
  razorpay_payment_id: string;
  order_id: string;
  student_name: string;
  student_email: string;
  course_title: string;
  amount: number;
  amount_in_rupees: number;
  currency: string;
  status: 'created' | 'authorized' | 'captured' | 'failed' | 'refunded';
  method?: string;
  captured_at?: string;
  created_at: string;
}

export interface AdminPaymentAnalytics {
  total_revenue_in_rupees: number;
  today_revenue_in_rupees: number;
  month_revenue_in_rupees: number;
  total_orders: number;
  successful_payments: number;
  failed_payments: number;
  paid_enrollments: number;
  top_selling_courses: Array<{
    course_id: number;
    course_title: string;
    course_slug: string;
    total_sales: number;
    revenue_in_rupees: number;
  }>;
}

export interface Enrollment {
  id: number;
  course: Course;
  status: 'active' | 'completed' | 'dropped';
  paid?: boolean;
  purchase_price_in_paise?: number;
  enrolled_at: string;
  completed_at?: string | null;
  last_accessed_at: string;
  progress_percentage: number;
  completed_chapters_count: number;
  total_chapters_count: number;
  next_up_chapter?: {
    id: number;
    title: string;
    slug: string;
    module_title: string;
  } | null;
}

export interface AssessmentQuestionOption {
  id: number;
  option_text: string;
  order: number;
}

export interface AssessmentQuestion {
  id: number;
  question_text: string;
  question_type: 'single' | 'multiple' | 'code';
  code_context?: string;
  code_language?: string;
  points: number;
  order: number;
  options: AssessmentQuestionOption[];
}

export interface AssessmentDetail {
  id: number;
  title: string;
  description: string;
  passing_score: number;
  time_limit_minutes: number;
  course_title: string;
  course_slug: string;
  total_questions: number;
  total_points: number;
  questions: AssessmentQuestion[];
}

export interface AssessmentAnswerReview {
  id: number;
  question_text: string;
  explanation: string;
  selected_option_id?: number | null;
  selected_option_text?: string;
  correct_option_id?: number;
  correct_option_text?: string;
  is_correct: boolean;
  all_options: Array<{
    id: number;
    option_text: string;
    is_correct: boolean;
  }>;
}

export interface AssessmentAttempt {
  id: number;
  assessment_title: string;
  course_title: string;
  course_slug: string;
  score: number;
  total_points: number;
  percentage: number;
  passing_score: number;
  passed: boolean;
  time_spent_seconds: number;
  started_at: string;
  submitted_at: string;
  certificate_code?: string | null;
  answers: AssessmentAnswerReview[];
}

export interface Certificate {
  id: string;
  certificate_code: string;
  student_name?: string;
  student_email?: string;
  course_title: string;
  course_slug: string;
  course_badge?: string;
  category_name?: string;
  grade_percentage: number;
  issue_date: string;
  is_valid: boolean;
  verification_hash: string;
}

export interface PublicVerifiedCertificate {
  id: string;
  certificate_code: string;
  recipient_name: string;
  course_title: string;
  course_slug: string;
  course_difficulty: string;
  estimated_hours: number;
  grade_percentage: number;
  issue_date: string;
  is_valid: boolean;
  verification_hash: string;
}

export interface DashboardOverview {
  user: {
    id: number;
    name: string;
    email: string;
    headline?: string;
    avatar?: string | null;
    created_at: string;
  };
  stats: {
    total_enrolled: number;
    completed_courses: number;
    certificates_earned: number;
    average_score: number;
    learning_streak_days: number;
  };
  continue_learning?: Enrollment | null;
  enrolled_courses: Enrollment[];
  recent_activity: Array<{
    id: number;
    chapter_title: string;
    course_title: string;
    course_slug: string;
    chapter_slug: string;
    completed_at: string;
  }>;
}

export interface AdminAnalytics {
  metrics: {
    total_students: number;
    total_courses: number;
    total_chapters: number;
    total_enrollments: number;
    total_certificates: number;
    total_attempts: number;
    pass_rate: number;
    completion_rate: number;
  };
  top_courses: Array<{
    id: number;
    title: string;
    slug: string;
    student_count: number;
    difficulty: string;
    estimated_hours: number;
  }>;
  recent_enrollments: Array<{
    id: number;
    user_name: string;
    user_email: string;
    course_title: string;
    status: string;
    enrolled_at: string;
  }>;
  recent_certificates: Array<{
    id: string;
    certificate_code: string;
    student_name: string;
    course_title: string;
    grade_percentage: number;
    issue_date: string;
  }>;
}
