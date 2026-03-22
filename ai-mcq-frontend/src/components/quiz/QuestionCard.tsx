import type { QuizQuestion } from "../../types/quiz";

interface QuestionCardProps {
  question: QuizQuestion;
  currentQuestionNumber: number;
  totalQuestions: number;
  selectedAnswer: string;
  onSelectAnswer: (answer: string) => void;
}

const QuestionCard = ({
  question,
  currentQuestionNumber,
  totalQuestions,
  selectedAnswer,
  onSelectAnswer,
}: QuestionCardProps) => {
  return (
    <div className="question-card">
      <div className="question-meta">
        Question {currentQuestionNumber} of {totalQuestions} • {question.difficulty}
      </div>

      <h2 className="question-text">{question.question}</h2>

      <div className="options-list">
        {question.options.map((option, index) => {
          const optionText = option.text;

          // Always derive labels from displayed order
          const optionLabel = String.fromCharCode(65 + index); // A, B, C, D

          // Backend expects labels
          const optionValue = optionLabel;

          const isSelected = selectedAnswer === optionValue;

          return (
            <button
              key={`${optionLabel}-${optionText}`}
              type="button"
              className={`option-btn ${isSelected ? "selected" : ""}`}
              onClick={() => onSelectAnswer(optionValue)}
            >
              <span className="option-label">{optionLabel}.</span>
              <span>{optionText}</span>
            </button>
          );
        })}
      </div>
    </div>
  );
};

export default QuestionCard;