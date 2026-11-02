# MP2: Data Processing API

This FastAPI application lets users upload CSV files, retrieve stored datasets, and process data using reusable modules from MP1. Processing supports column validation, numeric validation, duplicate removal, missing-value handling, and optional outlier removal. The API returns a processing report and stores the cleaned dataset in memory. Request logging records request IDs, status codes, and response times, and each response includes an X-Request-ID header. Three pytest tests verify uploading, processing and retrieval, and handling missing datasets.

Run the API with `python -m uvicorn main:app`, then open http://127.0.0.1:8000/docs.

Run the tests with `python -m pytest tests -v`.

Stored datasets are cleared when the server restarts.