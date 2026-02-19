"use client";
import { useState } from "react";
import { useSearchParams, useRouter } from "next/navigation";
import { submitGrowth } from "@/lib/api";
import { Loader2, ArrowLeft, TrendingUp } from "lucide-react";
import Link from "next/link";

export default function Submit() {
  const params = useSearchParams();
  const username = params.get("user") || "";
  const [prUrl, setPrUrl] = useState("");
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async () => {
    if (!prUrl.trim()) return;
    setLoading(true);
    setError("");
    try {
      const res = await submitGrowth(username, prUrl.trim());
      setResult(res.data);
    } catch (e: any) {
      setError(e?.response?.data?.error || "Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen max-w-2xl mx-auto px-4 py-12">
      <div className="flex items-center gap-3 mb-8">
        <Link href={`/dashboard?user=${username}`} className="text-gray-500 hover:text-white transition">
          <ArrowLeft size={20} />
        </Link>
        <h1 className="text-xl font-bold">Submit a PR</h1>
      </div>

      <p className="text-gray-400 text-sm mb-6">
        Paste the GitHub API URL of a pull request you submitted.
        Format: <span className="font-mono text-gray-300">https://api.github.com/repos/owner/repo/pulls/number</span>
      </p>

      <div className="flex flex-col gap-3 mb-6">
        <input
          type="text"
          placeholder="https://api.github.com/repos/owner/repo/pulls/123"
          value={prUrl}
          onChange={(e) => setPrUrl(e.target.value)}
          className="w-full bg-gray-900 border border-gray-700 rounded-lg px-4 py-3
            text-white placeholder-gray-600 text-sm focus:outline-none focus:border-gray-500"
        />
        <button
          onClick={handleSubmit}
          disabled={loading}
          className="bg-white text-black font-semibold py-3 rounded-xl
            hover:bg-gray-200 transition disabled:opacity-50 flex items-center justify-center gap-2"
        >
          {loading ? <Loader2 size={16} className="animate-spin" /> : "Update My Skill"}
        </button>
      </div>

      {error && <p className="text-red-400 text-sm">{error}</p>}

      {result && (
        <div className="bg-gray-900 rounded-2xl p-6">
          <div className="flex items-center gap-2 mb-4">
            <TrendingUp size={18} className="text-green-400" />
            <h2 className="font-semibold">Skill Updated</h2>
          </div>
          <div className="grid grid-cols-2 gap-4 text-center">
            <div className="bg-gray-800 rounded-xl p-4">
              <p className="text-xs text-gray-500 mb-1">Before</p>
              <p className="text-2xl font-bold text-gray-300">{result.old_skill.toFixed(2)}</p>
            </div>
            <div className="bg-gray-800 rounded-xl p-4">
              <p className="text-xs text-gray-500 mb-1">After</p>
              <p className="text-2xl font-bold text-green-400">{result.new_skill.toFixed(2)}</p>
            </div>
          </div>
          <div className="mt-4 text-center text-sm text-gray-500">
            +{result.growth_factor} growth from a difficulty {result.pr_difficulty} PR
          </div>
        </div>
      )}
    </main>
  );
}