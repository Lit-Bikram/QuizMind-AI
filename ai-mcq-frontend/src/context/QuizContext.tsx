import { createContext, useContext, useReducer } from "react";
import type { ReactNode, Dispatch } from "react";
import type { QuizQuestion, QuizResult, UserAnswers } from "../types/quiz";

interface QuizState {
  file: File | null;
  topic: string;
  numberOfQuestions: number;
  sessionId: string;
  questions: QuizQuestion[];
  currentQuestionIndex: number;
  userAnswers: UserAnswers;
  results: QuizResult | null;
}

type QuizAction =
  | { type: "SET_FILE"; payload: File | null }
  | { type: "SET_TOPIC"; payload: string }
  | { type: "SET_NUMBER_OF_QUESTIONS"; payload: number }
  | { type: "SET_SESSION_ID"; payload: string }
  | { type: "SET_QUESTIONS"; payload: QuizQuestion[] }
  | { type: "SET_CURRENT_QUESTION_INDEX"; payload: number }
  | {
      type: "SET_USER_ANSWER";
      payload: { questionId: number; answer: string };
    }
  | { type: "SET_RESULTS"; payload: QuizResult | null }
  | { type: "RESET_QUIZ" };

const initialState: QuizState = {
  file: null,
  topic: "",
  numberOfQuestions: 5,
  sessionId: "",
  questions: [],
  currentQuestionIndex: 0,
  userAnswers: {},
  results: null,
};

const quizReducer = (state: QuizState, action: QuizAction): QuizState => {
  switch (action.type) {
    case "SET_FILE":
      return {
        ...state,
        file: action.payload,
      };

    case "SET_TOPIC":
      return {
        ...state,
        topic: action.payload,
      };

    case "SET_NUMBER_OF_QUESTIONS":
      return {
        ...state,
        numberOfQuestions: action.payload,
      };

    case "SET_SESSION_ID":
      return {
        ...state,
        sessionId: action.payload,
      };

    case "SET_QUESTIONS":
      return {
        ...state,
        questions: action.payload,
      };

    case "SET_CURRENT_QUESTION_INDEX":
      return {
        ...state,
        currentQuestionIndex: action.payload,
      };

    case "SET_USER_ANSWER":
      return {
        ...state,
        userAnswers: {
          ...state.userAnswers,
          [action.payload.questionId]: action.payload.answer,
        },
      };

    case "SET_RESULTS":
      return {
        ...state,
        results: action.payload,
      };

    case "RESET_QUIZ":
      return {
        ...initialState,
      };

    default:
      return state;
  }
};

interface QuizContextType {
  state: QuizState;
  dispatch: Dispatch<QuizAction>;
}

const QuizContext = createContext<QuizContextType | undefined>(undefined);

export const QuizProvider = ({ children }: { children: ReactNode }) => {
  const [state, dispatch] = useReducer(quizReducer, initialState);

  return (
    <QuizContext.Provider value={{ state, dispatch }}>
      {children}
    </QuizContext.Provider>
  );
};

export const useQuiz = () => {
  const context = useContext(QuizContext);

  if (!context) {
    throw new Error("useQuiz must be used within a QuizProvider");
  }

  return context;
};