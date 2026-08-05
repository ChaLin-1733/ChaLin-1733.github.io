import type { Metadata } from "next";
import { DM_Sans, Fraunces } from "next/font/google";
import "./globals.css";

const sans = DM_Sans({ variable: "--font-sans", subsets: ["latin"] });
const display = Fraunces({ variable: "--font-display", subsets: ["latin"] });

export const metadata: Metadata = {
  metadataBase: new URL("https://chalin-1733.github.io"),
  title: "Cha Lin, Ph.D. - Computational Biomedical Imaging",
  description: "Academic portfolio of Cha Lin - medical AI, multimodal neuroimaging and biomarkers.",
  openGraph: {
    title: "Cha Lin, Ph.D. - Computational Biomedical Imaging",
    description: "Academic portfolio of Cha Lin - medical AI, multimodal neuroimaging and biomarkers.",
    type: "website",
    images: ["/og.png"],
  },
  twitter: {
    card: "summary_large_image",
    title: "Cha Lin, Ph.D. - Computational Biomedical Imaging",
    description: "Academic portfolio of Cha Lin - medical AI, multimodal neuroimaging and biomarkers.",
    images: ["/og.png"],
  },
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body className={`${sans.variable} ${display.variable}`}>{children}</body>
    </html>
  );
}
