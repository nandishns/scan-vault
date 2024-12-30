### **Documentation**
---
**Objective:**  
Develop a robust backend service to **scan files**, extract **sensitive data** (PII, PHI, PCI), and classify it using a combination of **Machine Learning (ML) models**, **regex-based patterns**, and **LLMs (ChatGPT)**. The service must:
- Handle various file formats (e.g., PDF, TXT, DOCX, CSV, Images).
- Extract and classify structured and unstructured data.
- Store scanned results in a database (e.g., Firestore).
- Provide APIs for scanning and retrieving scan results.

---

## **2. Approach**

**Core Approach:**
1. **File Processing:**  
   - Process files in-memory to extract readable content.
   - Use LLMs for text extraction and classification from various file formats.
   
2. **Hybrid Classification Logic:**
   - **Readable/Structured Data:** Use a combination of pre-trained NER models (e.g., spaCy) and regex for entity extraction.
   - **Unstructured/Unreadable Data:** Use an LLM (e.g., GPT-4 via OpenAI API) for classification via prompt engineering.

3. **Data Persistence:**  
   - Store the file metadata and extracted sensitive data in Firestore for future retrieval.

4. **Endpoints:**  
   - **/scan:** Upload a file for scanning.
   - **/get-scans:** Retrieve scan results based on filters (e.g., file name).

---

## **System Design Diagram**
![image](https://github.com/user-attachments/assets/bd124a80-67b6-448d-924b-2b80891853a0)

## **Class Diagram**
![image](https://github.com/user-attachments/assets/8ad6a33b-c203-41bd-bb30-093e563263dd)

## **3. Tech Stack**

### **Backend Framework:**
- **FastAPI:** For developing the REST API.

### **Data Processing:**
- **pdfplumber:** Extract text from PDFs.
- **pytesseract:** Perform OCR on image-based content.
- **pandas:** Handle CSV files.

### **Machine Learning:**
- **spaCy:** Pre-trained NER model for sensitive data extraction.
- **OpenAI GPT-4 API:** For unstructured data classification.

### **Database:**
- **Google Firestore:** Store scan results to handle crud operations on them

### **Deployment & Testing:**
- **Docker:** Containerize the application.
- **Pytest:** Unit and integration tests for endpoints and core logic.
---

## **4. Codebase Structure**

### **Directory Layout**
```plaintext
scan_vault-server/
├── src/
│   ├── __init__.py
│   ├── main.py                  # Entry point for FastAPI app
│   ├── server/
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── scan_request.py      # Request models for endpoints
│   │   │   ├── scan_result.py       # Response models
│   │   │   ├── model_handler.py     # ML model schemas and configurations
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── scan.py              # Scan-related API routes
│   │   │   ├── delete_detection.py  # Delete scan detection routes
│   │   │   ├── get_detection.py     # Get scan detection routes
│   │   │   ├── save_detection.py    # Save scan detection routes
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── scan_service.py      # File processing and scanning logic
│   │   │   ├── model_handler.py     # spaCy-based ML model logic
│   │   │   ├── file_handler.py      # File upload and processing utilities
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── firestore.py         # Firestore client and helper methods
│   │   ├── logger.py            # Centralized logging
├── tests/
│   ├── test_scan.py             # Unit tests for scan logic
├── requirements.txt             # Python dependencies
├── Dockerfile                   # Docker configuration
├── docker-compose.yml           # Orchestration for app + database
├── .env                         # Environment variables
├── .gitignore                   # Git ignore file
├── serviceAccount.json          # Firebase service account key                  

scan_vault-client/
├── .next/                       # Next.js build output
├── app/                         # App router pages
├── components/                  # React components
├── hooks/                       # Custom React hooks
├── lib/                        # Utility functions
├── node_modules/               # Node.js dependencies
├── public/                     # Static assets
├── services/                   # API service layers
├── .eslintrc.json             # ESLint configuration
├── .gitignore                 # Git ignore file
├── components.json            # Component configurations
├── next-env.d.ts             # Next.js TypeScript declarations
├── next.config.ts            # Next.js configuration
├── package-lock.json         # Locked dependencies
├── package.json              # Project dependencies
├── postcss.config.mjs        # PostCSS configuration
├── README.md                 # Documentation
├── tailwind.config.ts        # Tailwind CSS configuration
└── tsconfig.json             # TypeScript configuration

└── README.md 
```

---

## **5. Code Structures**

### **Classes and Design Patterns**
1. **`ScanService`:**  
   - Handles file processing, text extraction, and sensitive data classification.
   - Implements the **Strategy Pattern** to switch between regex+NER and LLM-based classification.

2. **`ModelHandler`:**  
   - Encapsulates logic for spaCy NER predictions and entity classification.

3. **`FirestoreClient`:**  
   - Provides a reusable interface for storing and retrieving data from Firestore.

4. **API Router (`scan.py`):**  
   - Defines REST endpoints, delegating processing to `ScanService`.

---

## **6. How to Set Up**

### **1. Clone the Repository**
```bash
git clone https://github.com/nandishns/scan-vault/
cd scan-vault
```

### **2. Server Setup**
1. **Navigate to server directory:**
   ```bash
   cd scan_vault-server
   ```

2. **Set up Python environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure environment variables:**
   - Create a `.env` file in the server directory:
   ```bash
   SCAN_VAULT_API_KEY=your_api_key
   OPENAI_API_KEY=your_openai_key
   ```

4. **Start the server:**
   ```bash
   uvicorn src.main:app --reload
   ```
   The server will run on `http://localhost:8000`

### **3. Client Setup**
1. **Navigate to client directory:**
   ```bash
   cd scan_vault-client
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Configure environment variables:**
   - Create a `.env.local` file in the client directory:
   ```bash
   ACCESS_TOKEN=your_access_token
   ```

4. **Start the development server:**
   ```bash
   npm run dev
   ```
   The client will run on `http://localhost:3000`

### **4. Docker Setup (Optional)**
To run the entire application using Docker:

```bash
# Build and run the server
cd scan_vault-server
docker build -t fastapi-scan-app .
docker run -d -p 8000:8000 --name scan-app fastapi-scan-app

# Build and run the client
cd ../scan_vault-client
docker build -t nextjs-scan-app .
docker run --env-file .env.production -p 3000:3000 scan-vault-client
```

### **5. Test the Application**
- Run server tests:
  ```bash
  cd scan_vault-server
  pytest tests/
  ```

- Run client tests:
  ```bash
  cd scan_vault-client
  npm run test
  ```

---

## **7. Testing Coverage**

### **Unit Tests**
1. **`test_scan.py`:**
   - Validate file processing logic for all supported file types (PDF, DOCX, etc.).
   - Ensure `_scan_content` combines regex and NER correctly.

2. **`test_model_handler.py`:**
   - Validate spaCy model predictions.
   - Test `get_category` classification for PII, PHI, PCI.

### **Integration Tests**
1. **`test_endpoints.py`:**
   - Test `/scan` endpoint with various file types.
   - Test `/get-scans` retrieval logic.

### **Mock Testing**
- Mock `Firestore` and `OpenAI API` to validate database and API interactions without external dependencies.

---

## **8. Conclusion**

This project demonstrates backend engineering best practices:
- **Hybrid Approach:** Combines regex, ML models, and LLMs for flexible and accurate data extraction.
- **Scalable Architecture:** Modular codebase with database integration (Firestore) and containerization.
- **Testing Coverage:** Ensures reliability and maintainability.
