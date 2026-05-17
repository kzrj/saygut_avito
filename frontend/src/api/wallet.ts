import { apiRequest } from "./client";
import type { Transaction } from "../types";

export function fetchBalance() {
  return apiRequest<{ balance: number }>("/wallet/balance");
}

export function fetchTransactions(page = 1, limit = 20, type?: string) {
  const params = new URLSearchParams({ page: String(page), limit: String(limit) });
  if (type) params.set("type", type);
  return apiRequest<{
    items: Transaction[];
    page: number;
    limit: number;
    total: number;
  }>(`/wallet/transactions?${params}`);
}

export function adminCredit(amount: number) {
  return apiRequest<{ balance: number }>("/wallet/admin/credit", {
    method: "POST",
    body: JSON.stringify({ amount }),
  });
}
