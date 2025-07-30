import nltk
import nltk.data
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import defaultdict
from .text_classifier_model import text_classifier

nltk.download('punkt')
nltk.download('stopwords')

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