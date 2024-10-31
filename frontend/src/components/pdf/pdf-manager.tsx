'use client';

import { useState } from "react";
import { PdfUpload } from "./pdf-upload";
import { PdfList } from "./pdf-list";
import { PdfViewer } from "./pdf-viewer";

export const PdfManager = () => {
  const [selectedPdfId, setSelectedPdfId] = useState<string | null>(null);
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  const handlePdfSelect = (pdfId: string) => {
    setSelectedPdfId(pdfId);
  };

  const handleUploadSuccess = () => {
    console.log("Upload success triggered");
    setRefreshTrigger(prev => prev + 1);
  };

  return (
    <div className="container mx-auto p-4">
      <div className="grid grid-cols-1 md:grid-cols-[300px_1fr] gap-6">
        <div className="space-y-6 bg-white p-4 rounded-lg shadow">
          <PdfUpload onUploadSuccess={handleUploadSuccess} />
          <PdfList onSelectPdf={handlePdfSelect} refreshTrigger={refreshTrigger} />
        </div>
        <div className="min-h-[600px] bg-white rounded-lg shadow">
          {selectedPdfId ? (
            <PdfViewer pdfId={selectedPdfId} />
          ) : (
            <div className="flex items-center justify-center h-full text-gray-500">
              Select a PDF to view
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
