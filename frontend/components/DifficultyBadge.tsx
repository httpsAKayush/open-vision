type Props = { score: number };

export default function DifficultyBadge({ score }: Props) {
  const getStyle = () => {
    if (score <= 2) return "bg-green-900 text-green-300 border border-green-700";
    if (score <= 4) return "bg-yellow-900 text-yellow-300 border border-yellow-700";
    if (score <= 7) return "bg-orange-900 text-orange-300 border border-orange-700";
    return "bg-red-900 text-red-300 border border-red-700";
  };

  const getLabel = () => {
    if (score <= 2) return "Easy";
    if (score <= 4) return "Medium";
    if (score <= 7) return "Hard";
    return "Expert";
  };

  return (
    <span className={`text-xs px-2 py-1 rounded-full font-semibold ${getStyle()}`}>
      {getLabel()} {score.toFixed(1)}
    </span>
  );
}