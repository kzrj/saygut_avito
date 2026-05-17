import { Link } from "react-router-dom";
import type { Listing } from "../../types";

interface Props {
  listing: Listing;
}

export function ListingCard({ listing }: Props) {
  const image = listing.images[0];
  return (
    <Link to={`/listing/${listing.id}`} className="card" style={{ display: "block" }}>
      {image && (
        <img
          src={image}
          alt=""
          style={{
            width: "100%",
            height: 160,
            objectFit: "cover",
            borderRadius: 8,
            marginBottom: "0.75rem",
          }}
        />
      )}
      <h3 style={{ marginBottom: "0.35rem" }}>{listing.title}</h3>
      <p
        style={{
          color: "var(--muted)",
          fontSize: "0.875rem",
          marginBottom: "0.5rem",
          overflow: "hidden",
          textOverflow: "ellipsis",
          whiteSpace: "nowrap",
        }}
      >
        {listing.description || "—"}
      </p>
      <span className="coins">{listing.price_coins} монет</span>
    </Link>
  );
}
