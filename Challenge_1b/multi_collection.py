import os
import json
import fitz  
from datetime import datetime
from sentence_transformers import SentenceTransformer, util
import re
from typing import List, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PersonaDrivenAnalyzer:
    def _init_(self, model_name='all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
        logger.info(f"Loaded model: {model_name}")

    def extract_sections_with_headings(self, pdf_path: str) -> List[Dict]:
        doc = fitz.open(pdf_path)
        sections = []

        for page_num in range(len(doc)):
            page = doc[page_num]
            blocks = page.get_text("dict")["blocks"]

            current_section = {
                "heading": "",
                "content": "",
                "page": page_num + 1,
                "document": os.path.basename(pdf_path)
            }

            for block in blocks:
                if "lines" in block:
                    block_text = ""
                    is_heading = False

                    for line in block["lines"]:
                        for span in line["spans"]:
                            text = span["text"].strip()
                            font_size = span["size"]
                            font_flags = span["flags"]

                            if (
                                font_flags & 16 or
                                font_size > 12 or
                                re.match(r'^\d+\.?\s+|^[A-Z][A-Z\s]{2,}$', text) or
                                any(k in text.lower() for k in ['chapter', 'section', 'introduction',
                                                               'conclusion', 'methodology', 'results'])
                            ):
                                is_heading = True

                            block_text += text + " "

                    block_text = block_text.strip()
                    if len(block_text) > 10:
                        if is_heading and len(block_text) < 200:
                            if current_section["content"].strip():
                                sections.append(current_section.copy())

                            current_section = {
                                "heading": block_text,
                                "content": "",
                                "page": page_num + 1,
                                "document": os.path.basename(pdf_path)
                            }
                        else:
                            current_section["content"] += block_text + "\n"

            if current_section["content"].strip():
                sections.append(current_section)

        doc.close()

        filtered_sections = []
        for section in sections:
            content = section["content"].strip()
            if len(content) > 50:
                section["content"] = re.sub(r'\s+', ' ', content)
                section["text"] = f"{section['heading']} {content}".strip()
                filtered_sections.append(section)

        return filtered_sections

    def rank_sections_by_relevance(self, sections: List[Dict], persona: str, job: str) -> List[Dict]:
        query = f"{persona} needs to {job}"
        section_texts = [f"{s['heading']} {s['content']}" for s in sections]

        if not section_texts:
            return []

        logger.info(f"Encoding {len(section_texts)} sections")
        section_embeddings = self.model.encode(section_texts, convert_to_tensor=True)
        query_embedding = self.model.encode(query, convert_to_tensor=True)

        similarities = util.pytorch_cos_sim(query_embedding, section_embeddings)[0]

        for i, section in enumerate(sections):
            section["relevance_score"] = float(similarities[i])

        return sorted(sections, key=lambda x: -x["relevance_score"])

    def extract_subsections(self, section: Dict) -> List[Dict]:
        content = section["content"]
        paragraphs = content.split('\n')
        subsections = []

        for para in paragraphs:
            para = para.strip()
            if len(para) > 100:
                subsections.append({
                    "document": section["document"],
                    "page_number": section["page"],
                    "refined_text": para
                })

        if not subsections and len(content) > 200:
            sentences = re.split(r'[.!?]+', content)
            current = ""
            for sent in sentences:
                sent = sent.strip()
                if sent:
                    current += sent + ". "
                    if len(current) > 150:
                        subsections.append({
                            "document": section["document"],
                            "page_number": section["page"],
                            "refined_text": current.strip()
                        })
                        current = ""
            if current.strip():
                subsections.append({
                    "document": section["document"],
                    "page_number": section["page"],
                    "refined_text": current.strip()
                })

        return subsections[:3]

def main():
    input_dir = "/app/input"
    output_dir = "/app/output"

    try:
        os.makedirs(output_dir, exist_ok=True)
        input_file = os.path.join(input_dir, "input.json")

        if not os.path.exists(input_file):
            logger.error("input.json not found in input directory")
            return

        with open(input_file, "r", encoding='utf-8') as f:
            metadata = json.load(f)

        persona = metadata.get("persona", {}).get("role", "")
        job = metadata.get("job_to_be_done", {}).get("task", "")
        logger.info(f"Persona: {persona}")
        logger.info(f"Job: {job}")
        pdf_files = [doc["filename"] for doc in metadata.get("documents", []) if doc["filename"].endswith(".pdf")]

        if not pdf_files:
            logger.warning("No PDF files listed in input.json")
            return

        all_sections = []
        analyzer = PersonaDrivenAnalyzer()

        for pdf_file in pdf_files:
            pdf_path = os.path.join(input_dir, pdf_file)
            if not os.path.exists(pdf_path):
                logger.warning(f"File not found: {pdf_file}")
                continue
            logger.info(f"Processing {pdf_file}")
            sections = analyzer.extract_sections_with_headings(pdf_path)
            all_sections.extend(sections)
            logger.info(f"Extracted {len(sections)} sections from {pdf_file}")

        ranked_sections = analyzer.rank_sections_by_relevance(all_sections, persona, job)
        top_sections = ranked_sections[:10]

        output = {
            "metadata": {
                "input_documents": pdf_files,
                "persona": persona,
                "job": job,
                "timestamp": datetime.now().isoformat(),
                "total_sections_found": len(all_sections),
                "sections_selected": len(top_sections)
            },
            "sections": [],
            "subsections": []
        }

        for rank, section in enumerate(top_sections, 1):
            title = section["heading"] or section["text"][:100] + "..."
            output["sections"].append({
                "document": section["document"],
                "page_number": section["page"],
                "section_title": title,
                "importance_rank": rank,
                "relevance_score": round(section["relevance_score"], 4)
            })
            output["subsections"].extend(analyzer.extract_subsections(section))

        result_path = os.path.join(output_dir, "result.json")
        with open(result_path, "w", encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)

        logger.info(f"Saved results to {result_path}")
        logger.info(f"Selected {len(output['sections'])} sections and {len(output['subsections'])} subsections")

    except Exception as e:
        logger.error(f"Error during processing: {str(e)}")
        error_output = {
            "metadata": {
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            },
            "sections": [],
            "subsections": []
        }
        with open(os.path.join(output_dir, "result.json"), "w") as f:
            json.dump(error_output, f, indent=2)

if __name__ == "__main__":
    main()