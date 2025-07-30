import nltk
import nltk.data
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import defaultdict

nltk.download('punkt')
nltk.download('stopwords')

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

def summarize_text(text, max_sentences=3):
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
    summary = ' '.join(ranked_sentences[:max_sentences])
    return summary
