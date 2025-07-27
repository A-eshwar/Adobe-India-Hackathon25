
import json
import os
import sys
from pathlib import Path
import re
import logging
from typing import Dict, List, Tuple
import fitz  
from collections import Counter
import statistics

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)  

class PDFOutlineExtractor:
    def _init(self): 
        self.heading_patterns = [
            r'^\d+\.?\s+',
            r'^\d+\.\d+\.?\s+',
            r'^\d+\.\d+\.\d+\.?\s+',
            r'^[A-Z][A-Z\s]{2,}$',
            r'^[A-Z][a-z]+(?:\s[A-Z][a-z])*$',
            r'^Chapter\s+\d+',
            r'^Section\s+\d+',
            r'^Part\s+[IVX]+',
        ]
        self.heading_keywords = [
            'introduction', 'overview', 'background', 'methodology', 'results',
            'conclusion', 'abstract', 'summary', 'discussion', 'analysis',
            'chapter', 'section', 'part', 'appendix', 'references', 'bibliography',
            'contents', 'index', 'preface', 'acknowledgments', 'table of contents',
            'はじめに', '概要', '結論', '参考文献', '目次', '付録'
        ]

    def extract_text_with_formatting(self, pdf_path: str) -> List[Dict]:
        doc = fitz.open(pdf_path)
        text_blocks = []

        for page_num in range(len(doc)):
            page = doc[page_num]
            blocks = page.get_text("dict")["blocks"]

            for block in blocks:
                if "lines" in block:
                    for line in block["lines"]:
                        for span in line["spans"]:
                            text = span["text"].strip()
                            if text:
                                text_blocks.append({
                                    'text': text,
                                    'page': page_num + 1,
                                    'font_size': span["size"],
                                    'font_flags': span["flags"],
                                    'bbox': span["bbox"]
                                })

        doc.close()
        return text_blocks

    def analyze_font_characteristics(self, text_blocks: List[Dict]) -> Dict:
        font_sizes = [block['font_size'] for block in text_blocks]
        font_flags = [block['font_flags'] for block in text_blocks]

        avg_font_size = statistics.mean(font_sizes)
        font_size_counts = Counter(font_sizes)
        body_font_size = font_size_counts.most_common(1)[0][0]

        heading_font_sizes = sorted([size for size in set(font_sizes)
                                     if size > body_font_size], reverse=True)

        return {
            'body_font_size': body_font_size,
            'avg_font_size': avg_font_size,
            'heading_font_sizes': heading_font_sizes,
            'font_size_counts': font_size_counts
        }

    def is_likely_heading(self, text: str, font_size: float, font_flags: int,
                          font_analysis: Dict) -> Tuple[bool, int]:
        text_clean = text.strip()

        if len(text_clean) < 3 or len(text_clean) > 200:
            return False, 0

        if any(skip in text_clean.lower() for skip in ['page', 'figure', 'table', 'www.', 'http']):
            return False, 0

        score = 0

        if font_size > font_analysis['body_font_size']:
            score += 3
            if font_size in font_analysis['heading_font_sizes'][:3]:
                score += 2

        if font_flags & 16:  
            score += 2

        for pattern in self.heading_patterns:
            if re.match(pattern, text_clean, re.IGNORECASE):
                score += 3
                break

        if any(keyword in text_clean.lower() for keyword in self.heading_keywords):
            score += 1

        if text_clean.isupper() and 3 <= len(text_clean) <= 50:
            score += 1

        if text_clean.istitle():
            score += 1

        level = 0
        if score >= 4:
            if font_size in font_analysis['heading_font_sizes'][:1]:
                level = 1
            elif font_size in font_analysis['heading_font_sizes'][:2]:
                level = 2
            elif font_size in font_analysis['heading_font_sizes'][:3]:
                level = 3
            else:
                level = 3

        return score >= 4, level

    def extract_title(self, text_blocks: List[Dict]) -> str:
        first_page_blocks = [block for block in text_blocks if block['page'] <= 3]

        if not first_page_blocks:
            return "Untitled Document"

        max_font_size = max(block['font_size'] for block in first_page_blocks)

        title_candidates = [
            block['text'] for block in first_page_blocks
            if block['font_size'] == max_font_size and len(block['text'].strip()) > 3
        ]

        if title_candidates:
            title = title_candidates[0].strip()
            title = re.sub(r'^\d+\.?\s*', '', title)
            return title

        return "Untitled Document"

    def extract_outline(self, pdf_path: str) -> Dict:
        try:
            logger.info(f"Processing PDF: {pdf_path}")

            text_blocks = self.extract_text_with_formatting(pdf_path)
            if not text_blocks:
                return {"title": "Empty Document", "outline": []}

            font_analysis = self.analyze_font_characteristics(text_blocks)
            logger.info(f"Font analysis: body={font_analysis['body_font_size']:.1f}, "
                        f"headings={font_analysis['heading_font_sizes'][:3]}")

            title = self.extract_title(text_blocks)
            logger.info(f"Extracted title: {title}")

            outline = []
            seen_headings = set()

            for block in text_blocks:
                is_heading, level = self.is_likely_heading(
                    block['text'], block['font_size'],
                    block['font_flags'], font_analysis
                )

                if is_heading and level > 0:
                    heading_text = re.sub(r'^\d+\.?\s*', '', block['text'].strip())
                    heading_text = re.sub(r'\s+', ' ', heading_text)

                    if heading_text not in seen_headings and 3 <= len(heading_text) <= 200:
                        outline.append({
                            "level": f"H{level}",
                            "text": heading_text,
                            "page": block['page']
                        })
                        seen_headings.add(heading_text)

            outline.sort(key=lambda x: (x['page'], x['level']))
            logger.info(f"Extracted {len(outline)} headings")

            return {
                "title": title,
                "outline": outline
            }

        except Exception as e:
            logger.error(f"Error processing PDF {pdf_path}: {str(e)}")
            return {"title": "Error Processing Document", "outline": []}


def process_all_pdfs(input_dir: str, output_dir: str):
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    extractor = PDFOutlineExtractor()
    pdf_files = list(input_path.glob("*.pdf"))

    if not pdf_files:
        logger.warning(f"No PDF files found in {input_dir}")
        return

    logger.info(f"Found {len(pdf_files)} PDF files to process")

    for pdf_file in pdf_files:
        try:
            logger.info(f"Processing: {pdf_file.name}")
            result = extractor.extract_outline(str(pdf_file))
            output_filename = pdf_file.stem + ".json"
            output_filepath = output_path / output_filename

            with open(output_filepath, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)

            logger.info(f"Saved: {output_filename}")
        except Exception as e:
            logger.error(f"Failed to process {pdf_file.name}: {str(e)}")


def main():
    input_dir = "/app/input"
    output_dir = "/app/output"
    logger.info("Starting PDF Outline Extractor")
    logger.info(f"Input directory: {input_dir}")
    logger.info(f"Output directory: {output_dir}")
    if not os.path.exists(input_dir):
        logger.error(f"Input directory does not exist: {input_dir}")
        sys.exit(1)
    process_all_pdfs(input_dir, output_dir)
    logger.info("Processing complete")


if __name__ == "_main_":
    main()
