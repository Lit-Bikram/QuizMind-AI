import type { DifficultyStats } from "../../types/quiz";

interface DifficultyChartProps {
  difficultyBreakdown: Record<string, DifficultyStats>;
}

const DifficultyChart = ({ difficultyBreakdown }: DifficultyChartProps) => {
  const levels = ["easy", "medium", "hard"];

  return (
    <div className="results-card">
      <h2 style={{ marginBottom: "18px", color: "#172554" }}>Difficulty Breakdown</h2>

      <div className="difficulty-list">
        {levels.map((level) => {
          const stats = difficultyBreakdown[level] || {
            total: 0,
            correct: 0,
            accuracy: 0,
          };

          return (
            <div key={level} className="difficulty-item">
              <div className="difficulty-row">
                <span style={{ textTransform: "capitalize" }}>{level}</span>
                <span>
                  {stats.correct} / {stats.total} correct
                </span>
              </div>

              <div className="difficulty-bar-bg">
                <div
                  className="difficulty-bar-fill"
                  style={{ width: `${stats.accuracy}%` }}
                />
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default DifficultyChart;