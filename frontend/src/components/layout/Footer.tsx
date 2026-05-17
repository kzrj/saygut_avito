export function Footer() {
  return (
    <footer className="mt-auto bg-white border-t border-slate-200 px-8 py-6 flex flex-col sm:flex-row items-center justify-between text-[10px] text-slate-400 font-bold uppercase tracking-widest gap-4">
      <div className="flex flex-wrap justify-center sm:justify-start gap-4 sm:gap-6">
        <span>© 2026 Витрина Улан-Удэ</span>
        <a href="#" className="hover:text-primary transition-colors">
          Помощь
        </a>
        <a href="#" className="hover:text-primary transition-colors">
          Безопасность
        </a>
        <a href="#" className="hover:text-primary transition-colors">
          Правила
        </a>
      </div>
      <div className="flex items-center space-x-4">
        <span className="px-2 py-1 bg-green-50 text-green-600 rounded normal-case tracking-normal font-semibold text-xs">
          Маркетплейс на монетах
        </span>
      </div>
    </footer>
  );
}
