import { Routes, Route } from "react-router-dom";
import UploadPage from "../pages/UploadPage";
import QuizPage from "../pages/QuizPage";
import ResultsPage from "../pages/ResultsPage";

function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<UploadPage />} />
      <Route path="/quiz" element={<QuizPage />} />
      <Route path="/results" element={<ResultsPage />} />
    </Routes>
  );
}

export default AppRoutes;