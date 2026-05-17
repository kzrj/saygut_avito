import { FormEvent, useEffect, useState } from "react";
import { Link, useNavigate, useSearchParams } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { AuthShell, FormField, TabSwitch } from "@/components/ui/auth-form";
import { useAuthStore } from "@/store/authStore";

type LoginMode = "email" | "phone";

export function Register() {
  const [searchParams] = useSearchParams();
  const [mode, setMode] = useState<LoginMode>("email");
  const [email, setEmail] = useState("");
  const [phone, setPhone] = useState("");
  const [displayName, setDisplayName] = useState("");
  const [password, setPassword] = useState("");
  const [passwordConfirm, setPasswordConfirm] = useState("");
  const [referralCode, setReferralCode] = useState(searchParams.get("ref") || "");
  const [localError, setLocalError] = useState<string | null>(null);

  const register = useAuthStore((s) => s.register);
  const loading = useAuthStore((s) => s.loading);
  const error = useAuthStore((s) => s.error);
  const navigate = useNavigate();

  useEffect(() => {
    const ref = searchParams.get("ref");
    if (ref) setReferralCode(ref.toUpperCase());
  }, [searchParams]);

  const switchMode = (next: LoginMode) => {
    setMode(next);
    setLocalError(null);
    useAuthStore.setState({ error: null });
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setLocalError(null);
    useAuthStore.setState({ error: null });

    if (password !== passwordConfirm) {
      setLocalError("Пароли не совпадают");
      return;
    }
    if (password.length < 6) {
      setLocalError("Пароль должен быть не короче 6 символов");
      return;
    }
    if (mode === "email" && !email.trim()) {
      setLocalError("Укажите email");
      return;
    }
    if (mode === "phone" && phone.replace(/\D/g, "").length < 10) {
      setLocalError("Укажите корректный номер телефона");
      return;
    }

    try {
      await register({
        email: mode === "email" ? email.trim() : undefined,
        phone: mode === "phone" ? phone.trim() : undefined,
        password,
        password_confirm: passwordConfirm,
        display_name: displayName.trim() || undefined,
        referral_code: referralCode.trim() || undefined,
      });
      navigate("/wallet", { replace: true });
    } catch {
      /* error in store */
    }
  };

  const displayError = localError || error;
  const inputClass = "h-11 rounded-xl bg-slate-50 border-slate-200";

  return (
    <AuthShell
      title="Регистрация"
      subtitle="Создайте аккаунт для размещения объявлений и работы с кошельком монет."
    >
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
          <FormField label="Email" htmlFor="reg-email">
            <Input
              id="reg-email"
              type="email"
              autoComplete="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="you@example.com"
              required
              className={inputClass}
            />
          </FormField>
        ) : (
          <FormField label="Телефон" htmlFor="reg-phone">
            <Input
              id="reg-phone"
              type="tel"
              autoComplete="tel"
              value={phone}
              onChange={(e) => setPhone(e.target.value)}
              placeholder="+7 900 123-45-67"
              required
              className={inputClass}
            />
          </FormField>
        )}

        <FormField label="Имя (необязательно)" htmlFor="reg-name">
          <Input
            id="reg-name"
            autoComplete="name"
            value={displayName}
            onChange={(e) => setDisplayName(e.target.value)}
            placeholder="Как к вам обращаться"
            className={inputClass}
          />
        </FormField>

        <FormField label="Пароль" htmlFor="reg-password">
          <Input
            id="reg-password"
            type="password"
            autoComplete="new-password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            minLength={6}
            className={inputClass}
          />
        </FormField>

        <FormField label="Повторите пароль" htmlFor="reg-password-confirm">
          <Input
            id="reg-password-confirm"
            type="password"
            autoComplete="new-password"
            value={passwordConfirm}
            onChange={(e) => setPasswordConfirm(e.target.value)}
            required
            minLength={6}
            className={inputClass}
          />
        </FormField>

        <FormField label="Реферальный код (необязательно)" htmlFor="reg-ref">
          <Input
            id="reg-ref"
            value={referralCode}
            onChange={(e) => setReferralCode(e.target.value.toUpperCase())}
            placeholder="AB12CD34"
            className={inputClass}
          />
        </FormField>

        {displayError && <p className="text-destructive text-sm mb-4">{displayError}</p>}

        <Button
          type="submit"
          className="w-full h-11 rounded-xl font-semibold"
          disabled={loading}
        >
          {loading ? "Создание аккаунта…" : "Зарегистрироваться"}
        </Button>

        <p className="mt-6 text-center text-sm text-slate-500">
          Уже есть аккаунт?{" "}
          <Link to="/login" className="text-primary font-semibold hover:underline">
            Вход
          </Link>
        </p>
      </form>
    </AuthShell>
  );
}
