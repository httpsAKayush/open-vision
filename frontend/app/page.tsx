"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import { analyzeUser } from "@/lib/api";
import { Github, Loader2 } from "lucide-react";

export default function Home() {
  const [username, setUsername] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const router = useRouter();

  const handleSubmit = async () => {
    if (!username.trim()) return;
    setLoading(true);
    setError("");
    try {
      await analyzeUser(username.trim());
      router.push(`/dashboard?user=${username.trim()}`);
    } catch (e: any) {
      setError(e?.response?.data?.error || "Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen flex flex-col items-center justify-center px-4">
      <div className="max-w-md w-full text-center">
        <div className="flex items-center justify-center gap-3 mb-6">
          <Github size={36} className="text-white" />
          <h1 className="text-3xl font-bold">OpenVision</h1>
        </div>
        <p className="text-gray-400 mb-8 text-sm leading-relaxed">
          Enter your GitHub username. We'll analyze your skills and recommend
          the right open source issues for your level.
        </p>

        <div className="flex gap-2">
          <input
            type="text"
            placeholder="github username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSubmit()}
            className="flex-1 bg-gray-900 border border-gray-700 rounded-lg px-4 py-3
              text-white placeholder-gray-600 focus:outline-none focus:border-gray-500"
          />
          <button
            onClick={handleSubmit}
            disabled={loading}
            className="bg-white text-black font-semibold px-5 py-3 rounded-lg
              hover:bg-gray-200 transition disabled:opacity-50 flex items-center gap-2"
          >
            {loading ? <Loader2 size={16} className="animate-spin" /> : "Analyze"}
          </button>
        </div>

        {error && <p className="text-red-400 text-sm mt-3">{error}</p>}
      </div>
    </main>
  );
}