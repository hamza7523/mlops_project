// File: app/page.tsx

'use client';

import Aurora from '@/components/Aurora';
import GradientText from '@/components/GradientText';
import Link from 'next/link';
import Header from '@/components/Header';
import { motion } from "motion/react";

export default function Home() {
  const buttonClass = "bg-black/30 backdrop-blur-md border border-green-500/30 text-green-400 font-semibold py-4 px-12 rounded-full shadow-[0_0_15px_rgba(74,222,128,0.1)] hover:shadow-[0_0_30px_rgba(74,222,128,0.4)] hover:border-green-400 hover:scale-105 transition-all duration-300 ease-out min-w-[200px] flex justify-center items-center tracking-wide";

  return (
    <main className="relative flex min-h-screen flex-col items-center justify-start overflow-hidden bg-black selection:bg-green-500/30">

      {/* Header Wrapper */}
      <div className="w-full z-50">
        <Header />
      </div>

      {/* Background Layer */}
      <div className="absolute inset-0 z-0">
        <Aurora
          colorStops={["#1E4620", "#1A5D3B", "#2A9D8F"]}
          blend={0.5}
          amplitude={1.0}
          speed={0.5}
        />
        {/* Futuristic Grid Overlay */}
        <div className="absolute inset-0 bg-[linear-gradient(to_right,#222_1px,transparent_1px),linear-gradient(to_bottom,#222_1px,transparent_1px)] bg-[size:4rem_4rem] [mask-image:radial-gradient(ellipse_60%_50%_at_50%_0%,#000_70%,transparent_100%)] opacity-20 pointer-events-none"></div>
      </div>

      {/* Main Content Container - Aligned with max-width */}
      <div className="relative z-10 flex flex-col items-center justify-center w-full max-w-7xl mx-auto px-6 pt-32 md:pt-48 text-center">

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, ease: "easeOut" }}
        >
          <h1 className="mb-8 tracking-tighter">
            <GradientText
              colors={["#40ffaa", "#4079ff", "#40ffaa", "#4079ff", "#40ffaa"]}
              animationSpeed={8}
              showBorder={false}
              className="text-6xl font-bold md:text-8xl lg:text-9xl drop-shadow-2xl"
            >
              Fluora Care
            </GradientText>
          </h1>
        </motion.div>

        <motion.p
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.2, ease: "easeOut" }}
          className="max-w-3xl text-xl md:text-2xl text-neutral-300 mb-12 leading-relaxed font-light"
        >
          Experience the future of botanical intelligence.
          <br className="hidden md:block" />
          Advanced computer vision for precise plant health diagnostics.
        </motion.p>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.4, ease: "easeOut" }}
          className="flex flex-wrap items-center justify-center gap-6"
        >
          <Link href="/try-it-out" className={buttonClass}>
            Learn More
          </Link>
          <Link href="/learn-more" className={buttonClass}>
            Try It Out
          </Link>
        </motion.div>

        {/* Stats / Features Footer to fill space */}
        <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 1, delay: 0.8 }}
            className="mt-32 grid grid-cols-1 md:grid-cols-3 gap-12 text-center border-t border-neutral-800/50 pt-10 w-full max-w-4xl"
        >
            <div className="flex flex-col items-center group cursor-default">
                <span className="text-4xl font-bold text-[#40ffaa] mb-2 drop-shadow-[0_0_10px_rgba(64,255,170,0.5)]">99.86%</span>
                <span className="text-sm text-neutral-400 uppercase tracking-widest font-medium">Accuracy</span>
            </div>
            <div className="flex flex-col items-center group cursor-default">
                <span className="text-4xl font-bold text-white mb-2 drop-shadow-[0_0_10px_rgba(255,255,255,0.5)]">29 Diseases</span>
                <span className="text-sm text-neutral-400 uppercase tracking-widest font-medium">Detection</span>
            </div>
            <div className="flex flex-col items-center group cursor-default">
                <GradientText
                    colors={["#40ffaa", "#ef4444", "#166534", "#4079ff", "#40ffaa"]}
                    animationSpeed={16}
                    showBorder={false}
                    className="text-4xl font-bold mb-2 drop-shadow-[0_0_10px_rgba(64,121,255,0.5)] rounded-lg px-4 py-2"
                >
                    RAG Powered
                </GradientText>
                <span className="text-sm text-neutral-400 uppercase tracking-widest font-medium">Chatbot</span>
            </div>
        </motion.div>

      </div>
    </main>
  );
}
