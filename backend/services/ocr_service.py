import os
import subprocess
import shutil
from collections import Counter
from PyPDF2 import PdfMerger
import tempfile

def process_pdf_to_text(pdf_path: str) -> str:
    """
    Performs OCR on a given PDF file and returns the path to the cleaned text file.
    """
    # Create a unique temporary directory for this specific PDF processing
    temp_dir = tempfile.mkdtemp()
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    file_base = os.path.splitext(os.path.basename(pdf_path))[0]
    
    # Check for Tesseract executable
    tesseract_path = shutil.which("tesseract") or r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    if not os.path.exists(tesseract_path):
        raise RuntimeError(f"Tesseract not found.")

    print(f"Processing {pdf_path} in temporary directory {temp_dir}")
    
    # Convert PDF to PNGs
    png_prefix = os.path.join(temp_dir, f"{file_base}-%04d.png")
    magick_command = f'magick -density 150 "{pdf_path}" "{png_prefix}"'
    os.system(magick_command)
    
    # OCR each PNG
    pngs = sorted([f for f in os.listdir(temp_dir) if f.lower().endswith('.png')])
    for pic in pngs:
        pic_path = os.path.join(temp_dir, pic)
        base_out = os.path.splitext(pic_path)[0]
        cmd_txt = [tesseract_path, pic_path, base_out, '-l', 'ind+eng']
        subprocess.run(cmd_txt, capture_output=True, text=True)
        
    # Combine TXTs and clean headers/footers
    ocr_txts = sorted([os.path.join(temp_dir, f) for f in os.listdir(temp_dir) if f.endswith(".txt")])
    page_texts = []
    for t in ocr_txts:
        with open(t, 'r', encoding='utf-8', errors='ignore') as f:
            page_texts.append([line.strip() for line in f if line.strip()])

    all_lines = [line for lines in page_texts for line in lines]
    line_counter = Counter(all_lines)
    likely_header_footer = {line for line, count in line_counter.items() if count > len(page_texts) // 2 and len(page_texts) > 1}

    # Write cleaned text to a final output file
    clean_txt_path = os.path.join(output_dir, f"{file_base}-clean.txt")
    with open(clean_txt_path, 'w', encoding='utf-8') as out:
        for lines in page_texts:
            for line in lines:
                if line not in likely_header_footer:
                    out.write(line + "\n")
            out.write("\n")
            
    # Cleanup the temporary directory
    shutil.rmtree(temp_dir)
    print(f"Cleaned TXT saved to: {clean_txt_path}")
    
    return clean_txt_path