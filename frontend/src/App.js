import React from 'react';
import './App.css';
import TextAnalysis from './components/TextAnalysis';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>SummarEase</h1>
        <p>AI-Powered Text Analysis & Summarization</p>
      </header>
      <main>
        <TextAnalysis />
      </main>
    </div>
  );
}

export default App;
