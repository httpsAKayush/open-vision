type Props = { skill: number };

export default function SkillLevelMeter({ skill }: Props) {
  const percentage = (skill / 10) * 100;
  const getColor = () => {
    if (skill < 3) return "bg-blue-400";
    if (skill < 6) return "bg-yellow-400";
    if (skill < 9) return "bg-orange-400";
    return "bg-green-500";
  };

  return (
    <div className="w-full">
      <div className="flex justify-between text-sm mb-1">
        <span className="text-gray-400">Skill Level</span>
        <span className="font-bold text-white">{skill.toFixed(2)} / 10</span>
      </div>
      <div className="w-full bg-gray-700 rounded-full h-3">
        <div
          className={`${getColor()} h-3 rounded-full transition-all duration-700`}
          style={{ width: `${percentage}%` }}
        />
      </div>
      <div className="flex justify-between text-xs text-gray-500 mt-1">
        <span>Beginner</span>
        <span>Intermediate</span>
        <span>Expert</span>
      </div>
    </div>
  );
}