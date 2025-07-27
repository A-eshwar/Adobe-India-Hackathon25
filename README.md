# 🎯 Adobe India Hackathon 2025
## 🔗 Connecting the Dots Challenge
Welcome to our submission for Adobe India Hackathon 2025, under the exciting “Connecting the Dots” problem statement! 🚀

This project tackles two core challenges focused on extracting and analyzing insights from complex PDF documents. Our mission: help users make sense of unstructured content across multiple documents — quickly, meaningfully, and at scale.

## 📘 What's Inside?
We’ve built two complementary tools:

## 🔹 Challenge 1a: PDF Processing Solution
"Extract meaningful structure from a single PDF document"

🧠 Extracts titles and headings using font analysis, formatting cues, and patterns

📄 Builds a structured outline (H1, H2, H3 style)

🗂 Outputs clean, human-readable JSON

🐳 Containerized using Docker for easy deployment

See full details → challenge-1a/README.md

## 🔹 Challenge 1b: Multi-Collection PDF Analysis
"Understand what matters most to a persona across multiple documents"

🤖 Reads input.json containing a persona + job to be done

📚 Analyzes multiple PDFs to extract relevant sections

🔍 Ranks content by semantic similarity using Sentence Transformers

🧾 Outputs a structured result.json with:

Top 10 ranked sections

Refined subsections

Metadata with timestamps and scores

See full details → challenge-1b/README.md

## 🧠 Tech Stack

Area	Tool

Language	Python 3.9

PDF Parsing	PyMuPDF (fitz)

NLP/Embedding	Sentence Transformers

Structure Logic	Regex + Heuristic Scoring

Containerization	Docker

## 🗂 Project Structure
```
├── challenge-1a/        
│   ├── pdf_extractor.py
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── input/
│   └── output/
├── challenge-1b/   
│   ├── persona_analyzer.py
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── input/
│   └── output/
└── README.md
 ```              

## 🏁 How to Run
Each challenge folder (challenge-1a/ and challenge-1b/) is fully self-contained with its own:

Dockerfile

input/ and output/ folders

Instructions in its own README

You can:

Run them independently

Chain them together for a full pipeline (e.g., structure with 1a → analyze with 1b)

## ✨ Why We Built This
PDFs are everywhere — whitepapers, manuals, research papers, reports — and they’re often too long and unstructured for fast consumption.

We wanted to give users:

✨ Clarity over chaos

🧠 Context that matters

🚀 Tools that adapt to who they are and what they need

Whether it’s a product manager seeking strategy insights, or a researcher finding relevant studies — this toolkit connects the dots.
