from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .utils import summarize_text, classify_text, classify_with_confidence, analyze_sentiment, extract_keywords
from .views import summarize_view, classify_view, sentiment_view, keywords_view
from django.test import RequestFactory
import json


class TextSummarizationTestCase(TestCase):
    """Test cases for text summarization utility functions"""
    
    def test_summarize_text_basic(self):
        """Test basic text summarization"""
        text = "This is a test sentence. This is another test sentence. This is a third test sentence."
        summary = summarize_text(text, max_sentences=2)
        
        # Should return 2 sentences
        sentences = summary.split('. ')
        self.assertEqual(len(sentences), 2)
        # Check that summary contains some content from the original text
        self.assertTrue(len(summary) > 0)
        self.assertTrue(any(word in summary.lower() for word in ['test', 'sentence']))
    
    def test_summarize_text_with_stopwords(self):
        """Test summarization handles stopwords correctly"""
        text = "The quick brown fox jumps over the lazy dog. The fox is very fast. The dog is very slow."
        summary = summarize_text(text, max_sentences=1)
        
        # Should return at least one sentence
        self.assertTrue(len(summary) > 0)
        self.assertIn("fox", summary.lower())
    
    def test_summarize_text_empty(self):
        """Test summarization with empty text"""
        summary = summarize_text("", max_sentences=3)
        self.assertEqual(summary, "")
    
    def test_summarize_text_single_sentence(self):
        """Test summarization with single sentence"""
        text = "This is a single sentence."
        summary = summarize_text(text, max_sentences=3)
        self.assertEqual(summary, text)
    
    def test_summarize_text_max_sentences(self):
        """Test that max_sentences parameter is respected"""
        text = "First sentence. Second sentence. Third sentence. Fourth sentence. Fifth sentence."
        summary = summarize_text(text, max_sentences=3)
        
        # Count sentences (split by period and filter empty strings)
        sentences = [s.strip() for s in summary.split('.') if s.strip()]
        self.assertLessEqual(len(sentences), 3)


class TextSummarizationAPITestCase(APITestCase):
    """Test cases for text summarization API endpoints"""
    
    def test_summarize_api_success(self):
        """Test successful text summarization via API"""
        url = reverse('summarize')
        data = {
            'text': 'This is the first sentence. This is the second sentence. This is the third sentence.',
            'max_sentences': 2
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('summary', response.data)
        self.assertIn('max_sentences', response.data)
        self.assertEqual(response.data['max_sentences'], 2)
        
        # Check that summary is returned
        summary = response.data['summary']
        self.assertTrue(len(summary) > 0)
    
    def test_summarize_api_missing_text(self):
        """Test API error when text is missing"""
        url = reverse('summarize')
        data = {'max_sentences': 3}
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Text is required')
    
    def test_summarize_api_empty_text(self):
        """Test API error when text is empty"""
        url = reverse('summarize')
        data = {'text': '', 'max_sentences': 3}
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Text is required')
    
    def test_summarize_api_invalid_max_sentences(self):
        """Test API error when max_sentences is invalid"""
        url = reverse('summarize')
        data = {'text': 'Test text', 'max_sentences': 'invalid'}
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'max_sentences must be an integer')
    
    def test_summarize_api_default_max_sentences(self):
        """Test API uses default max_sentences when not provided"""
        url = reverse('summarize')
        data = {'text': 'First sentence. Second sentence. Third sentence. Fourth sentence.'}
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['max_sentences'], 3)  # Default value
    
    def test_summarize_api_query_params(self):
        """Test API accepts max_sentences as query parameter"""
        url = reverse('summarize')
        data = {'text': 'First sentence. Second sentence. Third sentence.'}
        params = {'max_sentences': 1}
        
        response = self.client.post(url, data, format='json', **{'QUERY_STRING': 'max_sentences=1'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['max_sentences'], 1)


class TextSummarizationViewTestCase(TestCase):
    """Test cases for text summarization view functions"""
    
    def setUp(self):
        self.factory = RequestFactory()
    
    def test_summarize_view_function(self):
        """Test the summarize_view function directly"""
        request = self.factory.post('/api/text-summary/', 
                                  data=json.dumps({'text': 'Test sentence.', 'max_sentences': 1}),
                                  content_type='application/json')
        
        response = summarize_view(request)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # For DRF responses, we can access data directly
        self.assertIn('summary', response.data)


class TextClassificationTestCase(TestCase):
    """Test cases for text classification utility functions"""
    
    def test_classify_text_basic(self):
        """Test basic text classification"""
        text = "Python and AI are transforming the world"
        category = classify_text(text)
        
        # Should return one of the expected categories
        expected_categories = ['Technology', 'Healthcare', 'Business', 'Education']
        self.assertIn(category, expected_categories)
    
    def test_classify_text_healthcare(self):
        """Test healthcare text classification"""
        text = "Hospitals are improving healthcare with new technologies"
        category = classify_text(text)
        self.assertEqual(category, 'Healthcare')
    
    def test_classify_text_technology(self):
        """Test technology text classification"""
        text = "Machine learning is a subset of AI"
        category = classify_text(text)
        self.assertEqual(category, 'Technology')
    
    def test_classify_text_education(self):
        """Test education text classification"""
        text = "Students are learning with online platforms"
        category = classify_text(text)
        self.assertEqual(category, 'Education')
    
    def test_classify_text_business(self):
        """Test business text classification"""
        text = "Stock markets are volatile"
        category = classify_text(text)
        self.assertEqual(category, 'Business')


class TextClassificationAPITestCase(APITestCase):
    """Test cases for text classification API endpoints"""
    
    def test_classify_api_success(self):
        """Test successful text classification via API"""
        url = reverse('classify')
        data = {
            'text': 'Python and AI are transforming the world',
            'top_k': 3
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('category', response.data)
        self.assertIn('top', response.data)
        
        # Check that category is returned
        category = response.data['category']
        expected_categories = ['Technology', 'Healthcare', 'Business', 'Education']
        self.assertIn(category, expected_categories)
        
        # Check that top classifications are returned
        top = response.data['top']
        self.assertTrue(len(top) > 0)
        self.assertIn('label', response.data['top'][0])
        self.assertIn('confidence', response.data['top'][0])
    
    def test_classify_api_missing_text(self):
        """Test API error when text is missing"""
        url = reverse('classify')
        data = {'top_k': 3}
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Text is required')
    
    def test_classify_api_empty_text(self):
        """Test API error when text is empty"""
        url = reverse('classify')
        data = {'text': '', 'top_k': 3}
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Text is required')
    
    def test_classify_api_invalid_top_k(self):
        """Test API error when top_k is invalid"""
        url = reverse('classify')
        data = {'text': 'Test text', 'top_k': 'invalid'}
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'top_k must be an integer')
    
    def test_classify_api_default_top_k(self):
        """Test API uses default top_k when not provided"""
        url = reverse('classify')
        data = {'text': 'Python and AI are transforming the world'}
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check that top classifications are returned with default top_k=3
        top = response.data['top']
        self.assertLessEqual(len(top), 3)


class SentimentAnalysisTestCase(TestCase):
    """Test cases for sentiment analysis utility functions"""
    
    def test_sentiment_positive(self):
        """Test positive sentiment analysis"""
        text = "I love this product! It's amazing and wonderful."
        sentiment = analyze_sentiment(text)
        
        self.assertEqual(sentiment['label'], 'positive')
        self.assertIn('scores', sentiment)
        self.assertIn('pos', sentiment['scores'])
        self.assertIn('neg', sentiment['scores'])
        self.assertIn('neu', sentiment['scores'])
        self.assertIn('compound', sentiment['scores'])
    
    def test_sentiment_negative(self):
        """Test negative sentiment analysis"""
        text = "I hate this product! It's terrible and awful."
        sentiment = analyze_sentiment(text)
        
        self.assertEqual(sentiment['label'], 'negative')
        self.assertIn('scores', sentiment)
    
    def test_sentiment_neutral(self):
        """Test neutral sentiment analysis"""
        text = "This is a product. It has features."
        sentiment = analyze_sentiment(text)
        
        self.assertEqual(sentiment['label'], 'neutral')
        self.assertIn('scores', sentiment)
    
    def test_sentiment_empty(self):
        """Test sentiment analysis with empty text"""
        sentiment = analyze_sentiment("")
        
        self.assertIn('label', sentiment)
        self.assertIn('scores', sentiment)
    
    def test_sentiment_scores_range(self):
        """Test that sentiment scores are within valid range"""
        text = "This is a test sentence with mixed emotions."
        sentiment = analyze_sentiment(text)
        
        scores = sentiment['scores']
        self.assertGreaterEqual(scores['pos'], 0.0)
        self.assertLessEqual(scores['pos'], 1.0)
        self.assertGreaterEqual(scores['neg'], 0.0)
        self.assertLessEqual(scores['neg'], 1.0)
        self.assertGreaterEqual(scores['neu'], 0.0)
        self.assertLessEqual(scores['neu'], 1.0)
        self.assertGreaterEqual(scores['compound'], -1.0)
        self.assertLessEqual(scores['compound'], 1.0)


class SentimentAnalysisAPITestCase(APITestCase):
    """Test cases for sentiment analysis API endpoints"""
    
    def test_sentiment_api_success(self):
        """Test successful sentiment analysis via API"""
        url = reverse('sentiment')
        data = {'text': 'I love this amazing product!'}
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('label', response.data)
        self.assertIn('scores', response.data)
        
        # Check that sentiment label is returned
        label = response.data['label']
        expected_labels = ['positive', 'negative', 'neutral']
        self.assertIn(label, expected_labels)
        
        # Check that scores are returned
        scores = response.data['scores']
        self.assertIn('pos', scores)
        self.assertIn('neg', scores)
        self.assertIn('neu', scores)
        self.assertIn('compound', scores)
    
    def test_sentiment_api_missing_text(self):
        """Test API error when text is missing"""
        url = reverse('sentiment')
        data = {}
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Text is required')
    
    def test_sentiment_api_empty_text(self):
        """Test API error when text is empty"""
        url = reverse('sentiment')
        data = {'text': ''}
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Text is required')
    
    def test_sentiment_api_positive_text(self):
        """Test sentiment API with positive text"""
        url = reverse('sentiment')
        data = {'text': 'This is wonderful and amazing!'}
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['label'], 'positive')
    
    def test_sentiment_api_negative_text(self):
        """Test sentiment API with negative text"""
        url = reverse('sentiment')
        data = {'text': 'This is terrible and awful!'}
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['label'], 'negative')


class KeywordExtractionTestCase(TestCase):
    """Test cases for keyword extraction utility functions"""
    
    def test_extract_keywords_basic(self):
        """Test basic keyword extraction"""
        text = "Machine learning and artificial intelligence are transforming technology. AI algorithms process data efficiently."
        keywords = extract_keywords(text, top_k=5)
        
        self.assertIsInstance(keywords, list)
        self.assertLessEqual(len(keywords), 5)
        self.assertTrue(len(keywords) > 0)
        
        # Check that keywords are strings
        for keyword in keywords:
            self.assertIsInstance(keyword, str)
            self.assertTrue(len(keyword) > 0)
    
    def test_extract_keywords_empty(self):
        """Test keyword extraction with empty text"""
        keywords = extract_keywords("", top_k=5)
        
        self.assertIsInstance(keywords, list)
        self.assertEqual(len(keywords), 0)
    
    def test_extract_keywords_single_word(self):
        """Test keyword extraction with single word"""
        text = "Technology"
        keywords = extract_keywords(text, top_k=3)
        
        self.assertIsInstance(keywords, list)
        self.assertTrue(len(keywords) > 0)
    
    def test_extract_keywords_top_k_parameter(self):
        """Test that top_k parameter is respected"""
        text = "Machine learning artificial intelligence deep learning neural networks computer vision natural language processing"
        keywords = extract_keywords(text, top_k=3)
        
        self.assertLessEqual(len(keywords), 3)
    
    def test_extract_keywords_default_top_k(self):
        """Test keyword extraction uses default top_k when not provided"""
        text = "Machine learning and AI are important technologies"
        keywords = extract_keywords(text)
        
        self.assertLessEqual(len(keywords), 10)  # Default is 10


class KeywordExtractionAPITestCase(APITestCase):
    """Test cases for keyword extraction API endpoints"""
    
    def test_keywords_api_success(self):
        """Test successful keyword extraction via API"""
        url = reverse('keywords')
        data = {
            'text': 'Machine learning and artificial intelligence are transforming technology. AI algorithms process data efficiently.',
            'top_k': 5
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('keywords', response.data)
        self.assertIn('top_k', response.data)
        
        # Check that keywords are returned
        keywords = response.data['keywords']
        self.assertIsInstance(keywords, list)
        self.assertTrue(len(keywords) > 0)
        self.assertLessEqual(len(keywords), 5)
        
        # Check that top_k is returned
        self.assertEqual(response.data['top_k'], 5)
    
    def test_keywords_api_missing_text(self):
        """Test API error when text is missing"""
        url = reverse('keywords')
        data = {'top_k': 5}
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Text is required')
    
    def test_keywords_api_empty_text(self):
        """Test API error when text is empty"""
        url = reverse('keywords')
        data = {'text': '', 'top_k': 5}
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Text is required')
    
    def test_keywords_api_invalid_top_k(self):
        """Test API error when top_k is invalid"""
        url = reverse('keywords')
        data = {'text': 'Test text', 'top_k': 'invalid'}
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'top_k must be an integer')
    
    def test_keywords_api_default_top_k(self):
        """Test API uses default top_k when not provided"""
        url = reverse('keywords')
        data = {'text': 'Machine learning and AI are important technologies'}
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['top_k'], 10)  # Default value
