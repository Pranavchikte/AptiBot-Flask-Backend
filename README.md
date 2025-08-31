# AptiBot - Conversational AI Aptitude Tutor (Backend)

AptiBot is a smart, conversational AI tutor designed to help students prepare for aptitude tests and competitive exams. This repository contains the complete Flask backend that powers the application.



---

## Features

-   **Conversational Memory**: Remembers the context of the chat to answer follow-up questions.
-   **Multi-Format Input**: Solves problems from text, PDF, Word documents, and images (OCR).
-   **Accurate Math Solving**: Uses a hybrid Gemini + SymPy engine to ensure mathematical accuracy.
-   **Friendly Persona**: Acts as an encouraging "Friendly Professor" to guide students.
-   **Secure & Robust**: Includes error handling and file size limits for stability.

---

## Tech Stack

-   **Framework**: Flask
-   **Language**: Python
-   **AI**: Google Gemini Pro & Google Cloud Vision API
-   **Math Engine**: SymPy

---

## Setup and Installation

Follow these steps to run the project locally.

1.  **Clone the Repository**
    ```bash
    git clone <your-repo-url>
    cd aptibot_backend
    ```

2.  **Create and Activate a Virtual Environment**
    ```bash
    python -m venv venv
    # On Windows:
    .\venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set Up Environment Variables**
    * Create a file named `.env` in the root directory.
    * Add your Gemini API key: `GEMINI_API_KEY='your_key_here'`

5.  **Set Up Google Cloud Credentials**
    * Follow the Google Cloud Vision setup guide to get your service account JSON key.
    * Place the file in the root directory and name it `gcloud_credentials.json`.

---

## Running the Application

```bash
python run.py
```
The server will start on `http://127.0.0.1:5000`.

---

## API Endpoints

### 1. Create a New Session

-   **URL**: `/api/sessions`
-   **Method**: `POST`
-   **Description**: Starts a new conversation.
-   **Success Response**: `{"session_id": "unique-session-id"}`

### 2. Send a Message (Text or File)

-   **URL**: `/api/sessions/<session_id>/messages`
-   **Method**: `POST`
-   **Description**: The main endpoint for all interactions. Can handle both text and file uploads.

-   **For Text Messages**:
    -   **Headers**: `Content-Type: application/json`
    -   **Body**: `{"query": "What is 5 + 5?"}`

-   **For File Uploads**:
    -   **Headers**: `Content-Type: multipart/form-data`
    -   **Body**: Key `file` with the uploaded file as the value.

-   **Success Response**: `{"solution": "The detailed explanation from the AI..."}`