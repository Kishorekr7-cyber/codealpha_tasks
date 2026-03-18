# 🤖 FAQ Chatbot — CodeAlpha AI Internship Task 2

An NLP-powered chatbot that answers frequently asked questions about Artificial Intelligence using TF-IDF and cosine similarity.

## Features
- 25+ built-in AI/ML FAQs
- Text preprocessing: tokenization, stopword removal, lemmatization (NLTK)
- Smart matching using TF-IDF vectorization + cosine similarity (scikit-learn)
- Threshold-based fallback for unknown questions
- Colorful terminal chat interface

## Setup & Run

```bash
# 1. Install dependencies
pip install nltk scikit-learn colorama numpy

# 2. Run the chatbot
python chatbot.py
```

## Example Interaction
```
You: What is machine learning?
Bot: Machine Learning is a subset of AI where algorithms learn from data...

You: how to learn AI
Bot: Start with Python basics, then learn libraries like NumPy and Pandas...
```

## How It Works
1. FAQ questions are preprocessed using NLTK (tokenize → remove stopwords → lemmatize)
2. TF-IDF converts all questions into numeric vectors
3. User input is transformed the same way
4. Cosine similarity finds the most relevant FAQ
5. If similarity < threshold, a fallback message is shown

## Tech Stack
- **Python 3.x**
- **NLTK** — NLP preprocessing
- **scikit-learn** — TF-IDF + cosine similarity
- **NumPy** — array operations
- **colorama** — colored terminal output

## Customizing FAQs
Edit the `FAQ_DATA` list in `chatbot.py` to add your own questions and answers for any domain (product support, university, etc.)

## Project Structure
```
CodeAlpha_ChatbotFAQ/
├── chatbot.py        # Main chatbot script
├── requirements.txt  # Dependencies
└── README.md
```
