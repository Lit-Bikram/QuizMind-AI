interface QuizNavigationProps {
  currentIndex: number;
  totalQuestions: number;
  onPrevious: () => void;
  onNext: () => void;
  onSubmit: () => void;
  isCurrentAnswered: boolean;
  isSubmitting?: boolean;
}

const QuizNavigation = ({
  currentIndex,
  totalQuestions,
  onPrevious,
  onNext,
  onSubmit,
  isCurrentAnswered,
  isSubmitting = false,
}: QuizNavigationProps) => {
  const isFirst = currentIndex === 0;
  const isLast = currentIndex === totalQuestions - 1;

  return (
    <div className="quiz-nav">
      <button
        type="button"
        className="secondary-btn"
        onClick={onPrevious}
        disabled={isFirst}
      >
        Previous
      </button>

      {isLast ? (
        <button
          type="button"
          className="primary-btn"
          onClick={onSubmit}
          disabled={!isCurrentAnswered || isSubmitting}
        >
          {isSubmitting ? "Submitting..." : "Submit Quiz"}
        </button>
      ) : (
        <button
          type="button"
          className="primary-btn"
          onClick={onNext}
          disabled={!isCurrentAnswered}
        >
          Next
        </button>
      )}
    </div>
  );
};

export default QuizNavigation;