"use client";

import { PdfManager } from "@/components/pdf/pdf-manager";
import { useState, useEffect } from "react";
import Layout from "@/components/layout/Layout";

export default function TestPage() {
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  // Return null during SSR to prevent hydration mismatch
  if (!mounted) {
    return null;
  }

  return (
    <Layout>
      <PdfManager />
    </Layout>
  );
}