# SummarEase

A comprehensive AI-powered text analysis and summarization web application built with Django REST Framework and React.js.

## Features

### Text Summarization
- Intelligent text summarization using frequency-based algorithms
- Configurable maximum sentence count (1-10 sentences)
- Handles various text lengths and formats
- Optimized for academic, business, and general content

### Text Classification
- Multi-category text classification using machine learning
- Pre-trained model covering Technology, Business, Healthcare, and Education
- Confidence scoring for classification results
- Top-k classification results with accuracy metrics

### Sentiment Analysis
- Advanced sentiment analysis using VADER (Valence Aware Dictionary and sEntiment Reasoner)
- Multi-dimensional sentiment scoring (Positive, Negative, Neutral, Compound)
- Real-time sentiment detection and analysis
- Suitable for social media, reviews, and general text analysis

### Keyword Extraction
- TF-IDF based keyword extraction algorithm
- Configurable top-k keywords (1-20 keywords)
- Intelligent filtering of stop words and common terms
- Support for both single words and key phrases

## Tech Stack

### Backend
- **Django 5.2.4** - Web framework
- **Django REST Framework 3.16.0** - API development
- **Python 3.13** - Programming language
- **NLTK 3.8.1** - Natural language processing
- **Scikit-learn 1.5.1** - Machine learning algorithms
- **SQLite** - Database (default Django database)

### Frontend
- **React 18.2.0** - User interface library
- **Axios** - HTTP client for API communication
- **CSS3** - Styling with modern design patterns
- **Responsive Design** - Mobile and desktop compatible

### NLP Libraries
- **NLTK** - Tokenization, stopwords, sentence segmentation
- **VADER** - Sentiment analysis
- **TF-IDF Vectorizer** - Keyword extraction
- **Naive Bayes Classifier** - Text classification

## Project Structure

```
SummarEase/
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── README.md                # Project documentation
├── summarease_project/      # Django project settings
│   ├── __init__.py
│   ├── settings.py          # Django configuration
│   ├── urls.py             # Main URL routing
│   ├── asgi.py             # ASGI configuration
│   └── wsgi.py             # WSGI configuration
├── summarizer/              # Main Django app
│   ├── __init__.py
│   ├── admin.py            # Admin interface
│   ├── apps.py             # App configuration
│   ├── models.py           # Database models
│   ├── views.py            # API view functions
│   ├── urls.py             # API URL patterns
│   ├── utils.py            # NLP utility functions
│   ├── text_classifier_model.py  # ML model training
│   └── tests.py            # Comprehensive test suite
└── frontend/                # React frontend application
    ├── package.json         # Node.js dependencies
    ├── public/              # Static files
    ├── src/                 # React source code
    │   ├── App.js          # Main application component
    │   ├── App.css         # Main application styles
    │   ├── index.js        # React entry point
    │   ├── components/     # React components
    │   │   ├── TextAnalysis.js    # Main analysis component
    │   │   └── TextAnalysis.css  # Component styles
    │   └── index.css       # Global styles
    └── .gitignore          # Git ignore rules
```

## API Endpoints

### Text Summarization
- **POST** `/api/text-summary/`
- **Parameters**: `text` (required), `max_sentences` (optional, default: 3)
- **Response**: Summary text and configuration

### Text Classification
- **POST** `/api/classify-text/`
- **Parameters**: `text` (required), `top_k` (optional, default: 3)
- **Response**: Primary category and top classifications with confidence scores

### Sentiment Analysis
- **POST** `/api/sentiment/`
- **Parameters**: `text` (required)
- **Response**: Sentiment label and detailed scores (positive, negative, neutral, compound)

### Keyword Extraction
- **POST** `/api/keywords/`
- **Parameters**: `text` (required), `top_k` (optional, default: 10)
- **Response**: List of extracted keywords and top_k value

## Getting Started

### Prerequisites
- Python 3.8 or higher
- Node.js 14 or higher
- npm or yarn package manager

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd SummarEase
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

5. **Start Django server**
   ```bash
   python manage.py runserver
   ```

The backend will be available at `http://127.0.0.1:8000/`

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install Node.js dependencies**
   ```bash
   npm install
   ```

3. **Start React development server**
   ```bash
   npm start
   ```

The frontend will be available at `http://localhost:3000/`

## Testing

### Backend Tests
Run comprehensive test suite for all NLP features:
```bash
python manage.py test summarizer.tests -v 2
```

### API Testing
Test individual API endpoints:
```bash
python test_apis.py
```

## Usage

1. **Open the application** in your browser at `http://localhost:3000/`
2. **Enter or paste text** in the textarea
3. **Choose analysis type**:
   - Click individual buttons for specific analysis
   - Use "Analyze All" for comprehensive analysis
4. **View results** in the tabbed interface
5. **Adjust parameters** using the control inputs (max sentences, top keywords)

## Configuration

### Django Settings
- CORS enabled for frontend communication
- REST Framework configured for JSON responses
- Debug mode enabled for development

### Frontend Configuration
- Proxy configured to `http://127.0.0.1:8000`
- Axios for API communication
- Responsive design with modern UI components

## Development

### Adding New Features
1. Implement backend logic in `summarizer/utils.py`
2. Create API view in `summarizer/views.py`
3. Add URL pattern in `summarizer/urls.py`
4. Implement frontend component in React
5. Add comprehensive tests

### Code Quality
- Comprehensive test coverage for all features
- Error handling and validation
- Clean code structure and documentation
- Responsive and accessible UI design

## License

This project is open source and available under the MIT License.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## Support

For issues and questions, please check the existing issues or create a new one in the repository.