import { useEffect } from "react";
import { Link, useParams } from "react-router-dom";
import { ArrowLeft, Coins, Clock } from "lucide-react";
import { buttonVariants } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import { useListingStore } from "@/store/listingStore";
import { formatRelativeTime } from "@/utils/format";

export function ListingDetail() {
  const { id } = useParams<{ id: string }>();
  const listing = useListingStore((s) => s.current);
  const loading = useListingStore((s) => s.loading);
  const error = useListingStore((s) => s.error);
  const loadListing = useListingStore((s) => s.loadListing);

  useEffect(() => {
    if (id) loadListing(id);
  }, [id, loadListing]);

  if (loading) {
    return (
      <div className="container mx-auto px-4 py-20 text-center text-slate-400 font-medium">
        Загрузка…
      </div>
    );
  }

  if (error || !listing) {
    return (
      <div className="container mx-auto px-4 py-12 max-w-lg text-center">
        <p className="text-destructive mb-4">{error || "Объявление не найдено"}</p>
        <Link
          to="/catalog"
          className={cn(buttonVariants({ variant: "outline" }), "rounded-xl")}
        >
          ← Каталог
        </Link>
      </div>
    );
  }

  const time = formatRelativeTime(listing.published_at || listing.created_at);

  return (
    <div className="container mx-auto px-4 py-8 max-w-3xl">
      <Link
        to="/catalog"
        className="inline-flex items-center gap-2 text-sm font-semibold text-slate-500 hover:text-primary mb-6 transition-colors"
      >
        <ArrowLeft className="h-4 w-4" />
        Каталог
      </Link>

      <article className="bg-white rounded-2xl border border-slate-100 shadow-sm overflow-hidden">
        {listing.images[0] ? (
          <img
            src={listing.images[0]}
            alt={listing.title}
            className="w-full max-h-[420px] object-cover bg-slate-50"
          />
        ) : (
          <div className="w-full h-64 bg-slate-100 flex items-center justify-center text-slate-400">
            Нет фото
          </div>
        )}
        <div className="p-6 md:p-8">
          <h1 className="font-heading text-2xl md:text-3xl font-bold text-slate-900 mb-3">
            {listing.title}
          </h1>
          <div className="flex flex-wrap items-center gap-4 mb-6">
            <span className="inline-flex items-center gap-2 text-2xl font-bold text-amber-600">
              <Coins className="h-7 w-7" />
              {listing.price_coins.toLocaleString("ru-RU")} монет
            </span>
            <span className="flex items-center gap-1 text-xs font-bold uppercase tracking-wider text-slate-400">
              <Clock className="h-3.5 w-3.5" />
              {time}
            </span>
          </div>
          <p className="text-slate-600 whitespace-pre-wrap leading-relaxed">
            {listing.description || "Без описания"}
          </p>
        </div>
      </article>
    </div>
  );
}
