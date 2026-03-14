import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { BookOpen } from "lucide-react";
import { toast } from "react-toastify";

import FileUpload from "../components/upload/FileUpload";
import GenerateQuizForm from "../components/upload/GenerateQuizForm";
import { uploadAndGenerateMcqs } from "../services/api";

function UploadPage() {
  const navigate = useNavigate();

  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleFileChange = (file: File | null) => {
    setSelectedFile(file);
  };

  const handleGenerateQuiz = async (
    file: File,
    query: string,
    numberOfQuestions: number
  ) => {
    try {
      setIsLoading(true);

      const response = await uploadAndGenerateMcqs(file, query, numberOfQuestions);

      const questions = response.mcqs ?? [];

      if (!questions.length) {
        toast.error("No questions were generated. Please try a different PDF or topic.");
        return;
      }

      toast.success(`Quiz generated successfully with ${questions.length} questions!`);

      navigate("/quiz", {
        state: {
          questions,
          requestedCount: numberOfQuestions,
          sessionId: null,
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
          Upload a PDF, enter a topic, and instantly generate a personalized
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