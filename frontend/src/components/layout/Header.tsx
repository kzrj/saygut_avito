import { Link, useNavigate } from "react-router-dom";
import { useAuthStore } from "../../store/authStore";

export function Header() {
  const user = useAuthStore((s) => s.user);
  const logout = useAuthStore((s) => s.logout);
  const navigate = useNavigate();

  return (
    <header
      style={{
        borderBottom: "1px solid var(--border)",
        background: "var(--surface)",
        padding: "0.75rem 0",
      }}
    >
      <div
        className="container"
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          gap: "1rem",
        }}
      >
        <Link to="/" style={{ fontWeight: 700, fontSize: "1.25rem", color: "var(--text)" }}>
          MicroAvito
        </Link>
        <nav style={{ display: "flex", gap: "1.25rem", alignItems: "center" }}>
          <Link to="/catalog">Каталог</Link>
          {user ? (
            <>
              <Link to="/create">Разместить</Link>
              <Link to="/wallet">
                Кошелёк{" "}
                <span className="coins">{user.wallet_balance}</span>
              </Link>
              <span style={{ color: "var(--muted)", fontSize: "0.9rem" }}>
                {user.display_name}
              </span>
              <button
                className="btn btn-secondary"
                onClick={() => {
                  logout();
                  navigate("/login");
                }}
              >
                Выйти
              </button>
            </>
          ) : (
            <>
              <Link to="/login">Вход</Link>
              <Link to="/register" className="btn btn-primary">
                Регистрация
              </Link>
            </>
          )}
        </nav>
      </div>
    </header>
  );
}
