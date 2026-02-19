type Props = { value: number };
export default function SkillLevelMeter({ value }: Props) {
  return <div>Skill: {value}/10</div>;
}
