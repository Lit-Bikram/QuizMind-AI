import type { ChangeEvent } from "react";
import { FileText, Upload } from "lucide-react";

interface FileUploadProps {
  selectedFile: File | null;
  onFileSelect: (file: File | null) => void;
}

const FileUpload = ({ selectedFile, onFileSelect }: FileUploadProps) => {
  const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0] ?? null;

    if (file && file.type !== "application/pdf") {
      alert("Please upload a PDF file only.");
      return;
    }

    onFileSelect(file);
  };

  return (
    <div className="upload-card">
      <h2>Step 1: Upload Your Study Material</h2>
      <p className="upload-subtext">
        Upload a PDF document to extract content for question generation.
      </p>

      <label className="file-upload-box">
        <input type="file" accept="application/pdf" onChange={handleFileChange} />

        {selectedFile ? (
          <div className="file-preview">
            <FileText size={40} />
            <p className="file-name">{selectedFile.name}</p>
            <span className="file-size">
              {(selectedFile.size / (1024 * 1024)).toFixed(2)} MB
            </span>
            <small>Click to replace file</small>
          </div>
        ) : (
          <div className="file-placeholder">
            <Upload size={40} />
            <p>Click to upload or drag & drop PDF</p>
          </div>
        )}
      </label>
    </div>
  );
};

export default FileUpload;