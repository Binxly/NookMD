import { useState, useRef } from "react";
import { Button } from "@nextui-org/react";
import { Upload } from "lucide-react";

interface UploadResponse {
  success: boolean;
  message: string;
  filename?: string;
}

interface PdfUploadProps {
  onUploadSuccess?: () => void;
}

export const PdfUpload = ({ onUploadSuccess }: PdfUploadProps) => {
  const [isUploading, setIsUploading] = useState(false);
  const [feedback, setFeedback] = useState<{ type: 'success' | 'error', message: string } | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleButtonClick = () => {
    fileInputRef.current?.click();
  };

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    try {
      setIsUploading(true);
      setFeedback(null);
      const formData = new FormData();
      formData.append("file", file);

      const response = await fetch("http://localhost:8000/pdf/upload", {
        method: "POST",
        body: formData,
      });

      const data: UploadResponse = await response.json();
      
      if (!response.ok) {
        throw new Error(data.message || "Upload failed");
      }
      
      setFeedback({ type: 'success', message: 'PDF uploaded successfully!' });
      onUploadSuccess?.();
    } catch (error) {
      console.error("Upload error:", error);
      setFeedback({ 
        type: 'error', 
        message: error instanceof Error ? error.message : 'Failed to upload PDF' 
      });
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="w-full max-w-md mx-auto p-4">
      <input
        ref={fileInputRef}
        type="file"
        accept=".pdf"
        onChange={handleFileUpload}
        className="hidden"
        aria-label="Upload PDF file"
      />
      <Button
        isLoading={isUploading}
        startContent={<Upload className="w-4 h-4" />}
        className="w-full"
        color="primary"
        aria-label="Upload PDF"
        onClick={handleButtonClick}
      >
        {isUploading ? "Uploading..." : "Upload PDF"}
      </Button>
      {feedback && (
        <div className={`mt-2 p-2 rounded ${
          feedback.type === 'success' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'
        }`}>
          {feedback.message}
        </div>
      )}
    </div>
  );
};
