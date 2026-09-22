import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Digital Sippoy",
  description: "Digital Sippoy — Next.js 15.5.12 / React 19.1.0 reference app",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
