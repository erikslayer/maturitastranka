"""
PDF Text Extractor for Maturita Portal

This script downloads PDFs from URLs and extracts their text content.
The extracted text is saved to individual text files for use in the portal.

Requirements:
    pip install requests pypdf2
"""

import os
import re
import sys
from urllib.parse import unquote

# Check for required packages
try:
    import requests
except ImportError:
    print("Installing requests...")
    os.system("pip install requests")
    import requests

try:
    from PyPDF2 import PdfReader
except ImportError:
    print("Installing PyPDF2...")
    os.system("pip install pypdf2")
    from PyPDF2 import PdfReader

# PDF URLs with book information
BOOKS = [
    {
        "url": "https://www.milujemecestinu.cz/files/tournaments/112/Zdenek_Jirotka_Saturnin.pdf",
        "title": "Saturnin",
        "author": "Zdenek Jirotka",
        "slug": "saturnin"
    },
    {
        "url": "https://www.milujemecestinu.cz/files/tournaments/29/Karel_Capek_-_R._U._R..pdf",
        "title": "R.U.R.",
        "author": "Karel Capek",
        "slug": "rur"
    },
    {
        "url": "https://www.milujemecestinu.cz/files/tournaments/83/Francis_Scott_Fitzgerald_Velky_Gatsby.pdf",
        "title": "Velky Gatsby",
        "author": "Francis Scott Fitzgerald",
        "slug": "gatsby"
    },
    {
        "url": "https://www.milujemecestinu.cz/files/tournaments/131/Moliere_Lakomec.pdf",
        "title": "Lakomec",
        "author": "Moliere",
        "slug": "lakomec"
    },
    {
        "url": "https://www.milujemecestinu.cz/files/tournaments/157/Erich_Maria_Remarque_Na_zapadni_fronte_klid.pdf",
        "title": "Na zapadni fronte klid",
        "author": "Erich Maria Remarque",
        "slug": "na-zapadni-fronte-klid"
    },
    {
        "url": "https://www.milujemecestinu.cz/files/tournaments/68/John_Steinbeck_O_mysich_a_lidech.pdf",
        "title": "O mysich a lidech",
        "author": "John Steinbeck",
        "slug": "o-mysich-a-lidech"
    },
    {
        "url": "https://www.milujemecestinu.cz/files/tournaments/81/Antoine_de_Saint_Exupery_Maly_princ.pdf",
        "title": "Maly princ",
        "author": "Antoine de Saint-Exupery",
        "slug": "maly-princ"
    },
]


def download_pdf(url: str, output_path: str) -> bool:
    """
    Download a PDF from a URL.
    
    Args:
        url: The URL to download from
        output_path: Where to save the PDF
        
    Returns:
        True if successful, False otherwise
    """
    try:
        print(f"  Downloading from {url[:60]}...")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        with open(output_path, 'wb') as f:
            f.write(response.content)
        
        print(f"  Downloaded: {os.path.basename(output_path)}")
        return True
        
    except Exception as e:
        print(f"  ERROR downloading: {e}")
        return False


def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract text content from a PDF file.
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        Extracted text content
    """
    try:
        reader = PdfReader(pdf_path)
        text_parts = []
        
        for i, page in enumerate(reader.pages):
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)
        
        full_text = "\n\n".join(text_parts)
        
        # Clean up the text
        full_text = re.sub(r'\n{3,}', '\n\n', full_text)  # Remove excessive newlines
        full_text = re.sub(r' {2,}', ' ', full_text)  # Remove excessive spaces
        
        return full_text
        
    except Exception as e:
        print(f"  ERROR extracting text: {e}")
        return ""


def save_text(text: str, output_path: str) -> bool:
    """
    Save extracted text to a file.
    
    Args:
        text: The text content to save
        output_path: Where to save the text file
        
    Returns:
        True if successful, False otherwise
    """
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text)
        return True
    except Exception as e:
        print(f"  ERROR saving text: {e}")
        return False


def main():
    """Main function to process all PDFs."""
    
    # Setup directories
    script_dir = os.path.dirname(os.path.abspath(__file__))
    pdf_dir = os.path.join(script_dir, "literatura", "pdfs")
    text_dir = os.path.join(script_dir, "literatura", "text")
    
    os.makedirs(pdf_dir, exist_ok=True)
    os.makedirs(text_dir, exist_ok=True)
    
    print("=" * 60)
    print("PDF Text Extractor for Maturita Portal")
    print("=" * 60)
    print()
    
    results = []
    
    for i, book in enumerate(BOOKS, 1):
        print(f"[{i}/{len(BOOKS)}] Processing: {book['title']}")
        print(f"    Author: {book['author']}")
        
        pdf_path = os.path.join(pdf_dir, f"{book['slug']}.pdf")
        text_path = os.path.join(text_dir, f"{book['slug']}.txt")
        
        # Download PDF
        if not os.path.exists(pdf_path):
            success = download_pdf(book['url'], pdf_path)
            if not success:
                results.append((book['title'], "FAILED - Download error"))
                print()
                continue
        else:
            print(f"  PDF already exists: {book['slug']}.pdf")
        
        # Extract text
        print(f"  Extracting text...")
        text = extract_text_from_pdf(pdf_path)
        
        if text:
            # Save text
            save_text(text, text_path)
            word_count = len(text.split())
            results.append((book['title'], f"OK - {word_count} words"))
            print(f"  Saved: {book['slug']}.txt ({word_count} words)")
        else:
            results.append((book['title'], "FAILED - No text extracted"))
        
        print()
    
    # Summary
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    for title, status in results:
        print(f"  {title}: {status}")
    print()
    print(f"PDFs saved to: {pdf_dir}")
    print(f"Texts saved to: {text_dir}")
    print("=" * 60)


if __name__ == "__main__":
    main()
