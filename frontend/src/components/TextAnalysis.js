import React, { useState } from 'react';
import axios from 'axios';
import './TextAnalysis.css';

const TextAnalysis = () => {
  const [inputText, setInputText] = useState('');
  const [summary, setSummary] = useState('');
  const [classification, setClassification] = useState('');
  const [sentiment, setSentiment] = useState('');
  const [keywords, setKeywords] = useState([]);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('summary');
  const [maxSentences, setMaxSentences] = useState(3);
  const [topK, setTopK] = useState(10);

  const handleSummarize = async () => {
    if (!inputText.trim()) return;
    
    setLoading(true);
    try {
      console.log('Sending request to:', '/api/text-summary/');
      console.log('Request data:', { text: inputText, max_sentences: maxSentences });
      
      const response = await axios.post('/api/text-summary/', {
        text: inputText,
        max_sentences: maxSentences
      });
      
      console.log('Response received:', response.data);
      setSummary(response.data.summary);
      setActiveTab('summary');
    } catch (error) {
      console.error('Error summarizing text:', error);
      console.error('Error details:', {
        message: error.message,
        response: error.response?.data,
        status: error.response?.status
      });
      
      let errorMessage = 'Error occurred while summarizing text.';
      if (error.response?.data?.error) {
        errorMessage = `API Error: ${error.response.data.error}`;
      } else if (error.message) {
        errorMessage = `Network Error: ${error.message}`;
      }
      
      setSummary(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const handleClassify = async () => {
    if (!inputText.trim()) return;
    
    setLoading(true);
    try {
      const response = await axios.post('/api/classify-text/', {
        text: inputText,
        top_k: 3
      });
      setClassification(response.data);
      setActiveTab('classification');
    } catch (error) {
      console.error('Error classifying text:', error);
      setClassification('Error occurred while classifying text.');
    } finally {
      setLoading(false);
    }
  };

  const handleSentiment = async () => {
    if (!inputText.trim()) return;
    
    setLoading(true);
    try {
      const response = await axios.post('/api/sentiment/', {
        text: inputText
      });
      setSentiment(response.data);
      setActiveTab('sentiment');
    } catch (error) {
      console.error('Error analyzing sentiment:', error);
      setSentiment('Error occurred while analyzing sentiment.');
    } finally {
      setLoading(false);
    }
  };

  const handleKeywords = async () => {
    if (!inputText.trim()) return;
    
    setLoading(true);
    try {
      const response = await axios.post('/api/keywords/', {
        text: inputText,
        top_k: topK
      });
      setKeywords(response.data.keywords);
      setActiveTab('keywords');
    } catch (error) {
      console.error('Error extracting keywords:', error);
      setKeywords([]);
    } finally {
      setLoading(false);
    }
  };

  const handleAnalyzeAll = async () => {
    if (!inputText.trim()) return;
    
    setLoading(true);
    try {
      await Promise.all([
        handleSummarize(),
        handleClassify(),
        handleSentiment(),
        handleKeywords()
      ]);
    } catch (error) {
      console.error('Error in analysis:', error);
    } finally {
      setLoading(false);
    }
  };

  const clearResults = () => {
    setSummary('');
    setClassification('');
    setSentiment('');
    setKeywords([]);
    setInputText('');
  };

  return (
    <div className="text-analysis">
      <div className="input-section">
        <div className="input-controls">
          <div className="control-group">
            <label>Max Sentences:</label>
            <input
              type="number"
              min="1"
              max="10"
              value={maxSentences}
              onChange={(e) => setMaxSentences(parseInt(e.target.value))}
            />
          </div>
          <div className="control-group">
            <label>Top Keywords:</label>
            <input
              type="number"
              min="1"
              max="20"
              value={topK}
              onChange={(e) => setTopK(parseInt(e.target.value))}
            />
          </div>
        </div>
        
        <textarea
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          placeholder="Enter your text here... (or paste from any source)"
          rows="8"
          className="text-input"
        />
        
        <div className="action-buttons">
          <button 
            onClick={handleAnalyzeAll} 
            disabled={loading || !inputText.trim()}
            className="analyze-all-btn"
          >
            {loading ? 'Analyzing...' : 'Analyze All'}
          </button>
          <button onClick={clearResults} className="clear-btn">
            Clear All
          </button>
        </div>
        
        <div className="individual-actions">
          <button 
            onClick={handleSummarize} 
            disabled={loading || !inputText.trim()}
          >
            Summarize
          </button>
          <button 
            onClick={handleClassify} 
            disabled={loading || !inputText.trim()}
          >
            Classify
          </button>
          <button 
            onClick={handleSentiment} 
            disabled={loading || !inputText.trim()}
          >
            Sentiment
          </button>
          <button 
            onClick={handleKeywords} 
            disabled={loading || !inputText.trim()}
          >
            Keywords
          </button>
        </div>
      </div>

      <div className="results-section">
        <div className="tabs">
          <button 
            className={`tab ${activeTab === 'summary' ? 'active' : ''}`}
            onClick={() => setActiveTab('summary')}
          >
            Summary
          </button>
          <button 
            className={`tab ${activeTab === 'classification' ? 'active' : ''}`}
            onClick={() => setActiveTab('classification')}
          >
            Classification
          </button>
          <button 
            className={`tab ${activeTab === 'sentiment' ? 'active' : ''}`}
            onClick={() => setActiveTab('sentiment')}
          >
            Sentiment
          </button>
          <button 
            className={`tab ${activeTab === 'keywords' ? 'active' : ''}`}
            onClick={() => setActiveTab('keywords')}
          >
            Keywords
          </button>
        </div>

        <div className="tab-content">
          {activeTab === 'summary' && (
            <div className="result-content">
              <h3>Text Summary</h3>
              {summary ? (
                <div className="summary-result">
                  <p>{summary}</p>
                </div>
              ) : (
                <p className="no-result">No summary generated yet. Click "Summarize" to analyze your text.</p>
              )}
            </div>
          )}

          {activeTab === 'classification' && (
            <div className="result-content">
              <h3>Text Classification</h3>
              {classification && typeof classification === 'object' ? (
                <div className="classification-result">
                  <div className="primary-category">
                    <h4>Primary Category: {classification.category}</h4>
                  </div>
                  {classification.top && classification.top.length > 0 && (
                    <div className="top-categories">
                      <h4>Top Categories:</h4>
                      <ul>
                        {classification.top.map((item, index) => (
                          <li key={index}>
                            <strong>{item.label}</strong>: {(item.confidence * 100).toFixed(1)}%
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              ) : (
                <p className="no-result">No classification result yet. Click "Classify" to analyze your text.</p>
              )}
            </div>
          )}

          {activeTab === 'sentiment' && (
            <div className="result-content">
              <h3>Sentiment Analysis</h3>
              {sentiment && typeof sentiment === 'object' ? (
                <div className="sentiment-result">
                  <div className="sentiment-label">
                    <h4>Overall Sentiment: {sentiment.label}</h4>
                  </div>
                  <div className="sentiment-scores">
                    <h4>Detailed Scores:</h4>
                    <ul>
                      <li><strong>Positive:</strong> {(sentiment.scores.pos * 100).toFixed(1)}%</li>
                      <li><strong>Neutral:</strong> {(sentiment.scores.neu * 100).toFixed(1)}%</li>
                      <li><strong>Negative:</strong> {(sentiment.scores.neg * 100).toFixed(1)}%</li>
                      <li><strong>Compound:</strong> {(sentiment.scores.compound * 100).toFixed(1)}%</li>
                    </ul>
                  </div>
                </div>
              ) : (
                <p className="no-result">No sentiment analysis yet. Click "Sentiment" to analyze your text.</p>
              )}
            </div>
          )}

          {activeTab === 'keywords' && (
            <div className="result-content">
              <h3>Keyword Extraction</h3>
              {keywords && keywords.length > 0 ? (
                <div className="keywords-result">
                  <h4>Top Keywords:</h4>
                  <div className="keywords-list">
                    {keywords.map((keyword, index) => (
                      <div key={index} className="keyword-item">
                        <span className="keyword-term">{keyword}</span>
                        <span className="keyword-rank">#{index + 1}</span>
                      </div>
                    ))}
                  </div>
                </div>
              ) : (
                <p className="no-result">No keywords extracted yet. Click "Keywords" to analyze your text.</p>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default TextAnalysis;
