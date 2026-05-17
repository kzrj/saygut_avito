import { FormEvent, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { FormField } from "@/components/ui/auth-form";
import { useAuthStore } from "@/store/authStore";
import { useListingStore } from "@/store/listingStore";
import { useWalletStore } from "@/store/walletStore";

const inputClass = "h-11 rounded-xl bg-slate-50 border-slate-200";

export function CreateListing() {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [priceRub, setPriceRub] = useState(100);
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
        price_coins: priceRub,
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
    <div className="container mx-auto px-4 py-8 max-w-xl">
      <h1 className="font-heading text-3xl font-bold text-slate-900 mb-2">Новое объявление</h1>
      <p className="text-slate-500 mb-6">При публикации спишется комиссия платформы (10 монет).</p>

      <form
        onSubmit={handleSubmit}
        className="bg-white rounded-2xl border border-slate-100 shadow-sm p-6 md:p-8"
      >
        <FormField label="Заголовок">
          <Input
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            required
            className={inputClass}
          />
        </FormField>

        <FormField label="Описание">
          <textarea
            className={`w-full min-h-[120px] px-3 py-2 rounded-xl border border-slate-200 bg-slate-50 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary/50 ${inputClass}`}
            rows={4}
            value={description}
            onChange={(e) => setDescription(e.target.value)}
          />
        </FormField>

        <FormField label="Цена, ₽">
          <Input
            type="number"
            min={1}
            value={priceRub}
            onChange={(e) => setPriceRub(Number(e.target.value))}
            required
            className={inputClass}
          />
        </FormField>

        <FormField label="Категория">
          <select
            className={`w-full px-3 ${inputClass}`}
            value={categoryId}
            onChange={(e) => setCategoryId(e.target.value)}
          >
            <option value="">Без категории</option>
            {categories.map((c) => (
              <option key={c.id} value={c.id}>
                {c.name}
              </option>
            ))}
          </select>
        </FormField>

        <FormField label="Фото">
          <input
            type="file"
            accept="image/*"
            multiple
            onChange={(e) => setFiles(Array.from(e.target.files || []))}
            className="text-sm text-slate-600 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:bg-primary/10 file:text-primary file:font-semibold"
          />
        </FormField>

        {error && <p className="text-destructive text-sm mb-4">{error}</p>}

        <Button type="submit" className="w-full h-11 rounded-xl font-semibold" disabled={loading}>
          {loading ? "Публикация…" : "Опубликовать"}
        </Button>
      </form>
    </div>
  );
}
