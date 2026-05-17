import { apiRequest } from "./client";
import type { ReferralStats } from "../types";

export function fetchReferralMe() {
  return apiRequest<ReferralStats>("/referrals/me");
}

export function fetchReferralLink() {
  return apiRequest<{ url: string }>("/referrals/link");
}
