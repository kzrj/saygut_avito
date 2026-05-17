import { useEffect, useState } from "react";
import { ListingCard } from "../components/listing/ListingCard";
import { useListingStore } from "../store/listingStore";

export function Catalog() {
  const catalog = useListingStore((s) => s.catalog);
  const categories = useListingStore((s) => s.categories);
  const loading = useListingStore((s) => s.loading);
  const loadCatalog = useListingStore((s) => s.loadCatalog);
  const loadCategories = useListingStore((s) => s.loadCategories);
  const [q, setQ] = useState("");
  const [category, setCategory] = useState("");

  useEffect(() => {
    loadCategories();
  }, [loadCategories]);

  useEffect(() => {
    loadCatalog({ q: q || undefined, category: category || undefined });
  }, [loadCatalog, q, category]);

  return (
    <div className="container">
      <h1 style={{ marginBottom: "1.5rem" }}>Каталог</h1>
      <div
        style={{
          display: "flex",
          gap: "1rem",
          marginBottom: "1.5rem",
          flexWrap: "wrap",
        }}
      >
        <input
          className="input"
          placeholder="Поиск…"
          value={q}
          onChange={(e) => setQ(e.target.value)}
          style={{ maxWidth: 280 }}
        />
        <select
          className="input"
          value={category}
          onChange={(e) => setCategory(e.target.value)}
          style={{ maxWidth: 200 }}
        >
          <option value="">Все категории</option>
          {categories.map((c) => (
            <option key={c.id} value={c.id}>
              {c.name}
            </option>
          ))}
        </select>
      </div>
      {loading ? (
        <div className="loading">Загрузка…</div>
      ) : catalog.length === 0 ? (
        <div className="empty">Объявлений пока нет</div>
      ) : (
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fill, minmax(260px, 1fr))",
            gap: "1.25rem",
          }}
        >
          {catalog.map((l) => (
            <ListingCard key={l.id} listing={l} />
          ))}
        </div>
      )}
    </div>
  );
}
