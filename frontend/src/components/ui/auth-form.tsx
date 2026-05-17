import type { ReactNode } from "react";
import { cn } from "@/lib/utils";

export function AuthShell({
  title,
  subtitle,
  children,
}: {
  title: string;
  subtitle?: string;
  children: ReactNode;
}) {
  return (
    <div className="container mx-auto px-4 py-10 max-w-md">
      <h1 className="font-heading text-3xl font-bold text-slate-900 mb-2">{title}</h1>
      {subtitle && <p className="text-slate-500 mb-6">{subtitle}</p>}
      <div className="bg-white rounded-2xl border border-slate-100 shadow-sm p-6 md:p-8">
        {children}
      </div>
    </div>
  );
}

export function FormField({
  label,
  htmlFor,
  children,
  className,
}: {
  label: string;
  htmlFor?: string;
  children: ReactNode;
  className?: string;
}) {
  return (
    <div className={cn("mb-4", className)}>
      <label
        htmlFor={htmlFor}
        className="block text-xs font-bold text-slate-400 uppercase tracking-wider mb-2"
      >
        {label}
      </label>
      {children}
    </div>
  );
}

export function TabSwitch<T extends string>({
  value,
  options,
  onChange,
}: {
  value: T;
  options: { id: T; label: string }[];
  onChange: (v: T) => void;
}) {
  return (
    <div className="flex gap-1 mb-6 bg-slate-100 p-1 rounded-xl">
      {options.map((opt) => (
        <button
          key={opt.id}
          type="button"
          onClick={() => onChange(opt.id)}
          className={cn(
            "flex-1 py-2.5 text-sm font-semibold rounded-lg transition-all",
            value === opt.id
              ? "bg-white text-primary shadow-sm"
              : "text-slate-500 hover:text-slate-700"
          )}
        >
          {opt.label}
        </button>
      ))}
    </div>
  );
}
