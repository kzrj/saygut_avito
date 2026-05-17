import { FormEvent, useEffect, useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { Search, MapPin, Plus, LayoutGrid, Coins } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { useAuthStore } from "@/store/authStore";

export function Header() {
  const user = useAuthStore((s) => s.user);
  const logout = useAuthStore((s) => s.logout);
  const navigate = useNavigate();
  const location = useLocation();
  const [search, setSearch] = useState("");

  useEffect(() => {
    const params = new URLSearchParams(location.search);
    setSearch(params.get("q") || "");
  }, [location.pathname, location.search]);

  const submitSearch = (e?: FormEvent) => {
    e?.preventDefault();
    const q = search.trim();
    navigate(q ? `/catalog?q=${encodeURIComponent(q)}` : "/catalog");
  };

  return (
    <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container mx-auto px-4">
        <div className="flex h-16 items-center justify-between gap-4">
          <Link to="/" className="flex items-center gap-3 shrink-0">
            <div className="w-10 h-10 bg-primary rounded-lg flex items-center justify-center text-primary-foreground shadow-sm">
              <LayoutGrid className="h-6 w-6" />
            </div>
            <span className="font-heading text-2xl font-bold tracking-tight text-slate-800 uppercase hidden sm:block">
              Витрина
            </span>
          </Link>

          <form
            onSubmit={submitSearch}
            className="flex-1 max-w-xl mx-4 hidden md:flex items-center gap-2"
          >
            <div className="relative flex-1">
              <Search className="absolute left-4 top-1/2 -translate-y-1/2 h-5 w-5 text-slate-400" />
              <Input
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                placeholder="Поиск объявлений..."
                className="w-full bg-slate-100 border-none rounded-xl h-12 pl-12 pr-4 text-sm focus-visible:ring-2 focus-visible:ring-primary"
              />
            </div>
          </form>

          <div className="flex items-center gap-3 sm:gap-5">
            <div className="hidden sm:flex flex-col items-end">
              <span className="text-[10px] text-slate-400 font-bold uppercase tracking-wider">
                Локация
              </span>
              <span className="text-sm font-semibold border-b border-dotted border-primary text-primary leading-none">
                Улан-Удэ
              </span>
            </div>

            {user ? (
              <>
                <Link
                  to="/wallet"
                  className="hidden sm:flex items-center gap-1.5 text-sm font-semibold text-amber-600"
                >
                  <Coins className="h-4 w-4" />
                  {user.wallet_balance}
                </Link>
                <Button
                  type="button"
                  onClick={() => navigate("/create")}
                  className="hidden sm:flex bg-primary hover:bg-primary/90 text-white px-5 h-10 rounded-xl font-semibold shadow-sm gap-2"
                >
                  <Plus className="h-4 w-4" />
                  Подать объявление
                </Button>
                <div className="relative group">
                  <button
                    type="button"
                    className="w-10 h-10 bg-slate-100 rounded-full flex items-center justify-center text-sm font-bold text-slate-600 hover:bg-slate-200 transition-colors"
                    title={user.display_name}
                  >
                    {user.display_name.charAt(0).toUpperCase()}
                  </button>
                  <div className="absolute right-0 top-full mt-2 w-48 bg-white rounded-xl shadow-lg border border-slate-100 py-2 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all z-50">
                    <p className="px-4 py-2 text-sm font-medium text-slate-800 truncate">
                      {user.display_name}
                    </p>
                    <Link
                      to="/wallet"
                      className="block px-4 py-2 text-sm text-slate-600 hover:bg-slate-50"
                    >
                      Кошелёк
                    </Link>
                    <button
                      type="button"
                      onClick={() => {
                        logout();
                        navigate("/login");
                      }}
                      className="w-full text-left px-4 py-2 text-sm text-slate-600 hover:bg-slate-50"
                    >
                      Выйти
                    </button>
                  </div>
                </div>
              </>
            ) : (
              <>
                <Link
                  to="/login"
                  className="text-sm font-semibold text-slate-600 hover:text-primary"
                >
                  Вход
                </Link>
                <Button type="button" onClick={() => navigate("/register")} className="rounded-xl font-semibold">
                  Регистрация
                </Button>
              </>
            )}
          </div>
        </div>

        <form onSubmit={submitSearch} className="flex md:hidden pb-4 gap-2">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <Input
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Поиск..."
              className="pl-10 w-full bg-secondary/50 border-none h-10"
            />
          </div>
          <Button type="button" variant="outline" size="sm" className="gap-1 border-none bg-secondary/50">
            <MapPin className="h-3 w-3" />
            Улан-Удэ
          </Button>
        </form>
      </div>
    </header>
  );
}
