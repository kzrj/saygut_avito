import { useEffect, useMemo } from "react";
import { useSearchParams } from "react-router-dom";
import { LayoutGrid as LayoutGridIcon } from "lucide-react";
import { ListingCard } from "@/components/listing/ListingCard";
import { Button } from "@/components/ui/button";
import { useListingStore } from "@/store/listingStore";

export function Catalog() {
  const [searchParams, setSearchParams] = useSearchParams();
  const q = searchParams.get("q") || "";
  const category = searchParams.get("category") || "";

  const catalog = useListingStore((s) => s.catalog);
  const catalogTotal = useListingStore((s) => s.catalogTotal);
  const categories = useListingStore((s) => s.categories);
  const loading = useListingStore((s) => s.loading);
  const loadCatalog = useListingStore((s) => s.loadCatalog);
  const loadCategories = useListingStore((s) => s.loadCategories);

  const sidebarCategories = useMemo(
    () => [{ id: "", name: "Все" }, ...categories.map((c) => ({ id: c.id, name: c.name }))],
    [categories]
  );

  useEffect(() => {
    loadCategories();
  }, [loadCategories]);

  useEffect(() => {
    loadCatalog({ q: q || undefined, category: category || undefined });
  }, [loadCatalog, q, category]);

  const setCategory = (id: string) => {
    const next = new URLSearchParams(searchParams);
    if (id) next.set("category", id);
    else next.delete("category");
    setSearchParams(next);
  };

  const count = catalogTotal || catalog.length;

  return (
    <div className="flex flex-1 container mx-auto px-4 py-8 gap-8 overflow-hidden">
      <aside className="w-64 hidden lg:flex flex-col space-y-8 sticky top-24 h-fit">
        <div>
          <h3 className="text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-4">
            Категории
          </h3>
          <ul className="space-y-3">
            {sidebarCategories.map((cat) => {
              const active = category === cat.id;
              return (
                <li
                  key={cat.id || "all"}
                  onClick={() => setCategory(cat.id)}
                  className={`flex items-center cursor-pointer transition-all ${
                    active
                      ? "text-primary font-bold"
                      : "text-slate-600 hover:text-primary font-medium"
                  }`}
                >
                  {active && <span className="w-2 h-2 bg-primary rounded-full mr-3" />}
                  {cat.name}
                </li>
              );
            })}
          </ul>
        </div>
      </aside>

      <main className="flex-1 min-w-0">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-8">
          <h2 className="text-2xl font-bold text-slate-900 tracking-tight">
            Свежие предложения
            <span className="text-slate-400 font-normal ml-2 sm:ml-3 text-lg block sm:inline">
              {loading ? "…" : `${count} объявлений`} в Улан-Удэ
            </span>
          </h2>
          <div className="flex items-center space-x-2 text-xs font-bold uppercase tracking-wider text-slate-400">
            <span>Сортировка:</span>
            <span className="text-slate-900 border-b-2 border-primary">По новизне</span>
          </div>
        </div>

        {loading ? (
          <div className="py-20 text-center text-slate-400 font-medium">Загрузка…</div>
        ) : catalog.length > 0 ? (
          <div className="grid grid-cols-2 md:grid-cols-2 xl:grid-cols-3 gap-4 sm:gap-6">
            {catalog.map((listing) => (
              <ListingCard key={listing.id} listing={listing} />
            ))}
          </div>
        ) : (
          <div className="py-20 text-center flex flex-col items-center gap-4 bg-white rounded-3xl border border-dashed border-slate-200">
            <div className="p-4 bg-slate-50 rounded-full">
              <LayoutGridIcon className="h-12 w-12 text-slate-300" />
            </div>
            <p className="text-xl font-bold text-slate-400">
              {q || category ? "Ничего не найдено" : "Объявлений пока нет"}
            </p>
            {(q || category) && (
              <Button
                variant="outline"
                onClick={() => setSearchParams({})}
                className="rounded-xl"
              >
                Сбросить фильтры
              </Button>
            )}
          </div>
        )}
      </main>
    </div>
  );
}
