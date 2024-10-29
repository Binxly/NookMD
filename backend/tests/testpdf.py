import pytest
from fastapi.testclient import TestClient
import os


def test_pdf_upload_and_retrieve(client: TestClient):
    # Create a test PDF file
    test_file_path = "test.pdf"
    test_content = b"%PDF-1.4\n%Test PDF file"
    with open(test_file_path, "wb") as f:
        f.write(test_content)

    try:
        # Test PDF upload
        with open(test_file_path, "rb") as f:
            response = client.post(
                "/pdf/upload", files={"file": ("test.pdf", f, "application/pdf")}
            )
        assert response.status_code == 200
        pdf_data = response.json()
        assert "id" in pdf_data
        assert "filename" in pdf_data
        assert "path" in pdf_data
        assert "uploaded_at" in pdf_data
        assert pdf_data["filename"] == "test.pdf"
        pdf_id = pdf_data["id"]

        # Test get PDF info
        response = client.get(f"/pdf/{pdf_id}")
        assert response.status_code == 200
        pdf_info = response.json()
        assert pdf_info["id"] == pdf_id
        assert pdf_info["filename"] == "test.pdf"
        assert "path" in pdf_info
        assert "uploaded_at" in pdf_info

        # Test list PDFs with pagination
        response = client.get("/pdf/list?skip=0&limit=10")
        assert response.status_code == 200
        pdf_list = response.json()
        assert "items" in pdf_list
        assert "total" in pdf_list
        assert "skip" in pdf_list
        assert "limit" in pdf_list
        assert pdf_list["total"] > 0
        assert len(pdf_list["items"]) > 0
        assert any(pdf["id"] == pdf_id for pdf in pdf_list["items"])

        # Test PDF download
        response = client.get(f"/pdf/download/{pdf_id}")
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/pdf"
        assert response.content == test_content

    finally:  # cleanup
        if os.path.exists(test_file_path):
            os.remove(test_file_path)


def test_pdf_not_found(client: TestClient):
    # Test non-existent PDF info
    response = client.get("/pdf/999999")
    assert response.status_code == 404
    assert response.json()["detail"] == "PDF not found"

    # Test non-existent PDF download
    response = client.get("/pdf/download/999999")
    assert response.status_code == 404
    assert response.json()["detail"] == "PDF not found"


def test_invalid_file_upload(client: TestClient):
    # Test non-PDF file upload
    test_file_path = "test.txt"
    with open(test_file_path, "w") as f:
        f.write("This is not a PDF file")

    try:
        with open(test_file_path, "rb") as f:
            response = client.post(
                "/pdf/upload", files={"file": ("test.txt", f, "text/plain")}
            )
        assert response.status_code == 400
        assert "Invalid file type" in response.json()["detail"]

    finally:
        if os.path.exists(test_file_path):
            os.remove(test_file_path)


def test_pagination_limits(client: TestClient):
    # Test pagination limits
    response = client.get("/pdf/list?skip=0&limit=101")
    assert response.status_code == 422  # FastAPI validation error

    response = client.get("/pdf/list?skip=-1")
    assert response.status_code == 422  # FastAPI validation error

    response = client.get("/pdf/list?limit=0")
    assert response.status_code == 422  # FastAPI validation error


def test_large_file_upload(client: TestClient):
    """Test that large files (>50MB) are rejected with a proper error message"""
    test_file_path = "large.pdf"
    large_content = b"%PDF-1.4\n" + b"0" * (51 * 1024 * 1024)  # 51MB

    try:
        with open(test_file_path, "wb") as f:
            f.write(large_content)

        with open(test_file_path, "rb") as f:
            response = client.post(
                "/pdf/upload", files={"file": ("large.pdf", f, "application/pdf")}
            )
        assert response.status_code == 413  # Request Entity Too Large
        assert "File size exceeds" in response.json()["detail"]

    finally:
        if os.path.exists(test_file_path):
            os.remove(test_file_path)
