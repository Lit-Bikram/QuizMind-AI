import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { BookOpen } from "lucide-react";
import { toast } from "react-toastify";
import FileUpload from "../components/upload/FileUpload";
import GenerateQuizForm from "../components/upload/GenerateQuizForm";
import { createQuizSession, uploadAndGenerateMcqs } from "../services/api";
import type { QuizQuestion } from "../types/quiz";

function UploadPage() {
  const navigate = useNavigate();
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleFileChange = (file: File | null) => {
    setSelectedFile(file);
  };

  // Normalize option labels so frontend always has:
  // A, B, C, D in the same order as displayed
  const normalizeQuestions = (questions: QuizQuestion[]): QuizQuestion[] => {
    return questions.map((question) => ({
      ...question,
      options: question.options.map((option, index) => ({
        ...option,
        label: String.fromCharCode(65 + index), // A, B, C, D
      })),
    }));
  };

  const handleGenerateQuiz = async (
    file: File | null,
    topic: string,
    query: string,
    numberOfQuestions: number
  ) => {
    try {
      setIsLoading(true);

      const response = await uploadAndGenerateMcqs(
        file,
        topic,
        query,
        numberOfQuestions
      );

      const generatedQuestions = response.mcqs ?? [];

      if (!generatedQuestions.length) {
        toast.error("No questions were generated. Please try a different topic or PDF.");
        return;
      }

      const sessionResponse = await createQuizSession({
        query,
        original_filename: response.original_filename,
        mcqs: generatedQuestions,
      });

      const normalizedQuestions = normalizeQuestions(sessionResponse.mcqs ?? []);

      toast.success(`Quiz generated successfully with ${normalizedQuestions.length} questions!`);

      navigate("/quiz", {
        state: {
          questions: normalizedQuestions,
          requestedCount: numberOfQuestions,
          sessionId: sessionResponse.session_id,
          topic,
          query,
          contentSource: response.content_source,
        },
      });
    } catch (error: any) {
      console.error("Error generating quiz:", error);

      const backendMessage =
        error?.response?.data?.detail ||
        error?.response?.data?.message ||
        "Failed to generate quiz. Please try again.";

      toast.error(
        typeof backendMessage === "string"
          ? backendMessage
          : "Failed to generate quiz. Please check your input and try again."
      );
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="page-container">
      <div className="hero-section">
        <div className="hero-icon">
          <BookOpen size={32} />
        </div>

        <h1>AI MCQ Generator</h1>

        <p>
          Upload a PDF (optional), enter a topic, and generate a personalized
          multiple-choice quiz with AI.
        </p>
      </div>

      <div className="upload-grid">
        <FileUpload selectedFile={selectedFile} onFileSelect={handleFileChange} />

        <GenerateQuizForm
          selectedFile={selectedFile}
          onGenerate={handleGenerateQuiz}
          isLoading={isLoading}
        />
      </div>
    </div>
  );
}

export default UploadPage;