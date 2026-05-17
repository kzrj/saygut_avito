import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { Coins, Copy } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { FormField } from "@/components/ui/auth-form";
import { useAuthStore } from "@/store/authStore";
import { useWalletStore } from "@/store/walletStore";

const TX_LABELS: Record<string, string> = {
  topup: "Пополнение",
  listing_fee: "Размещение",
  referral_bonus: "Реферальный бонус",
  admin_adjustment: "Начисление",
};

const inputClass = "h-11 rounded-xl bg-slate-50 border-slate-200";

export function Wallet() {
  const [searchParams] = useSearchParams();
  const balance = useWalletStore((s) => s.balance);
  const transactions = useWalletStore((s) => s.transactions);
  const referral = useWalletStore((s) => s.referral);
  const loading = useWalletStore((s) => s.loading);
  const loadWallet = useWalletStore((s) => s.loadWallet);
  const loadTransactions = useWalletStore((s) => s.loadTransactions);
  const loadReferral = useWalletStore((s) => s.loadReferral);
  const adminCredit = useWalletStore((s) => s.adminCredit);
  const topup = useWalletStore((s) => s.topup);
  const [topupCoins, setTopupCoins] = useState(100);
  const [devCredit, setDevCredit] = useState(100);

  useEffect(() => {
    loadWallet();
    loadTransactions();
    loadReferral();
  }, [loadWallet, loadTransactions, loadReferral]);

  useEffect(() => {
    const paymentId = searchParams.get("payment_id");
    if (paymentId) {
      const interval = setInterval(async () => {
        const done = await useWalletStore.getState().pollPayment(paymentId);
        if (done) clearInterval(interval);
      }, 2000);
      return () => clearInterval(interval);
    }
  }, [searchParams]);

  const refLink = referral ? `${window.location.origin}/register?ref=${referral.code}` : "";

  return (
    <div className="container mx-auto px-4 py-8 max-w-2xl">
      <h1 className="font-heading text-3xl font-bold text-slate-900 mb-8">Кошелёк</h1>

      <div className="bg-white rounded-2xl border border-slate-100 shadow-sm p-6 mb-6">
        <p className="text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-2">Баланс</p>
        <p className="flex items-center gap-2 text-3xl font-bold text-amber-600">
          <Coins className="h-8 w-8" />
          {loading ? "…" : balance.toLocaleString("ru-RU")} монет
        </p>
      </div>

      <div className="bg-white rounded-2xl border border-slate-100 shadow-sm p-6 mb-6">
        <h2 className="font-heading font-semibold text-slate-900 mb-4">Пополнить</h2>
        <div className="flex flex-wrap gap-3 items-end">
          <FormField label="Монет" className="flex-1 min-w-[120px] mb-0">
            <Input
              type="number"
              min={1}
              value={topupCoins}
              onChange={(e) => setTopupCoins(Number(e.target.value))}
              className={inputClass}
            />
          </FormField>
          <Button
            type="button"
            onClick={() => topup(topupCoins)}
            className="h-11 rounded-xl font-semibold shrink-0"
          >
            Пополнить через ЮMoney
          </Button>
        </div>
        <p className="text-xs text-slate-400 mt-3">
          В dev-режиме откроется mock-страница подтверждения платежа.
        </p>
      </div>

      {referral && (
        <div className="bg-white rounded-2xl border border-slate-100 shadow-sm p-6 mb-6">
          <h2 className="font-heading font-semibold text-slate-900 mb-3">Реферальная программа</h2>
          <p className="text-slate-700">
            Ваш код: <strong className="text-primary">{referral.code}</strong>
          </p>
          <p className="text-sm text-slate-500 mt-2">
            Приглашено: {referral.invited_count} · Заработано:{" "}
            <span className="font-semibold text-amber-600">{referral.earned_coins}</span> монет
          </p>
          <p className="mt-3 text-xs text-slate-500 break-all flex items-start gap-2">
            <span className="flex-1">{refLink}</span>
            <button
              type="button"
              onClick={() => navigator.clipboard.writeText(refLink)}
              className="shrink-0 p-1.5 rounded-lg hover:bg-slate-100 text-slate-500"
              title="Копировать"
            >
              <Copy className="h-4 w-4" />
            </button>
          </p>
        </div>
      )}

      <div className="bg-white rounded-2xl border border-slate-100 shadow-sm p-6 mb-8">
        <h2 className="font-heading font-semibold text-slate-900 mb-4">Dev: начислить монеты</h2>
        <div className="flex gap-3">
          <Input
            type="number"
            value={devCredit}
            onChange={(e) => setDevCredit(Number(e.target.value))}
            className={`max-w-[120px] ${inputClass}`}
          />
          <Button
            type="button"
            variant="outline"
            className="h-11 rounded-xl"
            onClick={() => adminCredit(devCredit).then(() => useAuthStore.getState().refreshUser())}
          >
            Начислить
          </Button>
        </div>
      </div>

      <h2 className="font-heading font-semibold text-slate-900 mb-4">История</h2>
      {transactions.length === 0 ? (
        <div className="py-12 text-center text-slate-400 bg-white rounded-2xl border border-dashed border-slate-200">
          Транзакций пока нет
        </div>
      ) : (
        <div className="flex flex-col gap-2">
          {transactions.map((tx) => (
            <div
              key={tx.id}
              className="bg-white rounded-xl border border-slate-100 px-4 py-3 flex justify-between items-center text-sm"
            >
              <span className="font-medium text-slate-700">{TX_LABELS[tx.type] || tx.type}</span>
              <span
                className={
                  tx.amount >= 0 ? "font-bold text-amber-600" : "font-bold text-destructive"
                }
              >
                {tx.amount >= 0 ? "+" : ""}
                {tx.amount}
              </span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
