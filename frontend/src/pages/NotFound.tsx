import { Link } from "react-router-dom";
import { buttonVariants } from "@/components/ui/button";
import { cn } from "@/lib/utils";

export function NotFound() {
  return (
    <div className="container mx-auto px-4 py-20 text-center">
      <p className="text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-4">Ошибка</p>
      <h1 className="font-heading text-6xl font-bold text-slate-900 mb-4">404</h1>
      <p className="text-slate-500 mb-8">Страница не найдена</p>
      <Link to="/" className={cn(buttonVariants(), "rounded-xl px-8 h-11 font-semibold")}>
        На главную
      </Link>
    </div>
  );
}
