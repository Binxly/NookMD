import { Navbar, NavbarBrand, NavbarContent } from "@nextui-org/react";

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen bg-gray-100">
      {children}
    </div>
  );
} 