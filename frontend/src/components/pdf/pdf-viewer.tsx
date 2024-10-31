import { useState, useEffect } from 'react';

interface PdfViewerProps {
  pdfId: string;
}

export const PdfViewer = ({ pdfId }: PdfViewerProps) => {
  const [error, setError] = useState<string | null>(null);
  const [key, setKey] = useState<string>('');

  useEffect(() => {
    // Reset error when pdfId changes
    setError(null);
    // Generate new key when pdfId changes
    setKey(`${pdfId}-${Date.now()}`);
  }, [pdfId]);

  const pdfUrl = `http://localhost:8000/pdf/download/${pdfId}?t=${Date.now()}`;

  return (
    <div className="w-full h-[800px] flex flex-col items-center gap-4 p-4">
      {error ? (
        <div className="text-red-500">{error}</div>
      ) : (
        <iframe
          src={pdfUrl}
          className="w-full h-full border rounded-lg shadow-lg"
          title="PDF Viewer"
          onError={() => setError("Failed to load PDF")}
          key={key}
        />
      )}
    </div>
  );
};
