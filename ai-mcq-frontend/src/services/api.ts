import axios from "axios";
import type {
  GenerateQuizResponse,
  QuizCreateRequest,
  QuizCreateResponse,
  QuizResult,
  SubmitQuizRequest,
} from "../types/quiz";

const api = axios.create({
  baseURL: "http://localhost:8000",
});

export const uploadAndGenerateMcqs = async (
  file: File,
  topic: string,
  query: string,
  numQuestions: number
): Promise<GenerateQuizResponse> => {
  const formData = new FormData();

  formData.append("file", file);
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
  payload: QuizCreateRequest
): Promise<QuizCreateResponse> => {
  const response = await api.post<QuizCreateResponse>(
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