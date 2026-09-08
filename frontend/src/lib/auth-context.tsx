'use client';

import React, { createContext, useContext, useEffect, useState } from 'react';
import { User } from './types';
import { api } from './api';

interface AuthContextType {
  user: User | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  isAdmin: boolean;
  login: (emailOrUsername: string, password: string) => Promise<User>;
  register: (email: string, username: string, password: string, firstName?: string, lastName?: string) => Promise<User>;
  logout: () => void;
  updateProfile: (data: Partial<User>) => Promise<User>;
  refreshUser: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const fetchCurrentUser = async () => {
    try {
      const token = localStorage.getItem('techspire_access_token');
      if (!token) {
        setIsLoading(false);
        return;
      }
      const userData = await api.get<User>('/auth/me/');
      setUser(userData);
      localStorage.setItem('techspire_user', JSON.stringify(userData));
    } catch {
      setUser(null);
      api.clearTokens();
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    const cached = localStorage.getItem('techspire_user');
    if (cached) {
      try {
        setUser(JSON.parse(cached));
      } catch {
        // Ignore JSON error
      }
    }
    fetchCurrentUser();
  }, []);

  const login = async (emailOrUsername: string, password: string): Promise<User> => {
    setIsLoading(true);
    try {
      const response = await api.post<{
        user: User;
        tokens: { access: string; refresh: string };
      }>('/auth/login/', {
        email: emailOrUsername,
        password,
      });

      localStorage.setItem('techspire_access_token', response.tokens.access);
      localStorage.setItem('techspire_refresh_token', response.tokens.refresh);
      localStorage.setItem('techspire_user', JSON.stringify(response.user));
      setUser(response.user);
      return response.user;
    } finally {
      setIsLoading(false);
    }
  };

  const register = async (
    email: string,
    username: string,
    password: string,
    firstName?: string,
    lastName?: string
  ): Promise<User> => {
    setIsLoading(true);
    try {
      const response = await api.post<{
        user: User;
        tokens: { access: string; refresh: string };
      }>('/auth/register/', {
        email,
        username,
        password,
        password_confirm: password,
        first_name: firstName || '',
        last_name: lastName || '',
      });

      localStorage.setItem('techspire_access_token', response.tokens.access);
      localStorage.setItem('techspire_refresh_token', response.tokens.refresh);
      localStorage.setItem('techspire_user', JSON.stringify(response.user));
      setUser(response.user);
      return response.user;
    } finally {
      setIsLoading(false);
    }
  };

  const logout = () => {
    api.clearTokens();
    setUser(null);
    window.location.href = '/login';
  };

  const updateProfile = async (data: Partial<User>): Promise<User> => {
    const updated = await api.patch<User>('/auth/me/', data);
    setUser(updated);
    localStorage.setItem('techspire_user', JSON.stringify(updated));
    return updated;
  };

  const refreshUser = async () => {
    await fetchCurrentUser();
  };

  const isAdmin = Boolean(user && (user.role === 'admin' || user.is_staff || user.is_superuser));
  const isAuthenticated = Boolean(user);

  return (
    <AuthContext.Provider
      value={{
        user,
        isLoading,
        isAuthenticated,
        isAdmin,
        login,
        register,
        logout,
        updateProfile,
        refreshUser,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
