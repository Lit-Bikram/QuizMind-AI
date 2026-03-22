import axios from "axios";
import type {
  CreateQuizSessionRequest,
  CreateQuizSessionResponse,
  GenerateQuizResponse,
  QuizResult,
  SubmitQuizRequest,
} from "../types/quiz";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export const api = axios.create({
  baseURL: API_BASE_URL,
});

export const uploadAndGenerateMcqs = async (
  file: File | null,
  topic: string,
  query: string,
  numQuestions: number
): Promise<GenerateQuizResponse> => {
  const formData = new FormData();

  if (file) {
    formData.append("file", file);
  }

  formData.append("topic", topic);
  formData.append("query", query);
  formData.append("num_questions", String(numQuestions));

  const response = await api.post<GenerateQuizResponse>(
    "/api/v1/documents/upload-and-generate-mcqs",
    formData,
    {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    }
  );

  return response.data;
};

export const createQuizSession = async (
  payload: CreateQuizSessionRequest
): Promise<CreateQuizSessionResponse> => {
  const response = await api.post<CreateQuizSessionResponse>(
    "/api/v1/quiz/quiz/create",
    payload
  );

  return response.data;
};

export const submitQuiz = async (
  payload: SubmitQuizRequest
): Promise<QuizResult> => {
  const response = await api.post<QuizResult>("/api/v1/quiz/quiz/submit", payload);

  return response.data;
};

export default api;