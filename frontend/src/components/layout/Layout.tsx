import { Outlet } from "react-router-dom";
import { Header } from "./Header";

export function Layout() {
  return (
    <>
      <Header />
      <main style={{ padding: "2rem 0", minHeight: "calc(100vh - 64px)" }}>
        <Outlet />
      </main>
    </>
  );
}
