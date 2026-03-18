# 🌐 Language Translation Tool — CodeAlpha AI Internship Task 1

A desktop GUI application for translating text between 20+ languages using Google Translate, built with Python + Tkinter.

## Features
- Translate between 20+ languages including Tamil, Hindi, Telugu, and more
- Auto-detect source language
- Swap source ↔ target language with one click
- Copy translation result to clipboard
- Clean dark-themed UI

## Setup & Run

```bash
# 1. Install dependency
pip install deep-translator

# 2. Run the app
python app.py
```

## How It Works
1. Enter text in the left box
2. Select source & target languages
3. Click **Translate**
4. Result appears in the right box

## Tech Stack
- **Python 3.x**
- **Tkinter** — built-in GUI library
- **deep-translator** — free Google Translate wrapper (no API key needed)

## Project Structure
```
CodeAlpha_LanguageTranslationTool/
├── app.py            # Main application
├── requirements.txt  # Dependencies
└── README.md
```
