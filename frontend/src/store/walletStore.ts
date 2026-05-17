import { create } from "zustand";
import * as walletApi from "../api/wallet";
import * as paymentsApi from "../api/payments";
import * as referralsApi from "../api/referrals";
import type { ReferralStats, Transaction } from "../types";

interface WalletState {
  balance: number;
  transactions: Transaction[];
  total: number;
  referral: ReferralStats | null;
  loading: boolean;
  error: string | null;
  loadWallet: () => Promise<void>;
  loadTransactions: (page?: number) => Promise<void>;
  loadReferral: () => Promise<void>;
  adminCredit: (amount: number) => Promise<void>;
  topup: (coins: number) => Promise<string>;
  pollPayment: (paymentId: string) => Promise<boolean>;
}

export const useWalletStore = create<WalletState>((set, get) => ({
  balance: 0,
  transactions: [],
  total: 0,
  referral: null,
  loading: false,
  error: null,

  loadWallet: async () => {
    set({ loading: true, error: null });
    try {
      const { balance } = await walletApi.fetchBalance();
      set({ balance, loading: false });
    } catch (e) {
      set({
        loading: false,
        error: e instanceof Error ? e.message : "Failed to load wallet",
      });
    }
  },

  loadTransactions: async (page = 1) => {
    try {
      const res = await walletApi.fetchTransactions(page);
      set({ transactions: res.items, total: res.total });
    } catch (e) {
      set({ error: e instanceof Error ? e.message : "Failed to load transactions" });
    }
  },

  loadReferral: async () => {
    try {
      const referral = await referralsApi.fetchReferralMe();
      set({ referral });
    } catch {
      /* optional */
    }
  },

  adminCredit: async (amount) => {
    const { balance } = await walletApi.adminCredit(amount);
    set({ balance });
    await get().loadTransactions();
  },

  topup: async (coins) => {
    const res = await paymentsApi.initiateTopup({ coins_amount: coins });
    window.location.href = res.confirmation_url;
    return res.payment_id;
  },

  pollPayment: async (paymentId) => {
    const status = await paymentsApi.fetchPaymentStatus(paymentId);
    if (status.status === "succeeded") {
      await get().loadWallet();
      await get().loadTransactions();
      return true;
    }
    return false;
  },
}));
