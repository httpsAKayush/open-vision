"use client";
import { useEffect, useState } from "react";
import { useSearchParams, useRouter } from "next/navigation";
import { getRecommendations, analyzeRepo, analyzeIssues } from "@/lib/api";
import IssueRecommendationCard from "@/components/IssueRecommendationCard";
import { Loader2, FolderOpen, ArrowLeft } from "lucide-react";
import Link from "next/link";

export default function Recommend() {
  const params = useSearchParams();
  const router = useRouter();
  const username = params.get("user") || "";

  const [repoInput, setRepoInput] = useState("");
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const fetchRecommendations = async (fullName?: string) => {
    setLoading(true);
    setError("");
    try {
      if (fullName) {
        await analyzeRepo(fullName);
        await analyzeIssues(fullName);
      }
      const res = await getRecommendations(username, fullName || undefined);
      setData(res.data);
    } catch (e: any) {
      setError(e?.response?.data?.error || "Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (!username) { router.push("/"); return; }
    fetchRecommendations();
  }, [username]);

  const allEmpty = data && !data.recommendations.comfort.length &&
    !data.recommendations.growth.length && !data.recommendations.stretch.length;

  return (
    <main className="min-h-screen max-w-2xl mx-auto px-4 py-12">
      <div className="flex items-center gap-3 mb-8">
        <Link href={`/dashboard?user=${username}`} className="text-gray-500 hover:text-white transition">
          <ArrowLeft size={20} />
        </Link>
        <h1 className="text-xl font-bold">Recommendations</h1>
        {data && (
          <span className="ml-auto text-xs text-gray-500">
            skill: {data.skill_level.toFixed(2)}
          </span>
        )}
      </div>

      {/* Deep dive input */}
      <div className="flex gap-2 mb-6">
        <input
          type="text"
          placeholder="owner/repo for deep dive (optional)"
          value={repoInput}
          onChange={(e) => setRepoInput(e.target.value)}
          className="flex-1 bg-gray-900 border border-gray-700 rounded-lg px-4 py-2.5
            text-white placeholder-gray-600 text-sm focus:outline-none focus:border-gray-500"
        />
        <button
          onClick={() => fetchRecommendations(repoInput.trim() || undefined)}
          disabled={loading}
          className="bg-white text-black text-sm font-semibold px-4 py-2.5 rounded-lg
            hover:bg-gray-200 transition disabled:opacity-50 flex items-center gap-2"
        >
          {loading ? <Loader2 size={14} className="animate-spin" /> : "Search"}
        </button>
      </div>

      {error && <p className="text-red-400 text-sm mb-4">{error}</p>}

      {loading && (
        <div className="flex items-center justify-center py-20 text-gray-500">
          <Loader2 size={24} className="animate-spin mr-3" /> Analyzing...
        </div>
      )}

      {data && !loading && (
        <>
          {/* Anchor folders */}
          {data.anchor_folders?.length > 0 && (
            <div className="bg-gray-900 rounded-xl p-4 mb-6 flex items-start gap-3">
              <FolderOpen size={16} className="text-yellow-400 mt-0.5 shrink-0" />
              <div>
                <p className="text-xs text-gray-400 mb-1">Start exploring here</p>
                {data.anchor_folders.map((f: string) => (
                  <p key={f} className="text-sm font-mono text-yellow-300">{f}</p>
                ))}
              </div>
            </div>
          )}

          {allEmpty && (
            <p className="text-center text-gray-500 py-12 text-sm">
              No matching issues found. Try a specific repo using the search above.
            </p>
          )}

          {(["comfort", "growth", "stretch"] as const).map((band) => (
            data.recommendations[band].length > 0 && (
              <div key={band} className="mb-8">
                <h2 className="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-3">
                  {band === "comfort" ? "Comfort Zone" : band === "growth" ? "Growth Zone" : "Stretch Zone"}
                </h2>
                <div className="flex flex-col gap-3">
                  {data.recommendations[band].map((issue: any) => (
                    <IssueRecommendationCard key={issue.id} issue={issue} band={band} />
                  ))}
                </div>
              </div>
            )
          ))}
        </>
      )}
    </main>
  );
}