import DifficultyBadge from "./DifficultyBadge";
import { ExternalLink } from "lucide-react";

type Issue = {
  id: number;
  github_issue_number: number;
  title: string;
  difficulty_score: number;
  labels: string[];
  comment_count: number;
  html_url: string;
  matched_keywords?: string[];
  is_good_first_issue: boolean;
};

type Props = { issue: Issue; band: "comfort" | "growth" | "stretch" };

const bandStyles = {
  comfort: "border-blue-800 bg-blue-950/30",
  growth:  "border-yellow-800 bg-yellow-950/30",
  stretch: "border-orange-800 bg-orange-950/30",
};

const bandLabels = {
  comfort: "Comfort Zone",
  growth:  "Growth Zone",
  stretch: "Stretch Zone",
};

export default function IssueRecommendationCard({ issue, band }: Props) {
  return (
    <div className={`rounded-xl border p-4 ${bandStyles[band]} hover:brightness-110 transition`}>
      <div className="flex items-start justify-between gap-2">
        <div className="flex-1">
          <div className="flex items-center gap-2 mb-1 flex-wrap">
            <span className="text-xs text-gray-500">#{issue.github_issue_number}</span>
            <span className={`text-xs px-2 py-0.5 rounded-full font-medium
              ${band === "comfort" ? "bg-blue-900 text-blue-300" :
                band === "growth" ? "bg-yellow-900 text-yellow-300" :
                "bg-orange-900 text-orange-300"}`}>
              {bandLabels[band]}
            </span>
            {issue.is_good_first_issue && (
              <span className="text-xs px-2 py-0.5 rounded-full bg-green-900 text-green-300">
                Good First Issue
              </span>
            )}
          </div>
          <h3 className="text-white font-medium text-sm leading-snug">{issue.title}</h3>
          {issue.matched_keywords && issue.matched_keywords.length > 0 && (
            <div className="flex gap-1 flex-wrap mt-2">
              {issue.matched_keywords.map((kw) => (
                <span key={kw} className="text-xs bg-gray-800 text-gray-400 px-2 py-0.5 rounded">
                  {kw}
                </span>
              ))}
            </div>
          )}
          <div className="flex items-center gap-3 mt-2 text-xs text-gray-500">
            <span>{issue.comment_count} comments</span>
            {issue.labels.slice(0, 2).map((l) => (
              <span key={l} className="bg-gray-800 px-2 py-0.5 rounded">{l}</span>
            ))}
          </div>
        </div>
        <div className="flex flex-col items-end gap-2 shrink-0">
          <DifficultyBadge score={issue.difficulty_score} />
          <a href={issue.html_url} target="_blank" rel="noopener noreferrer"
            className="text-gray-500 hover:text-white transition">
            <ExternalLink size={14} />
          </a>
        </div>
      </div>
    </div>
  );
}