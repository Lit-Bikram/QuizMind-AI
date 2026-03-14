import { useLocation, useNavigate } from "react-router-dom";

import ScoreCard from "../components/results/ScoreCard";
import DifficultyChart from "../components/results/DifficultyChart";
import WeakAreas from "../components/results/WeakAreas";
import QuestionReview from "../components/results/QuestionReview";
import type { QuizResult } from "../types/quiz";

interface ResultsLocationState {
  result?: QuizResult;
  requestedCount?: number;
}

function ResultsPage() {
  const navigate = useNavigate();
  const location = useLocation();

  const { result, requestedCount } = (location.state as ResultsLocationState) || {};

  if (!result) {
    return (
      <div className="results-page">
        <div className="results-header">
          <h1>No Results Found</h1>
          <p>Please complete a quiz first to view results.</p>
        </div>

        <div className="center-actions">
          <button className="primary-btn" onClick={() => navigate("/")}>
            Generate New Quiz
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="results-page">
      <div className="results-header">
        <h1>Quiz Results</h1>
        <p>Here’s your performance summary and detailed review.</p>

        {requestedCount && requestedCount > result.total_questions && (
          <p
            style={{
              marginTop: "12px",
              color: "#475569",
              fontSize: "0.95rem",
            }}
          >
            You requested <strong>{requestedCount}</strong> questions, but only{" "}
            <strong>{result.total_questions}</strong> high-confidence questions
            could be generated from the selected PDF and query.
          </p>
        )}
      </div>

      <div className="score-grid">
        <ScoreCard label="Score" value={`${result.percentage}%`} type="neutral" />
        <ScoreCard
          label="Total Questions"
          value={result.total_questions}
          type="neutral"
        />
        <ScoreCard label="Correct" value={result.correct_count} type="correct" />
        <ScoreCard
          label="Incorrect"
          value={result.incorrect_count}
          type="incorrect"
        />
      </div>

      <div className="results-grid">
        <DifficultyChart difficultyBreakdown={result.difficulty_breakdown} />
        <WeakAreas weakAreas={result.weak_areas} />
      </div>

      <QuestionReview questionReviews={result.question_reviews} />

      <div className="center-actions">
        <button className="primary-btn" onClick={() => navigate("/")}>
          Generate New Quiz
        </button>
      </div>
    </div>
  );
}

export default ResultsPage;