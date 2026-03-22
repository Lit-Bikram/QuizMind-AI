import type { QuestionReview as QuestionReviewType } from "../../types/quiz";

interface QuestionReviewProps {
  questionReviews: QuestionReviewType[];
}

const QuestionReview = ({ questionReviews }: QuestionReviewProps) => {
  return (
    <div className="results-card">
      <h2 style={{ marginBottom: "18px", color: "#172554" }}>Question Review</h2>

      {!questionReviews.length ? (
        <p style={{ color: "#64748b" }}>No review data available.</p>
      ) : (
        <div className="review-list">
          {questionReviews.map((review, index) => (
            <div
              key={review.question_id || index}
              className={`review-item ${review.is_correct ? "correct" : "incorrect"}`}
            >
              <div className="review-question">
                Q{index + 1}. {review.question}
              </div>

              <div className="review-answer">
                <strong>Your Answer:</strong> {review.user_answer || "Not answered"}
              </div>

              <div className="review-answer">
                <strong>Correct Answer:</strong> {review.correct_answer}
              </div>

              <div className="review-answer">
                <strong>Difficulty:</strong> {review.difficulty}
              </div>

              <div className="review-answer">
                <strong>Result:</strong>{" "}
                <span style={{ color: review.is_correct ? "#16a34a" : "#dc2626" }}>
                  {review.is_correct ? "Correct" : "Incorrect"}
                </span>
              </div>

              {review.explanation && (
                <div className="review-explanation">
                  <strong>Explanation:</strong> {review.explanation}
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default QuestionReview;