"""
CodeAlpha Internship - Task 2: Chatbot for FAQs
Uses NLP (TF-IDF + cosine similarity) to match user questions to FAQs.
Install: pip install nltk scikit-learn colorama
"""

import nltk
import string
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from colorama import Fore, Style, init
import numpy as np

# ── Download NLTK data (first run only) ──────────────────────────────────────
nltk.download("punkt", quiet=True)
nltk.download("punkt_tab", quiet=True)
nltk.download("stopwords", quiet=True)
nltk.download("wordnet", quiet=True)

init(autoreset=True)  # Colorama

# ── FAQ Dataset ───────────────────────────────────────────────────────────────
# Topic: College / Education FAQ (you can swap this for any domain)
FAQ_DATA = [
    {
        "question": "What is artificial intelligence?",
        "answer": "Artificial Intelligence (AI) is the simulation of human intelligence in machines that are programmed to think, learn, and solve problems like humans.",
    },
    {
        "question": "What is machine learning?",
        "answer": "Machine Learning is a subset of AI where algorithms learn from data to make predictions or decisions without being explicitly programmed.",
    },
    {
        "question": "What is deep learning?",
        "answer": "Deep Learning is a subset of machine learning that uses neural networks with many layers (deep networks) to learn complex patterns from large amounts of data.",
    },
    {
        "question": "What is a neural network?",
        "answer": "A neural network is a computational model inspired by the human brain, consisting of interconnected nodes (neurons) organized in layers that process information.",
    },
    {
        "question": "What is natural language processing?",
        "answer": "NLP (Natural Language Processing) is a field of AI that enables computers to understand, interpret, and generate human language.",
    },
    {
        "question": "What is computer vision?",
        "answer": "Computer Vision is an AI field that enables computers to interpret and understand visual information from images and videos.",
    },
    {
        "question": "What is the difference between AI and machine learning?",
        "answer": "AI is the broader concept of machines performing tasks intelligently. Machine Learning is a specific approach within AI where machines learn from data.",
    },
    {
        "question": "What programming languages are used in AI?",
        "answer": "Python is the most popular language for AI, followed by R, Java, and Julia. Python dominates due to its rich ecosystem of libraries like TensorFlow, PyTorch, and scikit-learn.",
    },
    {
        "question": "What is TensorFlow?",
        "answer": "TensorFlow is an open-source deep learning framework developed by Google, widely used for building and training machine learning models.",
    },
    {
        "question": "What is PyTorch?",
        "answer": "PyTorch is an open-source deep learning framework developed by Facebook/Meta, popular for research due to its dynamic computation graphs.",
    },
    {
        "question": "What is overfitting in machine learning?",
        "answer": "Overfitting occurs when a model learns the training data too well, including noise, causing it to perform poorly on new, unseen data.",
    },
    {
        "question": "What is a training dataset?",
        "answer": "A training dataset is the data used to teach a machine learning model. The model learns patterns from this data to make predictions.",
    },
    {
        "question": "What is a test dataset?",
        "answer": "A test dataset is a separate set of data used to evaluate the final performance of a trained machine learning model.",
    },
    {
        "question": "What is supervised learning?",
        "answer": "Supervised learning is a type of ML where the model is trained on labeled data — each input has a corresponding correct output.",
    },
    {
        "question": "What is unsupervised learning?",
        "answer": "Unsupervised learning trains models on unlabeled data, where the algorithm finds hidden patterns or groupings on its own.",
    },
    {
        "question": "What is reinforcement learning?",
        "answer": "Reinforcement learning is a type of ML where an agent learns by interacting with an environment and receiving rewards or penalties for actions.",
    },
    {
        "question": "What is a large language model?",
        "answer": "A Large Language Model (LLM) is an AI model trained on massive text data to understand and generate human-like text. Examples include GPT-4 and Claude.",
    },
    {
        "question": "What is ChatGPT?",
        "answer": "ChatGPT is a conversational AI developed by OpenAI, based on the GPT (Generative Pre-trained Transformer) architecture.",
    },
    {
        "question": "How do I start learning AI?",
        "answer": "Start with Python basics, then learn libraries like NumPy and Pandas. Take online courses on ML (Coursera, edX), and practice on datasets from Kaggle.",
    },
    {
        "question": "What is Kaggle?",
        "answer": "Kaggle is an online platform for data science and ML competitions, providing datasets, notebooks, and a community for learning AI.",
    },
    {
        "question": "What is a confusion matrix?",
        "answer": "A confusion matrix is a table used to evaluate a classification model's performance, showing true/false positives and negatives.",
    },
    {
        "question": "What is accuracy in machine learning?",
        "answer": "Accuracy is a metric measuring the percentage of correctly predicted instances out of all predictions made by the model.",
    },
    {
        "question": "What is gradient descent?",
        "answer": "Gradient Descent is an optimization algorithm used to minimize the loss function of a model by iteratively adjusting weights in the direction of steepest descent.",
    },
    {
        "question": "goodbye",
        "answer": "Goodbye! Thanks for chatting. Good luck with your AI journey! 👋",
    },
    {
        "question": "hello",
        "answer": "Hello! 👋 I'm your AI FAQ Chatbot. Ask me anything about Artificial Intelligence!",
    },
    {
        "question": "who are you",
        "answer": "I'm an AI FAQ Chatbot built for the CodeAlpha AI Internship. I can answer questions about AI, ML, and deep learning!",
    },
]

# ── Text Preprocessor ─────────────────────────────────────────────────────────
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words("english"))

def preprocess(text: str) -> str:
    """Lowercase, remove punctuation, tokenize, remove stopwords, lemmatize."""
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", "", text)
    tokens = word_tokenize(text)
    tokens = [lemmatizer.lemmatize(t) for t in tokens if t not in stop_words]
    return " ".join(tokens)

# ── Build TF-IDF Index ────────────────────────────────────────────────────────
questions = [faq["question"] for faq in FAQ_DATA]
answers   = [faq["answer"]   for faq in FAQ_DATA]
processed_questions = [preprocess(q) for q in questions]

vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(processed_questions)

# ── Response Function ─────────────────────────────────────────────────────────
THRESHOLD = 0.15  # Minimum similarity to return a match

def get_response(user_input: str) -> str:
    processed_input = preprocess(user_input)
    if not processed_input.strip():
        return "I didn't quite catch that. Could you rephrase?"

    input_vec = vectorizer.transform([processed_input])
    similarities = cosine_similarity(input_vec, tfidf_matrix).flatten()
    best_idx = int(np.argmax(similarities))
    best_score = similarities[best_idx]

    if best_score < THRESHOLD:
        return (
            "🤔 I'm not sure about that. Try asking something related to AI, "
            "machine learning, or deep learning!"
        )
    return answers[best_idx]

# ── Chat UI (Terminal) ────────────────────────────────────────────────────────
def chat():
    print(Fore.CYAN + Style.BRIGHT + "=" * 60)
    print(Fore.CYAN + "  🤖 AI FAQ Chatbot — CodeAlpha AI Internship Task 2")
    print(Fore.CYAN + "=" * 60)
    print(Fore.YELLOW + "  Ask me anything about AI, ML, or Deep Learning!")
    print(Fore.YELLOW + "  Type 'quit' or 'exit' to stop.\n")

    while True:
        try:
            user_input = input(Fore.GREEN + "You: " + Style.RESET_ALL).strip()
        except (EOFError, KeyboardInterrupt):
            print(Fore.RED + "\n\nSession ended.")
            break

        if not user_input:
            continue

        if user_input.lower() in {"quit", "exit", "bye", "goodbye"}:
            print(Fore.MAGENTA + "Bot: " + get_response("goodbye"))
            break

        response = get_response(user_input)
        print(Fore.MAGENTA + "Bot: " + Style.RESET_ALL + response + "\n")


if __name__ == "__main__":
    chat()
