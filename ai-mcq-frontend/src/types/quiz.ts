export type DifficultyLevel = "easy" | "medium" | "hard" | string;

export interface QuizOption {
  label: string;
  text: string;
}

export interface QuizQuestion {
  id?: string;
  question_id?: string;
  question: string;
  options: QuizOption[];
  correct_answer: string; // backend returns label like "A", "B"
  difficulty: DifficultyLevel;
  explanation?: string;
  confidence_score?: number;
  is_verified?: boolean;
  verification_notes?: string[];
}

export interface GenerateQuizResponse {
  message: string;
  original_filename: string;
  saved_path: string;
  num_pages: number;
  text_length: number;
  topic?: string;
  query: string;
  chunks_created: number;
  keyphrases: Array<{
    keyword: string;
    score: number;
  }>;
  focused_context: string;
  mcqs: QuizQuestion[];
}

export interface QuizCreateRequest {
  query: string;
  original_filename: string;
  mcqs: QuizQuestion[];
}

export interface QuizCreateResponse {
  message: string;
  session_id: string;
  query: string;
  original_filename: string;
  total_questions: number;
  mcqs: QuizQuestion[];
}

export interface SubmitQuizRequest {
  session_id: string;
  answers: Record<string, string>; // question_id -> selected option label
}

export interface DifficultyStats {
  total: number;
  correct: number;
  accuracy?: number;
}

export interface QuestionReview {
  question_id: string;
  question: string;
  user_answer: string;
  correct_answer: string;
  is_correct: boolean;
  difficulty: string;
  explanation?: string;
  confidence_score?: number;
  is_verified?: boolean;
}

export interface QuizResult {
  message: string;
  session_id: string;
  total_questions: number;
  correct_count: number;
  incorrect_count: number;
  percentage: number;
  difficulty_breakdown: Record<string, DifficultyStats>;
  question_reviews: QuestionReview[];
  weak_areas: string[];
}