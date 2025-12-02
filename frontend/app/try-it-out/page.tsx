"use client";

import React, { useState } from "react";
import { FileUpload } from "@/components/ui/file-upload";
import { Sidebar, SidebarBody, SidebarLink } from "@/components/ui/sidebar";
import {
  IconArrowLeft,
  IconBrandTabler,
  IconSettings,
  IconUserBolt,
} from "@tabler/icons-react";
import { motion } from "motion/react";
import { cn } from "@/lib/utils";

export default function TryItOut() {
  return <SidebarDemo />;
}

// Sidebar stuff
// temporary links added --@qamar

export function SidebarDemo() {
  const links = [
    {
      label: "Dashboard",
      href: "#",
      icon: (
        <IconBrandTabler className="h-5 w-5 shrink-0 text-neutral-700 dark:text-neutral-200" />
      ),
    },
    {
      label: "Profile",
      href: "#",
      icon: (
        <IconUserBolt className="h-5 w-5 shrink-0 text-neutral-700 dark:text-neutral-200" />
      ),
    },
    {
      label: "Settings",
      href: "#",
      icon: (
        <IconSettings className="h-5 w-5 shrink-0 text-neutral-700 dark:text-neutral-200" />
      ),
    },
    {
      label: "Logout",
      href: "#",
      icon: (
        <IconArrowLeft className="h-5 w-5 shrink-0 text-neutral-700 dark:text-neutral-200" />
      ),
    },
  ];
  const [open, setOpen] = useState(false);
  return (
    <div
      className={cn(
        "mx-auto flex w-full flex-1 flex-col overflow-hidden rounded-md bg-black md:flex-row",
        "h-screen" // for your use case, use `h-screen` instead of `h-[60vh]`
      )}
    >
      <Sidebar open={open} setOpen={setOpen}>
        <SidebarBody className="justify-between gap-10">
          <div className="flex flex-1 flex-col overflow-x-hidden overflow-y-auto">
            {open ? <Logo /> : <LogoIcon />}
            <div className="mt-8 flex flex-col gap-2">
              {links.map((link, idx) => (
                <SidebarLink key={idx} link={link} />
              ))}
            </div>
          </div>
          <div>
            <SidebarLink
              link={{
                label: "Qamar Raza",
                href: "#",
                icon: (
                  <IconUserBolt className="h-5 w-5 shrink-0 text-neutral-700 dark:text-neutral-200" />
                ),
              }}
            />
          </div>
        </SidebarBody>
      </Sidebar>
      <Dashboard />
    </div>
  );
}
export const Logo = () => {
  return (
    <a
      href="#"
      className="relative z-20 flex items-center space-x-2 py-1 text-sm font-normal"
    >
      <motion.span
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className="font-bold text-xl whitespace-pre text-white"
      >
        Fluora Care
      </motion.span>
    </a>
  );
};
// could add a logo but im not making it --@qamar
export const LogoIcon = () => {
  return (
    <a
      href="#"
      className="relative z-20 flex items-center justify-center py-1 text-sm font-bold text-white"
    >
      FC
    </a>
  );
};

// Dummy dashboard component with content
const Dashboard = () => {
  // --- 1. STATE MANAGEMENT ---
  // Existing state for the selected file
  const [files, setFiles] = useState<File[]>([]);

  // New state for the prediction result
  const [prediction, setPrediction] = useState<{ predicted_class: string; confidence: number } | null>(null);

  // New state to handle loading status while the model is working
  const [isLoading, setIsLoading] = useState(false);

  // New state to handle any errors from the API call
  const [error, setError] = useState<string | null>(null);


  // Handler to update the state when files are uploaded
  const handleFileUpload = (uploadedFiles: File[]) => {
    setFiles(uploadedFiles);
    // Reset previous results when a new file is uploaded
    setPrediction(null);
    setError(null);
  };

  // --- 2. API CALL FUNCTION ---
  // This function sends the image to your FastAPI backend
  const handleSubmit = async () => {
    if (files.length === 0) {
      setError("Please upload an image first.");
      return;
    }

    // Start loading and clear previous state
    setIsLoading(true);
    setError(null);
    setPrediction(null);

    const formData = new FormData();
    // The key "file" MUST match the parameter name in your FastAPI endpoint
    formData.append("file", files[0]);

    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";
      const response = await fetch(`${apiUrl}/predict`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        // Handle HTTP errors like 500 or 404
        throw new Error(`Server responded with ${response.status}`);
      }

      const result = await response.json();
      setPrediction(result);

    } catch (err: any) {
      setError(`Failed to get prediction. Please try again. Error: ${err.message}`);
      console.error("Prediction API error:", err);
    } finally {
      // Stop loading whether the request succeeded or failed
      setIsLoading(false);
    }
  };

  // Function to clear the selection and result
  const handleClear = () => {
    setFiles([]);
    setPrediction(null);
    setError(null);
  };

  return (
    <div className="flex flex-1">
      <main className="min-h-screen bg-black flex flex-col items-center justify-center text-white py-12 w-full">
        <div className="max-w-4xl w-full mx-auto text-center px-6">
          <h1 className="text-6xl font-bold mb-4 bg-gradient-to-r from-emerald-600 to-green-600 bg-clip-text text-transparent">
            Try It Out
          </h1>

          <div className="w-full max-w-2xl mx-auto min-h-80 flex items-center justify-center">
            {/* Show file upload only if no file is selected */}
            {files.length === 0 && <FileUpload onChange={handleFileUpload} />}

            {/* --- 3. UI FOR DISPLAYING IMAGE & RESULTS --- */}
            {files.length > 0 && (
              <div className="w-full text-center">
                {/* Display a preview of the uploaded image */}
                <img
                  src={URL.createObjectURL(files[0])}
                  alt="Uploaded preview"
                  className="max-w-xs max-h-64 mx-auto rounded-lg"
                />
                <p className="text-gray-400 mt-4">{files[0].name}</p>
              </div>
            )}
          </div>

          {/* Buttons and Results section */}
          <div className="mt-8">
            {/* Show Predict/Clear buttons only if a file is uploaded */}
            {files.length > 0 && (
              <div className="flex justify-center gap-4">
                <button
                  onClick={handleSubmit}
                  disabled={isLoading}
                  className="px-6 py-2 bg-emerald-600 text-white font-semibold rounded-lg hover:bg-emerald-700 disabled:bg-gray-500 disabled:cursor-not-allowed"
                >
                  {isLoading ? "Analyzing..." : "Predict"}
                </button>
                <button
                  onClick={handleClear}
                  className="px-6 py-2 bg-neutral-700 text-white font-semibold rounded-lg hover:bg-neutral-800"
                >
                  Clear
                </button>
              </div>
            )}

            {/* Display the Prediction Result */}
            {prediction && (
              <div className="mt-8 p-6 bg-neutral-900 rounded-lg text-left">
                <h3 className="text-2xl font-bold text-white">Prediction Result</h3>
                <p className="mt-4 text-lg">
                  <span className="font-semibold text-gray-400">Class: </span>
                  <span className="text-emerald-400">{prediction.predicted_class.replace(/___/g, ' ')}</span>
                </p>
                <p className="mt-2 text-lg">
                  <span className="font-semibold text-gray-400">Confidence: </span>
                  <span className="text-emerald-400">{(prediction.confidence * 100).toFixed(2)}%</span>
                </p>
              </div>
            )}

            {/* Display any Error Messages */}
            {error && (
              <div className="mt-8 p-4 bg-red-900/50 border border-red-500 text-red-300 rounded-lg">
                <p>{error}</p>
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
};
