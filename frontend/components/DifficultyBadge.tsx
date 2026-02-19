type Props = { score: number };
export default function DifficultyBadge({ score }: Props) {
  return <span>Difficulty {score}</span>;
}
