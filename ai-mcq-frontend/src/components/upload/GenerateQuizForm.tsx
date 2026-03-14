import { useState } from "react";

interface GenerateQuizFormProps {
  onGenerate: (
    file: File,
    query: string,
    numberOfQuestions: number
  ) => Promise<void> | void;
  selectedFile: File | null;
  isLoading?: boolean;
}

const GenerateQuizForm = ({
  onGenerate,
  selectedFile,
  isLoading = false,
}: GenerateQuizFormProps) => {
  const [query, setQuery] = useState("");
  const [numberOfQuestions, setNumberOfQuestions] = useState(5);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    if (!selectedFile) {
      alert("Please upload a PDF first.");
      return;
    }

    if (!query.trim()) {
      alert("Please enter a topic or query.");
      return;
    }

    if (numberOfQuestions < 1 || numberOfQuestions > 20) {
      alert("Please enter a number between 1 and 20.");
      return;
    }

    await onGenerate(selectedFile, query.trim(), numberOfQuestions);
  };

  return (
    <div className="upload-card">
      <h2>Step 2: Configure Quiz</h2>
      <p className="upload-subtext">
        Choose the topic and how many questions you want in the quiz.
      </p>

      <form onSubmit={handleSubmit} className="generate-form">
        <div className="form-group">
          <label htmlFor="query">Topic / Query</label>
          <input
            id="query"
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="e.g. What are the key findings of the paper?"
          />
        </div>

        <div className="form-group">
          <label htmlFor="numQuestions">Number of Questions</label>
          <input
            id="numQuestions"
            type="number"
            min={1}
            max={20}
            value={numberOfQuestions}
            onChange={(e) => setNumberOfQuestions(Number(e.target.value))}
          />
          <small>Choose between 1 and 20 questions</small>
        </div>

        <button
          type="submit"
          className="primary-btn full-width"
          disabled={isLoading}
        >
          {isLoading ? "Generating..." : "Generate Quiz"}
        </button>
      </form>
    </div>
  );
};

export default GenerateQuizForm;