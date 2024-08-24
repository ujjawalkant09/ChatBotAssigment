# Basic Chat-Bot

This is a basic chatbot application integrated with OpenAI's GPT-3.5-turbo on the backend.

## Setup Instructions

### Prerequisites

- Make sure to create a `.env` file and provide your OpenAI API key as `OPENAI_API_KEY`.

### Local Setup

1. **Using Docker:**
   - Clone the repository.
   - Run the application using Docker by executing:
     ```bash
     docker-compose up --build
     ```

2. **Manual Setup:**

   **Frontend:**
   - Clone the repository.
   - Navigate to the frontend directory.
   - Install the required dependencies:
     ```bash
     npm install
     ```
   - Run the frontend using:
     ```bash
     npm start
     ```

   **Backend:**
   - Create a virtual environment:
     ```bash
     python3 -m venv env
     source env/bin/activate
     ```
   - Install the required libraries:
     ```bash
     pip install -r req_be.txt
     ```
   - Run the backend server:
     ```bash
     uvicorn main:app --reload
     ```

