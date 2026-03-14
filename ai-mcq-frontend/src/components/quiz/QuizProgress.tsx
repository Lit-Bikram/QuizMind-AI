interface QuizProgressProps {
  current: number;
  total: number;
}

const QuizProgress = ({ current, total }: QuizProgressProps) => {
  const progress = total > 0 ? (current / total) * 100 : 0;

  return (
    <div className="progress-card">
      <div className="progress-header">
        <span>Progress</span>
        <span>
          {current} / {total}
        </span>
      </div>

      <div className="progress-bar-bg">
        <div
          className="progress-bar-fill"
          style={{ width: `${progress}%` }}
        />
      </div>
    </div>
  );
};

export default QuizProgress;