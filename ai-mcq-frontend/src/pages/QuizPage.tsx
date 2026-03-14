import { useMemo, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { toast } from "react-toastify";

import QuestionCard from "../components/quiz/QuestionCard";
import QuizNavigation from "../components/quiz/QuizNavigation";
import QuizProgress from "../components/quiz/QuizProgress";
import { submitQuiz } from "../services/api";
import type { QuizQuestion, QuizResult } from "../types/quiz";

interface QuizLocationState {
  questions?: QuizQuestion[];
  requestedCount?: number;
  sessionId?: string | null;
}

function QuizPage() {
  const navigate = useNavigate();
  const location = useLocation();

  const {
    questions = [],
    requestedCount = 0,
    sessionId = null,
  } = (location.state as QuizLocationState) || {};

  const [currentIndex, setCurrentIndex] = useState(0);
  const [userAnswers, setUserAnswers] = useState<Record<string, string>>({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  const totalQuestions = questions.length;
  const currentQuestion = questions[currentIndex];

  const currentQuestionId = useMemo(() => {
    if (!currentQuestion) return "";
    return currentQuestion.id ?? String(currentIndex);
  }, [currentQuestion, currentIndex]);

  if (!questions.length || !currentQuestion) {
    return (
      <div className="quiz-page">
        <div className="results-card">
          <h1>No Quiz Data Found</h1>
          <p style={{ marginTop: "10px", color: "#64748b" }}>
            Please generate a new quiz first.
          </p>
          <div className="center-actions">
            <button
              className="primary-btn"
              onClick={() => navigate("/")}
              style={{ marginTop: "20px" }}
            >
              Back to Upload
            </button>
          </div>
        </div>
      </div>
    );
  }

  const handleSelectAnswer = (answer: string) => {
    setUserAnswers((prev) => ({
      ...prev,
      [currentQuestionId]: answer,
    }));
  };

  const handlePrevious = () => {
    if (currentIndex > 0) {
      setCurrentIndex((prev) => prev - 1);
    }
  };

  const handleNext = () => {
    if (currentIndex < totalQuestions - 1) {
      setCurrentIndex((prev) => prev + 1);
    }
  };

  const buildFallbackResult = (): QuizResult => {
    const reviews = questions.map((question, index) => {
      const qid = question.id ?? String(index);
      const userAnswer = userAnswers[qid] || "Not answered";

      return {
        question_id: qid,
        question: question.question,
        user_answer: userAnswer,
        correct_answer: question.correct_answer,
        is_correct: userAnswer === question.correct_answer,
        difficulty: question.difficulty,
        explanation: question.explanation,
        confidence_score: question.confidence_score,
        is_verified: question.is_verified,
      };
    });

    const correctCount = reviews.filter((r) => r.is_correct).length;
    const incorrectCount = reviews.length - correctCount;
    const percentage = reviews.length
      ? Math.round((correctCount / reviews.length) * 100)
      : 0;

    const difficulty_breakdown: QuizResult["difficulty_breakdown"] = {
      easy: { total: 0, correct: 0, accuracy: 0 },
      medium: { total: 0, correct: 0, accuracy: 0 },
      hard: { total: 0, correct: 0, accuracy: 0 },
    };

    reviews.forEach((review) => {
      const level = review.difficulty as "easy" | "medium" | "hard";
      if (!difficulty_breakdown[level]) return;

      difficulty_breakdown[level].total += 1;
      if (review.is_correct) {
        difficulty_breakdown[level].correct += 1;
      }
    });

    (Object.keys(difficulty_breakdown) as Array<"easy" | "medium" | "hard">).forEach(
      (level) => {
        const bucket = difficulty_breakdown[level];
        bucket.accuracy = bucket.total
          ? Math.round((bucket.correct / bucket.total) * 100)
          : 0;
      }
    );

    const weakAreas = reviews
      .filter((r) => !r.is_correct)
      .map((r) => r.question)
      .slice(0, 5);

    return {
      message: "Quiz submitted and scored successfully",
      session_id: sessionId ?? "local-session",
      total_questions: reviews.length,
      correct_count: correctCount,
      incorrect_count: incorrectCount,
      percentage,
      difficulty_breakdown,
      question_reviews: reviews,
      weak_areas: weakAreas,
    };
  };

  const handleSubmit = async () => {
    const unanswered = questions.some((question, index) => {
      const qid = question.id ?? String(index);
      return !userAnswers[qid];
    });

    if (unanswered) {
      toast.error("Please answer all questions before submitting.");
      return;
    }

    try {
      setIsSubmitting(true);

      if (!sessionId) {
        const fallbackResult = buildFallbackResult();

        toast.success("Quiz submitted successfully!");
        navigate("/results", {
          state: { result: fallbackResult },
        });
        return;
      }

      const answersPayload: Record<string, string> = {};

      questions.forEach((question, index) => {
        const qid = question.id ?? String(index);
        answersPayload[qid] = userAnswers[qid];
      });

      const result = await submitQuiz({
        session_id: sessionId,
        answers: answersPayload,
      });

      toast.success("Quiz submitted successfully!");

      navigate("/results", {
        state: { result },
      });
    } catch (error: any) {
      console.error("Error submitting quiz:", error);

      toast.error(
        error?.response?.data?.detail ||
          error?.response?.data?.message ||
          "Failed to submit quiz. Please try again."
      );
    } finally {
      setIsSubmitting(false);
    }
  };

  const currentSelectedAnswer = userAnswers[currentQuestionId] || "";
  const isCurrentAnswered = !!currentSelectedAnswer;

  return (
    <div className="quiz-page">
      {requestedCount > totalQuestions && (
        <p
          style={{
            marginBottom: "16px",
            color: "#475569",
            fontSize: "0.95rem",
          }}
        >
          Requested {requestedCount} questions, but only {totalQuestions} high-quality
          questions were generated.
        </p>
      )}

      <QuizProgress current={currentIndex + 1} total={totalQuestions} />

      <QuestionCard
        question={currentQuestion}
        currentQuestionNumber={currentIndex + 1}
        totalQuestions={totalQuestions}
        selectedAnswer={currentSelectedAnswer}
        onSelectAnswer={handleSelectAnswer}
      />

      <QuizNavigation
        currentIndex={currentIndex}
        totalQuestions={totalQuestions}
        onPrevious={handlePrevious}
        onNext={handleNext}
        onSubmit={handleSubmit}
        isCurrentAnswered={isCurrentAnswered}
        isSubmitting={isSubmitting}
      />
    </div>
  );
}

export default QuizPage;