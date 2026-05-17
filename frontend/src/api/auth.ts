import { apiRequest } from "./client";
import type { AuthResponse, UserProfile } from "../types";

export function register(data: {
  email?: string;
  phone?: string;
  password: string;
  password_confirm?: string;
  display_name?: string;
  referral_code?: string;
}) {
  return apiRequest<AuthResponse>("/auth/register", {
    method: "POST",
    body: JSON.stringify(data),
  });
}

export function login(data: {
  email?: string;
  phone?: string;
  password: string;
}) {
  return apiRequest<AuthResponse>("/auth/login", {
    method: "POST",
    body: JSON.stringify(data),
  });
}

export function fetchMe() {
  return apiRequest<UserProfile>("/auth/me");
}

export function logout() {
  return apiRequest<void>("/auth/logout", { method: "POST" });
}
