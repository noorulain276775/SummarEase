"""
Basic custom text classification model trainer using scikit-learn pipeline.

This script demonstrates training a simple text classification model
that categorizes input texts into predefined labels such as 'Technology',
'Healthcare', 'Business', and 'Education'. It uses the TF-IDF vectorizer
to convert text data into numeric features and the Multinomial Naive Bayes
algorithm as the classifier.

Components:
- TfidfVectorizer: Converts raw text to a matrix of TF-IDF features.
- MultinomialNB: Probabilistic classifier suited for discrete features like word counts.

Training data:
- `training_texts`: List of example text samples.
- `training_labels`: Corresponding category labels for each text sample.

Usage:
- Fit the model with training data using `text_classifier.fit(training_texts, training_labels)`.
- Use `text_classifier.predict(new_texts)` to predict categories for new texts.

Note:
- This is a basic example intended for educational purposes and may need
  additional data and tuning for production use.

"""
from sklearn.pipeline import make_pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

training_texts = [
    "Python and AI are transforming the world",
    "Hospitals are improving healthcare with new technologies",
    "Stock markets are volatile",
    "Students are learning with online platforms",
    "Teachers are using smart boards in education",
    "Machine learning is a subset of AI",
    "Patients are receiving better care"
]

training_labels = [
    "Technology",
    "Healthcare",
    "Business",
    "Education",
    "Education",
    "Technology",
    "Healthcare"
]

text_classifier = make_pipeline(
    TfidfVectorizer(),
    MultinomialNB()
)
text_classifier.fit(training_texts, training_labels)