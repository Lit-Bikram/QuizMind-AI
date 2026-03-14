interface ScoreCardProps {
  label: string;
  value: string | number;
  type?: "score" | "correct" | "incorrect" | "neutral";
}

const ScoreCard = ({ label, value, type = "neutral" }: ScoreCardProps) => {
  return (
    <div className="score-card">
      <p className="score-label">{label}</p>
      <h3 className={`score-value ${type}`}>{value}</h3>
    </div>
  );
};

export default ScoreCard;