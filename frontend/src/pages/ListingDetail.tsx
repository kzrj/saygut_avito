import { useEffect } from "react";
import { Link, useParams } from "react-router-dom";
import { useListingStore } from "../store/listingStore";

export function ListingDetail() {
  const { id } = useParams<{ id: string }>();
  const listing = useListingStore((s) => s.current);
  const loading = useListingStore((s) => s.loading);
  const error = useListingStore((s) => s.error);
  const loadListing = useListingStore((s) => s.loadListing);

  useEffect(() => {
    if (id) loadListing(id);
  }, [id, loadListing]);

  if (loading) return <div className="loading container">Загрузка…</div>;
  if (error || !listing) {
    return (
      <div className="container">
        <p className="error-msg">{error || "Объявление не найдено"}</p>
        <Link to="/catalog">← Каталог</Link>
      </div>
    );
  }

  return (
    <div className="container" style={{ maxWidth: 720 }}>
      <Link to="/catalog" style={{ display: "inline-block", marginBottom: "1rem" }}>
        ← Каталог
      </Link>
      <article className="card">
        {listing.images[0] && (
          <img
            src={listing.images[0]}
            alt=""
            style={{ width: "100%", maxHeight: 400, objectFit: "cover", borderRadius: 8 }}
          />
        )}
        <h1 style={{ margin: "1rem 0 0.5rem" }}>{listing.title}</h1>
        <p className="coins" style={{ fontSize: "1.25rem", marginBottom: "1rem" }}>
          {listing.price_coins} монет
        </p>
        <p style={{ whiteSpace: "pre-wrap", color: "var(--muted)" }}>
          {listing.description || "Без описания"}
        </p>
      </article>
    </div>
  );
}
