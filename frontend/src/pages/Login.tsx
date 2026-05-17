import { FormEvent, useState } from "react";
import { Link, useNavigate, useLocation } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { AuthShell, FormField, TabSwitch } from "@/components/ui/auth-form";
import { useAuthStore } from "@/store/authStore";

type LoginMode = "email" | "phone";

export function Login() {
  const [mode, setMode] = useState<LoginMode>("email");
  const [email, setEmail] = useState("");
  const [phone, setPhone] = useState("");
  const [password, setPassword] = useState("");
  const login = useAuthStore((s) => s.login);
  const loading = useAuthStore((s) => s.loading);
  const error = useAuthStore((s) => s.error);
  const navigate = useNavigate();
  const location = useLocation();
  const from = (location.state as { from?: { pathname: string } })?.from?.pathname || "/";

  const switchMode = (next: LoginMode) => {
    setMode(next);
    useAuthStore.setState({ error: null });
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    try {
      await login({
        email: mode === "email" ? email.trim() : undefined,
        phone: mode === "phone" ? phone.trim() : undefined,
        password,
      });
      navigate(from, { replace: true });
    } catch {
      /* error in store */
    }
  };

  return (
    <AuthShell title="Вход">
      <form onSubmit={handleSubmit}>
        <TabSwitch
          value={mode}
          options={[
            { id: "email", label: "Email" },
            { id: "phone", label: "Телефон" },
          ]}
          onChange={switchMode}
        />

        {mode === "email" ? (
          <FormField label="Email" htmlFor="login-email">
            <Input
              id="login-email"
              type="email"
              autoComplete="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className="h-11 rounded-xl bg-slate-50 border-slate-200"
            />
          </FormField>
        ) : (
          <FormField label="Телефон" htmlFor="login-phone">
            <Input
              id="login-phone"
              type="tel"
              autoComplete="tel"
              value={phone}
              onChange={(e) => setPhone(e.target.value)}
              placeholder="+7 900 123-45-67"
              required
              className="h-11 rounded-xl bg-slate-50 border-slate-200"
            />
          </FormField>
        )}

        <FormField label="Пароль" htmlFor="login-password">
          <Input
            id="login-password"
            type="password"
            autoComplete="current-password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            minLength={6}
            className="h-11 rounded-xl bg-slate-50 border-slate-200"
          />
        </FormField>

        {error && <p className="text-destructive text-sm mb-4">{error}</p>}

        <Button
          type="submit"
          className="w-full h-11 rounded-xl font-semibold"
          disabled={loading}
        >
          {loading ? "Вход…" : "Войти"}
        </Button>

        <p className="mt-6 text-center text-sm text-slate-500">
          Нет аккаунта?{" "}
          <Link to="/register" className="text-primary font-semibold hover:underline">
            Регистрация
          </Link>
        </p>
      </form>
    </AuthShell>
  );
}
