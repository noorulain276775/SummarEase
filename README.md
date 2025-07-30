# SummarEase

SummarEase is a free and open-source Django web application designed to provide quick, reliable, and privacy-conscious text summarization and classification, all processed locally with no reliance on third-party AI APIs or cloud services.

This project showcases how to build intelligent text tools using Python NLP libraries and classic machine learning models, making it budget-friendly and secure for users who prefer data privacy and offline functionality.

---

## Features

- Paste or upload documents (TXT, PDF) to get instant text summaries
- Local text summarization using custom algorithms (frequency-based, extractive)
- Basic text classification based on custom-trained models (e.g., Technology, Healthcare, Education)
- Plans for sentiment analysis to detect positive, negative, and neutral tones
- Fast, cost-free, and offline processing — no internet connection required
- User-friendly Django REST API backend ready for integration with frontend frameworks like React.js
- Supports common document formats with PDF parsing
- Simple and responsive interface (React.js + TypeScript planned for frontend)

---

## Tech Stack

| Component        | Technology                  |
|------------------|-----------------------------|
| Backend          | Django REST Framework       |
| Text Processing  | Python NLP (NLTK, scikit-learn) |
| Machine Learning | Scikit-learn (Naive Bayes classifier) |
| File Parsing     | PyPDF2                      |
| Frontend         | React.js (TypeScript) planned |
| Environment      | Python 3.11+                |

---

## Getting Started

### Prerequisites

- Python 3.11 or higher
- Git
- pip (Python package installer)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/summarease.git
   cd summarease

2. Create and activate a virtual environment:
    
    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/macOS
    venv\Scripts\activate     # Windows

3. Install dependencies:

    ```bash
    pip install -r requirements.txt

4. Run Database Migration

    ```bash
    python manage.py migrate

5. Start the development server

    ```bash
    python manage.py runserver

## API Endpoints
    - POST /api/text-summary/ (NLTK)
    Send raw text or upload document to get a summary.

    - POST /api/classify-text/ (Scikit-Learn)
    Classify text into categories like Technology, Healthcare, Education.

    - (Future) POST /api/sentiment-analysis/
    Analyze the sentiment of a text snippet.