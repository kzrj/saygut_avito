import { Link } from "react-router-dom";
import { Clock } from "lucide-react";
import { Card, CardContent, CardFooter } from "@/components/ui/card";
import type { Listing } from "@/types";
import { formatPriceRub, formatRelativeTime } from "@/utils/format";

interface Props {
  listing: Listing;
}

export function ListingCard({ listing }: Props) {
  const image = listing.images[0];
  const time = formatRelativeTime(listing.published_at || listing.created_at);

  return (
    <Link to={`/listing/${listing.id}`} className="block h-full">
      <Card className="overflow-hidden bg-white rounded-2xl shadow-sm border border-slate-100/50 group cursor-pointer hover:shadow-md hover:-translate-y-1 transition-all duration-300 h-full flex flex-col p-0 ring-0">
        <CardContent className="p-0 relative aspect-square bg-slate-50 overflow-hidden">
          {image ? (
            <img
              src={image}
              alt={listing.title}
              className="object-cover w-full h-full transition-transform duration-700 group-hover:scale-110"
            />
          ) : (
            <div className="w-full h-full flex items-center justify-center text-slate-300 text-sm font-medium">
              Нет фото
            </div>
          )}
        </CardContent>
        <CardFooter className="p-5 flex flex-col items-start gap-1 flex-1 border-0 bg-transparent">
          <div className="text-xl font-bold text-slate-900 leading-none mb-1">
            {formatPriceRub(listing.price_coins)}
          </div>
          <h3 className="text-sm text-slate-600 font-medium line-clamp-2 w-full group-hover:text-primary transition-colors">
            {listing.title}
          </h3>
          <div className="mt-4 pt-3 border-t border-slate-50 flex items-center gap-2 w-full text-[10px] text-slate-400 font-bold uppercase tracking-wider">
            <span className="truncate flex-1">Улан-Удэ</span>
            <span className="flex items-center gap-1 shrink-0">
              <Clock className="h-3 w-3" />
              {time}
            </span>
          </div>
        </CardFooter>
      </Card>
    </Link>
  );
}
