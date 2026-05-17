import { Link } from "react-router-dom";
import { Coins, Gift, Search } from "lucide-react";
import { buttonVariants } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import { useAuthStore } from "@/store/authStore";

export function Home() {
  const user = useAuthStore((s) => s.user);

  return (
    <div className="container mx-auto px-4 py-12 md:py-20">
      <section className="text-center max-w-2xl mx-auto">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-primary/10 text-primary text-xs font-bold uppercase tracking-widest mb-6">
          Улан-Удэ · Маркетплейс
        </div>
        <h1 className="font-heading text-4xl md:text-5xl font-bold text-slate-900 tracking-tight mb-6">
          Покупайте и продавайте за{" "}
          <span className="text-primary">внутренние монеты</span>
        </h1>
        <p className="text-slate-500 text-lg mb-10 leading-relaxed">
          Размещайте объявления, пополняйте кошелёк через ЮMoney и приглашайте друзей по
          реферальной программе.
        </p>
        <div className="flex flex-wrap gap-3 justify-center">
          <Link
            to="/catalog"
            className={cn(
              buttonVariants({ size: "lg" }),
              "rounded-xl px-8 h-12 font-semibold shadow-sm gap-2"
            )}
          >
            <Search className="h-4 w-4" />
            Смотреть каталог
          </Link>
          {user ? (
            <Link
              to="/create"
              className={cn(
                buttonVariants({ variant: "outline", size: "lg" }),
                "rounded-xl px-8 h-12 font-semibold"
              )}
            >
              Разместить объявление
            </Link>
          ) : (
            <Link
              to="/register"
              className={cn(
                buttonVariants({ variant: "outline", size: "lg" }),
                "rounded-xl px-8 h-12 font-semibold"
              )}
            >
              Начать бесплатно
            </Link>
          )}
        </div>
      </section>

      <section className="grid md:grid-cols-3 gap-6 mt-16 md:mt-24">
        {[
          {
            icon: Coins,
            title: "Монеты вместо рублей",
            text: "Оплачивайте размещение и сделки внутренней валютой платформы.",
          },
          {
            icon: Gift,
            title: "Реферальная программа",
            text: "Приглашайте друзей и получайте бонусные монеты на кошелёк.",
          },
          {
            icon: Search,
            title: "Удобный каталог",
            text: "Фильтры по категориям и поиск по объявлениям в вашем городе.",
          },
        ].map(({ icon: Icon, title, text }) => (
          <div
            key={title}
            className="bg-white rounded-2xl border border-slate-100 p-6 shadow-sm hover:shadow-md transition-shadow"
          >
            <div className="w-12 h-12 rounded-xl bg-primary/10 flex items-center justify-center mb-4">
              <Icon className="h-6 w-6 text-primary" />
            </div>
            <h3 className="font-heading font-semibold text-slate-900 mb-2">{title}</h3>
            <p className="text-sm text-slate-500 leading-relaxed">{text}</p>
          </div>
        ))}
      </section>
    </div>
  );
}
