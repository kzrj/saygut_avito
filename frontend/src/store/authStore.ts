import { create } from "zustand";
import * as authApi from "../api/auth";
import { clearTokens, setTokens } from "../api/client";
import type { UserProfile } from "../types";

interface AuthState {
  user: UserProfile | null;
  loading: boolean;
  error: string | null;
  initialized: boolean;
  init: () => Promise<void>;
  register: (data: {
    email?: string;
    phone?: string;
    password: string;
    display_name?: string;
    referral_code?: string;
  }) => Promise<void>;
  login: (data: {
    email?: string;
    phone?: string;
    password: string;
  }) => Promise<void>;
  logout: () => void;
  refreshUser: () => Promise<void>;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  loading: false,
  error: null,
  initialized: false,

  init: async () => {
    const token = localStorage.getItem("access_token");
    if (!token) {
      set({ initialized: true });
      return;
    }
    try {
      const user = await authApi.fetchMe();
      set({ user, initialized: true });
    } catch {
      clearTokens();
      set({ user: null, initialized: true });
    }
  },

  register: async (data) => {
    set({ loading: true, error: null });
    try {
      const res = await authApi.register(data);
      setTokens(res.access_token, res.refresh_token);
      set({ user: res.user, loading: false });
    } catch (e) {
      set({
        loading: false,
        error: e instanceof Error ? e.message : "Registration failed",
      });
      throw e;
    }
  },

  login: async (data) => {
    set({ loading: true, error: null });
    try {
      const res = await authApi.login(data);
      setTokens(res.access_token, res.refresh_token);
      set({ user: res.user, loading: false });
    } catch (e) {
      set({
        loading: false,
        error: e instanceof Error ? e.message : "Login failed",
      });
      throw e;
    }
  },

  logout: () => {
    clearTokens();
    set({ user: null });
  },

  refreshUser: async () => {
    const user = await authApi.fetchMe();
    set({ user });
  },
}));
