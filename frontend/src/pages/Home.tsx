import { Link } from "react-router-dom";
import { useAuthStore } from "../store/authStore";

export function Home() {
  const user = useAuthStore((s) => s.user);

  return (
    <div className="container">
      <section style={{ textAlign: "center", padding: "3rem 0 4rem" }}>
        <h1 style={{ fontSize: "2.5rem", marginBottom: "1rem" }}>
          Маркетплейс на внутренних монетах
        </h1>
        <p style={{ color: "var(--muted)", maxWidth: 520, margin: "0 auto 2rem" }}>
          Размещайте объявления за монеты, пополняйте кошелёк через ЮMoney и
          приглашайте друзей по реферальной программе.
        </p>
        <div style={{ display: "flex", gap: "1rem", justifyContent: "center", flexWrap: "wrap" }}>
          <Link to="/catalog" className="btn btn-primary">
            Смотреть каталог
          </Link>
          {user ? (
            <Link to="/create" className="btn btn-secondary">
              Разместить объявление
            </Link>
          ) : (
            <Link to="/register" className="btn btn-secondary">
              Начать бесплатно
            </Link>
          )}
        </div>
      </section>
    </div>
  );
}
