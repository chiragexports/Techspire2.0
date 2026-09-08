'use client';

import React, { useState, useEffect, useMemo, Suspense } from 'react';
import { useSearchParams } from 'next/navigation';
import {
  Search,
  Filter,
  SlidersHorizontal,
  BookOpen,
  ArrowUpDown,
  Sparkles,
  X,
  Layers,
} from 'lucide-react';
import { CourseCard } from '@/components/CourseCard';
import { api } from '@/lib/api';
import { Course, Category } from '@/lib/types';

function CoursesContent() {
  const searchParams = useSearchParams();
  const initialSearch = searchParams.get('search') || '';

  const [courses, setCourses] = useState<Course[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  // Filter & Search states
  const [searchTerm, setSearchTerm] = useState(initialSearch);
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [selectedDifficulty, setSelectedDifficulty] = useState<string>('all');
  const [sortBy, setSortBy] = useState<string>('order');

  useEffect(() => {
    async function loadData() {
      setIsLoading(true);
      try {
        const [coursesData, categoriesData] = await Promise.all([
          api.get<{ results?: Course[] } | Course[]>('/courses/'),
          api.get<Category[]>('/categories/'),
        ]);

        if (Array.isArray(coursesData)) {
          setCourses(coursesData);
        } else if (coursesData.results) {
          setCourses(coursesData.results);
        }

        if (Array.isArray(categoriesData)) {
          setCategories(categoriesData);
        }
      } catch (err) {
        console.error('Failed to load courses', err);
      } finally {
        setIsLoading(false);
      }
    }
    loadData();
  }, []);

  const filteredCourses = useMemo(() => {
    return courses
      .filter((course) => {
        // Search term filter
        if (searchTerm.trim()) {
          const q = searchTerm.toLowerCase();
          const matchTitle = course.title.toLowerCase().includes(q);
          const matchTagline = (course.tagline || '').toLowerCase().includes(q);
          const matchDesc = (course.description || '').toLowerCase().includes(q);
          const matchCat = (course.category_name || '').toLowerCase().includes(q);
          if (!matchTitle && !matchTagline && !matchDesc && !matchCat) return false;
        }

        // Category filter
        if (selectedCategory !== 'all') {
          const catSlug = typeof course.category === 'object' ? course.category.slug : course.category_name?.toLowerCase();
          if (catSlug && !catSlug.includes(selectedCategory.toLowerCase())) {
            return false;
          }
        }

        // Difficulty filter
        if (selectedDifficulty !== 'all' && course.difficulty !== selectedDifficulty) {
          return false;
        }

        return true;
      })
      .sort((a, b) => {
        if (sortBy === 'hours_asc') return a.estimated_hours - b.estimated_hours;
        if (sortBy === 'hours_desc') return b.estimated_hours - a.estimated_hours;
        if (sortBy === 'title') return a.title.localeCompare(b.title);
        return 0; // Default order
      });
  }, [courses, searchTerm, selectedCategory, selectedDifficulty, sortBy]);

  const clearFilters = () => {
    setSearchTerm('');
    setSelectedCategory('all');
    setSelectedDifficulty('all');
    setSortBy('order');
  };

  return (
    <div className="min-h-screen bg-[#07090E] py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto space-y-10">
        {/* Page Header */}
        <div className="space-y-3">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-cyan-500/10 border border-cyan-500/30 text-xs font-mono text-cyan-400">
            <BookOpen className="w-3.5 h-3.5" />
            <span>Comprehensive Technical Curricula</span>
          </div>
          <h1 className="text-3xl sm:text-5xl font-extrabold text-white tracking-tight">
            Curriculum Directory
          </h1>
          <p className="text-slate-400 text-sm max-w-2xl">
            Explore 9 flagship technical tracks. Master memory allocation, pointer arithmetic, modern C++, distributed database indexing, algorithms, and AI architectures.
          </p>
        </div>

        {/* Filter Controls Bar */}
        <div className="p-6 rounded-2xl bg-slate-900/80 border border-slate-800/90 shadow-xl space-y-5">
          <div className="grid grid-cols-1 md:grid-cols-12 gap-4">
            {/* Search Input */}
            <div className="md:col-span-5 relative">
              <Search className="w-4 h-4 text-slate-500 absolute left-3.5 top-3.5" />
              <input
                type="text"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                placeholder="Search curricula, algorithms, SQL, pointers..."
                className="w-full pl-10 pr-4 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-sm text-slate-200 placeholder-slate-500 focus:outline-none focus:border-cyan-500"
              />
              {searchTerm && (
                <button
                  onClick={() => setSearchTerm('')}
                  className="absolute right-3 top-3 text-slate-500 hover:text-white"
                >
                  <X className="w-4 h-4" />
                </button>
              )}
            </div>

            {/* Category Dropdown */}
            <div className="md:col-span-3">
              <select
                value={selectedCategory}
                onChange={(e) => setSelectedCategory(e.target.value)}
                className="w-full px-4 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-sm text-slate-200 focus:outline-none focus:border-cyan-500"
              >
                <option value="all">All Categories</option>
                {categories.map((c) => (
                  <option key={c.id} value={c.slug}>
                    {c.name}
                  </option>
                ))}
              </select>
            </div>

            {/* Difficulty Dropdown */}
            <div className="md:col-span-2">
              <select
                value={selectedDifficulty}
                onChange={(e) => setSelectedDifficulty(e.target.value)}
                className="w-full px-4 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-sm text-slate-200 focus:outline-none focus:border-cyan-500"
              >
                <option value="all">All Levels</option>
                <option value="beginner">Beginner</option>
                <option value="intermediate">Intermediate</option>
                <option value="advanced">Advanced</option>
              </select>
            </div>

            {/* Sort Dropdown */}
            <div className="md:col-span-2">
              <select
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value)}
                className="w-full px-4 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-sm text-slate-200 focus:outline-none focus:border-cyan-500"
              >
                <option value="order">Featured Order</option>
                <option value="hours_asc">Duration (Shortest)</option>
                <option value="hours_desc">Duration (Longest)</option>
                <option value="title">Alphabetical (A-Z)</option>
              </select>
            </div>
          </div>

          {/* Active Filter Chips & Clear Action */}
          {(searchTerm || selectedCategory !== 'all' || selectedDifficulty !== 'all') && (
            <div className="flex items-center justify-between pt-3 border-t border-slate-800/80 text-xs font-mono">
              <div className="flex items-center gap-2 flex-wrap">
                <span className="text-slate-400">Active Filters:</span>
                {searchTerm && (
                  <span className="px-2.5 py-1 rounded-md bg-cyan-500/10 border border-cyan-500/30 text-cyan-300">
                    Query: "{searchTerm}"
                  </span>
                )}
                {selectedCategory !== 'all' && (
                  <span className="px-2.5 py-1 rounded-md bg-indigo-500/10 border border-indigo-500/30 text-indigo-300">
                    Category: {selectedCategory}
                  </span>
                )}
                {selectedDifficulty !== 'all' && (
                  <span className="px-2.5 py-1 rounded-md bg-amber-500/10 border border-amber-500/30 text-amber-300">
                    Level: {selectedDifficulty}
                  </span>
                )}
              </div>

              <button
                onClick={clearFilters}
                className="text-rose-400 hover:text-rose-300 flex items-center gap-1"
              >
                <X className="w-3.5 h-3.5" />
                <span>Reset Filters</span>
              </button>
            </div>
          )}
        </div>

        {/* Course Grid / States */}
        {isLoading ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {[1, 2, 3, 4, 5, 6].map((i) => (
              <div
                key={i}
                className="h-72 rounded-2xl bg-slate-900/60 border border-slate-800 animate-pulse"
              />
            ))}
          </div>
        ) : filteredCourses.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredCourses.map((course) => (
              <CourseCard key={course.id} course={course} />
            ))}
          </div>
        ) : (
          /* Empty State */
          <div className="p-16 rounded-3xl bg-slate-900/40 border border-slate-800 text-center space-y-4 max-w-md mx-auto">
            <div className="w-12 h-12 rounded-2xl bg-slate-800 flex items-center justify-center text-slate-400 mx-auto">
              <Search className="w-6 h-6" />
            </div>
            <h3 className="text-lg font-bold text-white">No Curricula Found</h3>
            <p className="text-xs text-slate-400">
              No matching tracks match your current filter parameters. Try adjusting your query or resetting filters.
            </p>
            <button
              onClick={clearFilters}
              className="px-4 py-2 rounded-xl text-xs font-mono font-semibold text-cyan-400 bg-cyan-500/10 border border-cyan-500/30 hover:bg-cyan-500/20"
            >
              Reset All Filters
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

export default function CoursesPage() {
  return (
    <Suspense
      fallback={
        <div className="min-h-screen bg-[#07090E] flex items-center justify-center">
          <div className="w-10 h-10 rounded-full border-2 border-cyan-500 border-t-transparent animate-spin" />
        </div>
      }
    >
      <CoursesContent />
    </Suspense>
  );
}
