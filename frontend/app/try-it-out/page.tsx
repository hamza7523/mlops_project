import React from "react";
import Header from "@/components/Header";

export default function LearnMorePage() {
  return (
    <div className="min-h-screen bg-black text-white flex flex-col items-center justify-start overflow-hidden">
       <div className="w-full z-50">
        <Header />
      </div>

      <div className="flex-1 flex flex-col items-center justify-center p-4 w-full max-w-4xl mt-20">
        <div className="text-center space-y-8">
          <h1 className="text-5xl md:text-7xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-green-400 to-blue-500">
            Coming Soon
          </h1>
          <p className="text-xl text-neutral-400 max-w-2xl mx-auto">
            We are building a comprehensive guide to our botanical intelligence system.
            Check back soon for detailed documentation, case studies, and technical deep dives.
          </p>

          <div className="p-8 border border-neutral-800 rounded-2xl bg-neutral-900/50 backdrop-blur-sm">
            <p className="text-sm text-neutral-500 uppercase tracking-widest mb-4">What to expect</p>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-left">
              <div className="p-4 bg-neutral-900 rounded-lg">
                <h3 className="text-green-400 font-semibold mb-2">Architecture</h3>
                <p className="text-neutral-400 text-sm">Deep dive into our RAG + CNN hybrid model structure.</p>
              </div>
              <div className="p-4 bg-neutral-900 rounded-lg">
                <h3 className="text-blue-400 font-semibold mb-2">Dataset</h3>
                <p className="text-neutral-400 text-sm">Exploration of the 50k+ image dataset used for training.</p>
              </div>
              <div className="p-4 bg-neutral-900 rounded-lg">
                <h3 className="text-purple-400 font-semibold mb-2">API Docs</h3>
                <p className="text-neutral-400 text-sm">Full reference for integrating Flora Care into your apps.</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
