import { useEffect, useState } from "react";
import { Card, CardBody, Button } from "@nextui-org/react";
import { Trash2, Eye } from "lucide-react";

interface PdfDocument {
  id: string;
  filename: string;
  upload_date: string;
}

interface PdfListProps {
  onSelectPdf: (pdfId: string) => void;
  refreshTrigger?: number;
}

interface PaginatedResponse {
  items: PdfDocument[];
  total: number;
  skip: number;
  limit: number;
}

export const PdfList = ({ onSelectPdf, refreshTrigger }: PdfListProps) => {
  const [pdfs, setPdfs] = useState<PdfDocument[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  const fetchPdfs = async () => {
    try {
      console.log("Fetching PDFs...");
      const response = await fetch("http://localhost:8000/pdf/list");
      const data: PaginatedResponse = await response.json();
      console.log("Received PDF data:", data);
      
      // Extract the items array from the paginated response
      setPdfs(data.items || []);
    } catch (error) {
      console.error("Error fetching PDFs:", error);
      setPdfs([]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleDelete = async (id: string) => {
    try {
      const response = await fetch(`http://localhost:8000/pdf/${id}`, {
        method: "DELETE",
      });

      if (response.ok) {
        setPdfs(pdfs.filter(pdf => pdf.id !== id));
      }
    } catch (error) {
      console.error("Error deleting PDF:", error);
    }
  };

  useEffect(() => {
    console.log("refreshTrigger changed:", refreshTrigger);
    fetchPdfs();
  }, [refreshTrigger]);

  if (isLoading) {
    return <div className="text-center p-4">Loading PDFs...</div>;
  }

  console.log("Rendering PDFs:", pdfs);

  return (
    <div className="space-y-4 p-4">
      {pdfs.length === 0 && (
        <div className="text-center text-gray-500">No PDFs uploaded yet</div>
      )}
      {pdfs.map((pdf) => (
        <Card key={pdf.id} className="w-full">
          <CardBody className="flex flex-row items-center justify-between p-4">
            <div className="flex-1">
              <h3 className="text-lg font-medium">{pdf.filename}</h3>
              <p className="text-sm text-gray-500">
                Uploaded: {new Date(pdf.upload_date).toLocaleDateString()}
              </p>
            </div>
            <div className="flex gap-2">
              <Button
                isIconOnly
                color="primary"
                aria-label="View PDF"
                onClick={() => onSelectPdf(pdf.id)}
              >
                <Eye className="w-4 h-4" />
              </Button>
              <Button
                isIconOnly
                color="danger"
                aria-label="Delete PDF"
                onClick={() => handleDelete(pdf.id)}
              >
                <Trash2 className="w-4 h-4" />
              </Button>
            </div>
          </CardBody>
        </Card>
      ))}
    </div>
  );
};
