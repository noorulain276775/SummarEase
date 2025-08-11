import nltk
import nltk.data
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import defaultdict
from .text_classifier_model import text_classifier
from nltk.sentiment import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import TfidfVectorizer

nltk.download('punkt')
nltk.download('stopwords')
# Download sentiment lexicon for VADER
nltk.download('vader_lexicon')

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')


def summarize_text(text, max_sentences=3):
    """Returns Summary of the text"""
    sentences = tokenizer.tokenize(text)
    stop_words = set(stopwords.words('english'))
    
    word_freq = defaultdict(int)
    for sent in sentences:
        words = word_tokenize(sent.lower())
        for word in words:
            if word.isalpha() and word not in stop_words:
                word_freq[word] += 1
                
    sentence_scores = defaultdict(int)
    for sent in sentences:
        for word in word_tokenize(sent.lower()):
            if word in word_freq:
                sentence_scores[sent] += word_freq[word]
                
    ranked_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)
    print(ranked_sentences)
    summary = ' '.join(ranked_sentences[:max_sentences])
    return summary



def classify_text(text):
    """Returns predicted category for the given text"""
    prediction = text_classifier.predict([text])[0]
    return prediction

# New helpers
_vader_analyzer = SentimentIntensityAnalyzer()


def analyze_sentiment(text: str):
    """Return sentiment scores and label using NLTK VADER."""
    scores = _vader_analyzer.polarity_scores(text)
    compound = scores.get('compound', 0.0)
    if compound >= 0.05:
        label = 'positive'
    elif compound <= -0.05:
        label = 'negative'
    else:
        label = 'neutral'
    return {
        'label': label,
        'scores': scores,
    }


def extract_keywords(text: str, top_k: int = 10):
    """Extract top keywords/keyphrases using TF-IDF on the single document."""
    vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2), max_features=5000)
    tfidf_matrix = vectorizer.fit_transform([text])
    feature_names = vectorizer.get_feature_names_out()
    scores = tfidf_matrix.toarray()[0]
    ranked_indices = scores.argsort()[::-1]
    keywords = []
    for idx in ranked_indices[:top_k]:
        term = feature_names[idx]
        score = float(scores[idx])
        if score > 0:
            keywords.append({'term': term, 'score': score})
    return keywords


def classify_with_confidence(text: str, top_k: int = 3):
    """Return top-k labels with probabilities using the existing classifier."""
    try:
        proba = text_classifier.predict_proba([text])[0]
        # If using a Pipeline, classes_ live on the final estimator
        classes = getattr(text_classifier, 'classes_', None)
        if classes is None and hasattr(text_classifier, 'steps'):
            try:
                classes = text_classifier.named_steps[list(text_classifier.named_steps.keys())[-1]].classes_
            except Exception:
                classes = []
        if not classes:
            # Try to get from estimator_ attribute
            classes = getattr(getattr(text_classifier, 'estimator', None), 'classes_', [])
        pairs = list(zip(list(classes), list(proba)))
        pairs.sort(key=lambda x: x[1], reverse=True)
        top = [{'label': label, 'confidence': float(prob)} for label, prob in pairs[:top_k]]
        return top
    except Exception:
        label = text_classifier.predict([text])[0]
        return [{'label': label, 'confidence': 1.0}]