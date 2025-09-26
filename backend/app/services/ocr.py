import os
import time
import calendar
import subprocess
import shutil
from collections import Counter
from PyPDF2 import PdfMerger

# directories
INPUT_DIR = "pdfs"
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# all files inside pdfs/
dir_files = [f for f in os.listdir(INPUT_DIR) if os.path.isfile(os.path.join(INPUT_DIR, f))]
epoch_time = int(calendar.timegm(time.gmtime()))
print("Found PDFs:", dir_files)

# find tesseract
def which(program):
    for path in os.environ["PATH"].split(os.pathsep):
        exe_file = os.path.join(path.strip('"'), program)
        if os.path.isfile(exe_file) and os.access(exe_file, os.X_OK):
            return exe_file
    return None

tesseract_path = which("tesseract") or r"C:\Program Files\Tesseract-OCR\tesseract.exe"
if not os.path.exists(tesseract_path):
    raise RuntimeError(f"Tesseract not found at: {tesseract_path}")

for file in dir_files:  # look at every file in pdfs/
    if file.endswith('.pdf') and "-ocr" not in file:  # skip already OCR'd
        print('Working on converting:', file)

        # setup
        file_base = file.replace('.pdf', '')
        folder = str(int(epoch_time)) + '_' + file_base
        combined = os.path.join(folder, file_base)

        # create folder
        if not os.path.exists(folder):
            os.makedirs(folder)

        # input path
        input_pdf = os.path.join(INPUT_DIR, file)

        # convert PDF to PNG(s)
        magick = f'magick -density 150 "{input_pdf}" "{combined}-%04d.png"'
        print(magick)
        os.system(magick)

        # OCR each PNG -> PDF + TXT
        pngs = sorted([f for f in os.listdir(folder) if f.lower().endswith('.png')])
        for pic in pngs:
            combined_pic = os.path.join(folder, pic)
            base_out = combined_pic + '-ocr'
            print("OCRing:", combined_pic)

            # PDF output
            cmd_pdf = [tesseract_path, combined_pic, base_out, '-l', 'ind+eng', 'pdf']
            r = subprocess.run(cmd_pdf, capture_output=True, text=True)
            if r.returncode != 0:
                print("ERROR (pdf):", r.stderr.strip() or r.stdout.strip())

            # TXT output
            cmd_txt = [tesseract_path, combined_pic, base_out, '-l', 'ind+eng']
            r2 = subprocess.run(cmd_txt, capture_output=True, text=True)
            if r2.returncode != 0:
                print("ERROR (txt):", r2.stderr.strip() or r2.stdout.strip())

        # combine OCR'd PDFs into one
        ocr_pdfs = sorted([os.path.join(folder, f) for f in os.listdir(folder) if f.endswith("-ocr.pdf")])
        merger = PdfMerger()
        for pdf in ocr_pdfs:
            merger.append(pdf)
        out_pdf = os.path.join(OUTPUT_DIR, file_base + '-ocr-combined.pdf')
        merger.write(out_pdf)
        merger.close()
        print("Combined PDF:", out_pdf)

        # combine OCR'd TXTs into one
        ocr_txts = sorted([os.path.join(folder, f) for f in os.listdir(folder) if f.endswith("-ocr.txt")])
        page_texts = []
        for t in ocr_txts:
            with open(t, 'r', encoding='utf-8', errors='ignore') as ff:
                lines = [line.strip() for line in ff if line.strip()]
                page_texts.append(lines)

        # count line frequencies across pages
        all_lines = []
        for lines in page_texts:
            all_lines.extend(lines)
        line_counter = Counter(all_lines)

        # detect repeating header/footer
        likely_header_footer = {line for line, count in line_counter.items() if count > len(page_texts) // 2}
        print("Detected repeating header/footer lines:", likely_header_footer)

        # write cleaned output
        out_txt = os.path.join(OUTPUT_DIR, file_base + '-ocr-combined-clean.txt')
        with open(out_txt, 'w', encoding='utf-8') as out:
            for lines in page_texts:
                for line in lines:
                    if line not in likely_header_footer:
                        out.write(line + "\n")
                out.write("\n")
        print("Cleaned TXT:", out_txt)

print("Current working directory:", os.getcwd())

# cleanup temp folder
shutil.rmtree(folder, ignore_errors=True)
print("Deleted temp folder:", folder)