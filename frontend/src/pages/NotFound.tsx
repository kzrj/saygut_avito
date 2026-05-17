import { Link } from "react-router-dom";

export function NotFound() {
  return (
    <div className="container" style={{ textAlign: "center", padding: "4rem 0" }}>
      <h1>404</h1>
      <p style={{ color: "var(--muted)", margin: "1rem 0" }}>Страница не найдена</p>
      <Link to="/" className="btn btn-primary">
        На главную
      </Link>
    </div>
  );
}
