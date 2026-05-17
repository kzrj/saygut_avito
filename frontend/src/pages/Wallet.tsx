import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { useAuthStore } from "../store/authStore";
import { useWalletStore } from "../store/walletStore";

const TX_LABELS: Record<string, string> = {
  topup: "Пополнение",
  listing_fee: "Размещение",
  referral_bonus: "Реферальный бонус",
  admin_adjustment: "Начисление",
};

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

  return (
    <div className="container" style={{ maxWidth: 720 }}>
      <h1 style={{ marginBottom: "1.5rem" }}>Кошелёк</h1>

      <div className="card" style={{ marginBottom: "1.5rem" }}>
        <p style={{ color: "var(--muted)", marginBottom: "0.25rem" }}>Баланс</p>
        <p className="coins" style={{ fontSize: "2rem" }}>
          {loading ? "…" : balance} монет
        </p>
      </div>

      <div className="card" style={{ marginBottom: "1.5rem" }}>
        <h2 style={{ marginBottom: "1rem", fontSize: "1.1rem" }}>Пополнить</h2>
        <div style={{ display: "flex", gap: "0.75rem", flexWrap: "wrap", alignItems: "flex-end" }}>
          <div className="form-group" style={{ margin: 0, flex: 1, minWidth: 120 }}>
            <label className="label">Монет</label>
            <input
              className="input"
              type="number"
              min={1}
              value={topupCoins}
              onChange={(e) => setTopupCoins(Number(e.target.value))}
            />
          </div>
          <button
            type="button"
            className="btn btn-primary"
            onClick={() => topup(topupCoins)}
          >
            Пополнить через ЮMoney
          </button>
        </div>
        <p style={{ fontSize: "0.8rem", color: "var(--muted)", marginTop: "0.5rem" }}>
          В dev-режиме откроется mock-страница подтверждения платежа.
        </p>
      </div>

      {referral && (
        <div className="card" style={{ marginBottom: "1.5rem" }}>
          <h2 style={{ marginBottom: "0.75rem", fontSize: "1.1rem" }}>Реферальная программа</h2>
          <p>
            Ваш код: <strong>{referral.code}</strong>
          </p>
          <p style={{ color: "var(--muted)", fontSize: "0.9rem", marginTop: "0.5rem" }}>
            Приглашено: {referral.invited_count} · Заработано:{" "}
            <span className="coins">{referral.earned_coins}</span> монет
          </p>
          <p style={{ marginTop: "0.5rem", fontSize: "0.85rem" }}>
            Ссылка: {`${window.location.origin}/register?ref=${referral.code}`}
          </p>
        </div>
      )}

      <div className="card" style={{ marginBottom: "1.5rem" }}>
        <h2 style={{ marginBottom: "0.75rem", fontSize: "1.1rem" }}>Dev: начислить монеты</h2>
        <div style={{ display: "flex", gap: "0.75rem" }}>
          <input
            className="input"
            type="number"
            value={devCredit}
            onChange={(e) => setDevCredit(Number(e.target.value))}
            style={{ maxWidth: 120 }}
          />
          <button
            type="button"
            className="btn btn-secondary"
            onClick={() => adminCredit(devCredit).then(() => useAuthStore.getState().refreshUser())}
          >
            Начислить
          </button>
        </div>
      </div>

      <h2 style={{ marginBottom: "1rem" }}>История</h2>
      {transactions.length === 0 ? (
        <div className="empty">Транзакций пока нет</div>
      ) : (
        <div style={{ display: "flex", flexDirection: "column", gap: "0.5rem" }}>
          {transactions.map((tx) => (
            <div
              key={tx.id}
              className="card"
              style={{ display: "flex", justifyContent: "space-between", padding: "0.75rem 1rem" }}
            >
              <span>{TX_LABELS[tx.type] || tx.type}</span>
              <span className={tx.amount >= 0 ? "coins" : ""} style={tx.amount < 0 ? { color: "var(--danger)" } : {}}>
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
