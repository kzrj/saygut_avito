import { FormEvent, useState } from "react";
import { Link, useNavigate, useSearchParams } from "react-router-dom";
import { useAuthStore } from "../store/authStore";

export function Register() {
  const [searchParams] = useSearchParams();
  const [email, setEmail] = useState("");
  const [displayName, setDisplayName] = useState("");
  const [password, setPassword] = useState("");
  const [referralCode, setReferralCode] = useState(searchParams.get("ref") || "");
  const register = useAuthStore((s) => s.register);
  const loading = useAuthStore((s) => s.loading);
  const error = useAuthStore((s) => s.error);
  const navigate = useNavigate();

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    try {
      await register({
        email,
        password,
        display_name: displayName,
        referral_code: referralCode || undefined,
      });
      navigate("/wallet");
    } catch {
      /* error in store */
    }
  };

  return (
    <div className="container" style={{ maxWidth: 400 }}>
      <h1 style={{ marginBottom: "1.5rem" }}>Регистрация</h1>
      <form onSubmit={handleSubmit} className="card">
        <div className="form-group">
          <label className="label">Email</label>
          <input
            className="input"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
        <div className="form-group">
          <label className="label">Имя</label>
          <input
            className="input"
            value={displayName}
            onChange={(e) => setDisplayName(e.target.value)}
          />
        </div>
        <div className="form-group">
          <label className="label">Пароль</label>
          <input
            className="input"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            minLength={6}
          />
        </div>
        <div className="form-group">
          <label className="label">Реферальный код (необязательно)</label>
          <input
            className="input"
            value={referralCode}
            onChange={(e) => setReferralCode(e.target.value.toUpperCase())}
          />
        </div>
        {error && <p className="error-msg">{error}</p>}
        <button type="submit" className="btn btn-primary" style={{ width: "100%" }} disabled={loading}>
          {loading ? "Создание…" : "Зарегистрироваться"}
        </button>
        <p style={{ marginTop: "1rem", textAlign: "center", color: "var(--muted)" }}>
          Уже есть аккаунт? <Link to="/login">Вход</Link>
        </p>
      </form>
    </div>
  );
}
