import { useState } from "react";

interface GenerateQuizFormProps {
  onGenerate: (
    file: File | null,
    topic: string,
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
  const [topic, setTopic] = useState("");
  const [query, setQuery] = useState("");
  const [numberOfQuestions, setNumberOfQuestions] = useState(5);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    if (!topic.trim()) {
      alert("Please enter a topic name.");
      return;
    }

    if (!query.trim()) {
      alert("Please enter a question instruction.");
      return;
    }

    if (numberOfQuestions < 1 || numberOfQuestions > 20) {
      alert("Please enter a number between 1 and 20.");
      return;
    }

    await onGenerate(
      selectedFile,
      topic.trim(),
      query.trim(),
      numberOfQuestions
    );
  };

  return (
    <div className="upload-card">
      <h2>Step 2: Configure Quiz</h2>
      <p className="upload-subtext">
        Choose the topic focus, question style, and number of questions for the quiz.
      </p>

      {!selectedFile && (
        <div className="upload-subtext" style={{ marginBottom: "1rem" }}>
          No PDF uploaded — QuizMind AI will generate topic-based study content automatically.
        </div>
      )}

      <form onSubmit={handleSubmit} className="generate-form">
        <div className="form-group">
          <label htmlFor="topic">Topic Name</label>
          <input
            id="topic"
            type="text"
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
            placeholder="e.g. Data Mining"
          />
          <small>
            Used to focus the content source (PDF if uploaded, otherwise AI-generated study content)
          </small>
        </div>

        <div className="form-group">
          <label htmlFor="query">Question Instruction / Query</label>
          <input
            id="query"
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="e.g. Generate medium and hard conceptual + application-based MCQs on clustering and classification"
          />
          <small>Used to control question type, style, and difficulty</small>
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