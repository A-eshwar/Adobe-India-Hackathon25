# 🚀 Challenge 1a: PDF Processing Solution
Hey there! 👋
This project is built for Adobe India Hackathon 2025 – Challenge 1a and is all about making sense of PDF documents by pulling out titles and headings into a structured JSON. It's smart, fast, and runs smoothly in Docker!

# 💡 What It Does
🧠 Understands PDF structure by analyzing fonts, styles, and heading patterns

🔍 Detects meaningful section titles like "Introduction", "Results", or "Chapter 3"

🏷 Extracts the document title from the top of the first pages

🧾 Outputs a clean JSON showing the document's outline

🐳 Fully containerized – run it anywhere without setup headaches!

🗂 Folder Structure
```
├── pdf_extractor.py
├── Dockerfile 
├── /input
└── /output     
```
# ⚙ How to Use It (The Easy Way: Docker)
## 1. 🔨 Build the Image

docker build -t pdf-outline-extractor 
## 2. 📥 Add PDFs
Put all your PDFs inside a folder called input in the project root.

## 3. 🚀 Run the Extractor
```
docker run --rm \
  -v "$(pwd)/input":/app/input \
  -v "$(pwd)/output":/app/output \
  pdf-outline-extractor
```
  
That’s it! You’ll find beautifully structured JSON files waiting in the output/ folder.

# 🧪 Example Output
Here’s a peek at what you’ll get:

json
```
{
  "title": "Understanding AI Ethics",
  "outline": [
    {
      "level": "H1",
      "text": "Introduction",
      "page": 1
    },
    {
      "level": "H2",
      "text": "The Rise of AI",
      "page": 2
    }
  ]
}
```
# 🧰 Want to Run Locally?
Make sure you’ve got Python 3.9 installed, then:

bash

pip install -r requirements.txt

python pdf_extractor.py

Just make sure you’ve got /input and /output folders created in the root!

