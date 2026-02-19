"use client";
import { useEffect, useState } from "react";
import { useSearchParams, useRouter } from "next/navigation";
import { getUser } from "@/lib/api";
import SkillLevelMeter from "@/components/SkillLevelMeter";
import { Github, Layers, GitPullRequest, Star } from "lucide-react";
import Link from "next/link";

export default function Dashboard() {
  const params = useSearchParams();
  const router = useRouter();
  const username = params.get("user") || "";
  const [profile, setProfile] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!username) { router.push("/"); return; }
    getUser(username)
      .then((res) => setProfile(res.data))
      .catch(() => router.push("/"))
      .finally(() => setLoading(false));
  }, [username]);

  if (loading) return (
    <div className="min-h-screen flex items-center justify-center text-gray-400">
      Loading profile...
    </div>
  );

  if (!profile) return null;

  return (
    <main className="min-h-screen max-w-2xl mx-auto px-4 py-12">
      <div className="flex items-center gap-3 mb-8">
        <Github size={24} />
        <h1 className="text-xl font-bold">{profile.github_username}</h1>
      </div>

      <div className="bg-gray-900 rounded-2xl p-6 mb-6">
        <SkillLevelMeter skill={profile.skill_level} />
      </div>

      <div className="grid grid-cols-3 gap-4 mb-8">
        <div className="bg-gray-900 rounded-xl p-4 text-center">
          <Layers size={20} className="mx-auto mb-2 text-gray-400" />
          <p className="text-2xl font-bold">{profile.total_repos}</p>
          <p className="text-xs text-gray-500 mt-1">Repos</p>
        </div>
        <div className="bg-gray-900 rounded-xl p-4 text-center">
          <GitPullRequest size={20} className="mx-auto mb-2 text-gray-400" />
          <p className="text-2xl font-bold">{profile.total_prs}</p>
          <p className="text-xs text-gray-500 mt-1">Pull Requests</p>
        </div>
        <div className="bg-gray-900 rounded-xl p-4 text-center">
          <Star size={20} className="mx-auto mb-2 text-gray-400" />
          <p className="text-2xl font-bold">{profile.total_stars}</p>
          <p className="text-xs text-gray-500 mt-1">Stars</p>
        </div>
      </div>

      <div className="bg-gray-900 rounded-xl p-4 mb-6">
        <p className="text-xs text-gray-500 mb-3">Domain Keywords</p>
        <div className="flex flex-wrap gap-2">
          {profile.domain_keywords.map((kw: string) => (
            <span key={kw} className="text-xs bg-gray-800 text-gray-300 px-3 py-1 rounded-full">
              {kw}
            </span>
          ))}
        </div>
      </div>

      <div className="flex flex-col gap-3">
        <Link href={`/recommend?user=${username}`}
          className="w-full bg-white text-black font-semibold py-3 rounded-xl text-center hover:bg-gray-200 transition">
          Get Recommendations
        </Link>
        <Link href={`/submit?user=${username}`}
          className="w-full bg-gray-900 text-white font-semibold py-3 rounded-xl text-center hover:bg-gray-800 transition border border-gray-700">
          Submit a PR
        </Link>
      </div>
    </main>
  );
}