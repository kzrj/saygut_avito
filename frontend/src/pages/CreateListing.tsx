import { FormEvent, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuthStore } from "../store/authStore";
import { useListingStore } from "../store/listingStore";
import { useWalletStore } from "../store/walletStore";

export function CreateListing() {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [priceCoins, setPriceCoins] = useState(100);
  const [categoryId, setCategoryId] = useState("");
  const [files, setFiles] = useState<File[]>([]);
  const categories = useListingStore((s) => s.categories);
  const loading = useListingStore((s) => s.loading);
  const error = useListingStore((s) => s.error);
  const loadCategories = useListingStore((s) => s.loadCategories);
  const createAndPublish = useListingStore((s) => s.createAndPublish);
  const refreshUser = useAuthStore((s) => s.refreshUser);
  const loadWallet = useWalletStore((s) => s.loadWallet);
  const navigate = useNavigate();

  useEffect(() => {
    loadCategories();
  }, [loadCategories]);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    try {
      const listing = await createAndPublish({
        title,
        description,
        price_coins: priceCoins,
        category_id: categoryId || undefined,
        files: files.length ? files : undefined,
      });
      await refreshUser();
      await loadWallet();
      navigate(`/listing/${listing.id}`);
    } catch {
      /* error in store */
    }
  };

  return (
    <div className="container" style={{ maxWidth: 560 }}>
      <h1 style={{ marginBottom: "1.5rem" }}>Новое объявление</h1>
      <p style={{ color: "var(--muted)", marginBottom: "1rem" }}>
        При публикации спишется комиссия платформы (10 монет).
      </p>
      <form onSubmit={handleSubmit} className="card">
        <div className="form-group">
          <label className="label">Заголовок</label>
          <input className="input" value={title} onChange={(e) => setTitle(e.target.value)} required />
        </div>
        <div className="form-group">
          <label className="label">Описание</label>
          <textarea
            className="input"
            rows={4}
            value={description}
            onChange={(e) => setDescription(e.target.value)}
          />
        </div>
        <div className="form-group">
          <label className="label">Цена (монеты)</label>
          <input
            className="input"
            type="number"
            min={1}
            value={priceCoins}
            onChange={(e) => setPriceCoins(Number(e.target.value))}
            required
          />
        </div>
        <div className="form-group">
          <label className="label">Категория</label>
          <select className="input" value={categoryId} onChange={(e) => setCategoryId(e.target.value)}>
            <option value="">Без категории</option>
            {categories.map((c) => (
              <option key={c.id} value={c.id}>
                {c.name}
              </option>
            ))}
          </select>
        </div>
        <div className="form-group">
          <label className="label">Фото</label>
          <input
            type="file"
            accept="image/*"
            multiple
            onChange={(e) => setFiles(Array.from(e.target.files || []))}
          />
        </div>
        {error && <p className="error-msg">{error}</p>}
        <button type="submit" className="btn btn-primary" disabled={loading}>
          {loading ? "Публикация…" : "Опубликовать"}
        </button>
      </form>
    </div>
  );
}
