import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Opera - Personal Intelligence OS",
  description: "Your personal AI assistant powered by local Llama model",
  manifest: "/manifest.json",
  appleWebApp: {
    capable: true,
    statusBarStyle: "black-translucent",
    title: "Opera AI",
  },
  icons: {
    apple: "/icon.svg",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <head>
        <link rel="manifest" href="/manifest.json" />
        <meta name="apple-mobile-web-app-capable" content="yes" />
        <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent" />
        <meta name="apple-mobile-web-app-title" content="Opera" />
        <link rel="apple-touch-icon" href="/icon.svg" />
        <meta name="theme-color" content="#6366f1" />
        <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no, viewport-fit=cover" />
      </head>
      <body className="antialiased">
        {children}
      </body>
    </html>
  );
}
