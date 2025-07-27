# 🧠 Challenge 1b: Multi-Collection PDF Analysis
Hey there! 👋

This is our solution for Adobe India Hackathon 2025 – Challenge 1b, and it’s built to do one thing really well: help a persona make sense of multiple PDFs like a pro. Whether you're a UX researcher, product manager, or analyst — this tool pulls out the most relevant insights just for you.

🚀 What This Tool Can Do

🔍 Reads through lots of PDFs

🧠 Understands the user persona and their goal/task

🪄 Picks out the most important sections

📊 Gives back a beautiful, structured JSON with:

✅ Top 10 ranked sections

🧩 Refined subsections (digestible chunks of content)

📌 Metadata with full transparency

No fluff, just focused insights tailored to who you are and what you’re trying to do.

📁 How the Project is Structured
```
Challenge_1b/
├── Collection 1/                    # Travel Planning
│   ├── PDFs/                       # South of France guides
│   ├── challenge1b_input.json      # Input configuration
│   └── challenge1b_output.json     # Analysis results
├── Collection 2/                    # Adobe Acrobat Learning
│   ├── PDFs/                       # Acrobat tutorials
│   ├── challenge1b_input.json      # Input configuration
│   └── challenge1b_output.json     # Analysis results
├── Collection 3/                    # Recipe Collection
│   ├── PDFs/                       # Cooking guides
│   ├── challenge1b_input.json      # Input configuration
│   └── challenge1b_output.json     # Analysis results
└── README.md
```          
# 🐳 Run It Like a Pro (in Docker)
1️⃣ Build the Image
```
docker build -t pdf-analyzer .
```

2️⃣ Add Your Inputs
Inside the input/ folder:

Drop your PDF files (e.g., doc1.pdf, doc2.pdf)

Create an input.json like this:
```
{
  "persona": { "role": "UX Researcher" },
  "job_to_be_done": { "task": "analyze user behavior reports" },
  "documents": [
    { "filename": "doc1.pdf" },
    { "filename": "doc2.pdf" }
  ]
}
```

3️⃣ Run It!
```
docker run --rm \
  -v "$(pwd)/input":/app/input \
  -v "$(pwd)/output":/app/output \
  pdf-analyzer
```

🎉 You'll find the results in output/result.json

# 🔎 A Glimpse at the Output
```
{
  "metadata": {
    "input_documents": ["doc1.pdf", "doc2.pdf"],
    "persona": "UX Researcher",
    "job": "analyze user behavior reports",
    "sections_selected": 10,
    "timestamp": "2025-07-26T18:30:00Z"
  },
  "sections": [
    {
      "document": "doc1.pdf",
      "page_number": 3,
      "section_title": "Behavioral Patterns",
      "importance_rank": 1,
      "relevance_score": 0.9271
    }
  ],
  "subsections": [
    {
      "document": "doc1.pdf",
      
      "page_number": 3,
      
      "refined_text": "Most users consistently chose feature A over B, suggesting..."
      
    }
  ]
}
```
# 🧠 What’s Under the Hood
Python 3.9

PyMuPDF (fitz) for extracting text with style

SentenceTransformers for semantic matching magic

Regex & heuristics for heading detection

Docker to make life easier

# ✨ Why We Built This

Because PDFs are long, messy, and a pain to scan — especially when you’re trying to find the stuff that matters to you.

We wanted to build something that thinks like a human, filters like a machine, and delivers insights fast. Mission accomplished. ✅
# 🧠 Challenge 1b: Multi-Collection PDF Analysis
Hey there! 👋

This is our solution for Adobe India Hackathon 2025 – Challenge 1b, and it’s built to do one thing really well: help a persona make sense of multiple PDFs like a pro. Whether you're a UX researcher, product manager, or analyst — this tool pulls out the most relevant insights just for you.

🚀 What This Tool Can Do

🔍 Reads through lots of PDFs

🧠 Understands the user persona and their goal/task

🪄 Picks out the most important sections

📊 Gives back a beautiful, structured JSON with:

✅ Top 10 ranked sections

🧩 Refined subsections (digestible chunks of content)

📌 Metadata with full transparency

No fluff, just focused insights tailored to who you are and what you’re trying to do.

📁 How the Project is Structured
```
Challenge_1b/
├── Collection 1/                    # Travel Planning
│   ├── PDFs/                       # South of France guides
│   ├── challenge1b_input.json      # Input configuration
│   └── challenge1b_output.json     # Analysis results
├── Collection 2/                    # Adobe Acrobat Learning
│   ├── PDFs/                       # Acrobat tutorials
│   ├── challenge1b_input.json      # Input configuration
│   └── challenge1b_output.json     # Analysis results
├── Collection 3/                    # Recipe Collection
│   ├── PDFs/                       # Cooking guides
│   ├── challenge1b_input.json      # Input configuration
│   └── challenge1b_output.json     # Analysis results
└── README.md
```          
# 🐳 Run It Like a Pro (in Docker)
1️⃣ Build the Image

docker build -t pdf-analyzer .

2️⃣ Add Your Inputs
Inside the input/ folder:

Drop your PDF files (e.g., doc1.pdf, doc2.pdf)

Create an input.json like this:

{
  "persona": { "role": "UX Researcher" },
  "job_to_be_done": { "task": "analyze user behavior reports" },
  "documents": [
    { "filename": "doc1.pdf" },
    { "filename": "doc2.pdf" }
  ]
}

3️⃣ Run It!
```
docker run --rm \
  -v "$(pwd)/input":/app/input \
  -v "$(pwd)/output":/app/output \
  pdf-analyzer
```

🎉 You'll find the results in output/result.json

# 🔎 A Glimpse at the Output
```
{
  "metadata": {
    "input_documents": ["doc1.pdf", "doc2.pdf"],
    "persona": "UX Researcher",
    "job": "analyze user behavior reports",
    "sections_selected": 10,
    "timestamp": "2025-07-26T18:30:00Z"
  },
  "sections": [
    {
      "document": "doc1.pdf",
      "page_number": 3,
      "section_title": "Behavioral Patterns",
      "importance_rank": 1,
      "relevance_score": 0.9271
    }
  ],
  "subsections": [
    {
      "document": "doc1.pdf",
      
      "page_number": 3,
      
      "refined_text": "Most users consistently chose feature A over B, suggesting..."
      
    }
  ]
}
```
# 🧠 What’s Under the Hood
Python 3.9

PyMuPDF (fitz) for extracting text with style

SentenceTransformers for semantic matching magic

Regex & heuristics for heading detection

Docker to make life easier

# ✨ Why We Built This

Because PDFs are long, messy, and a pain to scan — especially when you’re trying to find the stuff that matters to you.

We wanted to build something that thinks like a human, filters like a machine, and delivers insights fast. Mission accomplished. ✅
