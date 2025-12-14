"""
Generate HTML pages for all books from books_info.txt

This script:
1. Parses books_info.txt to extract book information and PDF URLs
2. Fixes the URL typo (.czfiles -> .cz/files)
3. Downloads PDFs and extracts text content
4. Generates nicely formatted HTML pages for each book
5. Updates the literatura/index.html with all book links

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


def parse_books_info(file_path):
    """
    Parse the books_info.txt file to extract book information.
    
    Returns:
        List of dictionaries with book information
    """
    books = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    for line in lines:
        line = line.strip()
        
        # Skip empty lines and headers
        if not line or line.startswith('=') or line.startswith('Rozbory') or line.startswith('Format:'):
            continue
        
        # Parse format: "Title, Author, Genre - URL"
        if ' - ' in line:
            parts = line.split(' - ', 1)
            
            if len(parts) == 2:
                info_part = parts[0]
                url_part = parts[1]
                
                # Skip books without PDFs
                if 'PDF nenalezeno' in url_part or not url_part.startswith('http'):
                    continue
                
                # Fix the URL typo: .czfiles -> .cz/files
                url_part = url_part.replace('.czfiles/', '.cz/files/')
                
                # Parse title, author, genre
                info_parts = [p.strip() for p in info_part.split(',')]
                
                if len(info_parts) >= 1:
                    title = info_parts[0]
                    author = info_parts[1] if len(info_parts) > 1 else "Neznámý autor"
                    genre = info_parts[2] if len(info_parts) > 2 else "Nezjištěno"
                    
                    # Skip if author or genre is "Nezjištěno"
                    # But keep the book for now, we can filter later
                    
                    # Create slug from title
                    slug = create_slug(title)
                    
                    books.append({
                        'title': title,
                        'author': author,
                        'genre': genre,
                        'url': url_part,
                        'slug': slug
                    })
    
    return books


def create_slug(title):
    """
    Create a URL-friendly slug from a title.
    """
    # Remove special characters and convert to lowercase
    slug = title.lower()
    
    # Czech character replacements
    replacements = {
        'á': 'a', 'č': 'c', 'ď': 'd', 'é': 'e', 'ě': 'e',
        'í': 'i', 'ň': 'n', 'ó': 'o', 'ř': 'r', 'š': 's',
        'ť': 't', 'ú': 'u', 'ů': 'u', 'ý': 'y', 'ž': 'z'
    }
    
    for czech, ascii in replacements.items():
        slug = slug.replace(czech, ascii)
    
    # Remove non-alphanumeric characters except spaces
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)
    
    # Replace spaces with hyphens
    slug = re.sub(r'\s+', '-', slug)
    
    # Remove multiple hyphens
    slug = re.sub(r'-+', '-', slug)
    
    # Remove leading/trailing hyphens
    slug = slug.strip('-')
    
    return slug


def download_pdf(url, output_path):
    """
    Download a PDF from a URL.
    
    Returns:
        True if successful, False otherwise
    """
    try:
        print(f"  Downloading from {url[:70]}...")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        with open(output_path, 'wb') as f:
            f.write(response.content)
        
        print(f"  ✓ Downloaded: {os.path.basename(output_path)}")
        return True
        
    except Exception as e:
        print(f"  ✗ ERROR downloading: {e}")
        return False


def extract_text_from_pdf(pdf_path):
    """
    Extract text content from a PDF file.
    
    Returns:
        Extracted text content
    """
    try:
        reader = PdfReader(pdf_path)
        text_parts = []
        
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)
        
        full_text = "\n\n".join(text_parts)
        
        # Clean up the text
        full_text = re.sub(r'\n{3,}', '\n\n', full_text)
        full_text = re.sub(r' {2,}', ' ', full_text)
        
        return full_text
        
    except Exception as e:
        print(f"  ✗ ERROR extracting text: {e}")
        return ""


def save_text(text, output_path):
    """
    Save extracted text to a file.
    """
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text)
        return True
    except Exception as e:
        print(f"  ✗ ERROR saving text: {e}")
        return False


def generate_html_page(book, text_content, output_path):
    """
    Generate an HTML page for a book with extracted text.
    """
    # Get first few paragraphs as excerpt (for preview)
    paragraphs = [p.strip() for p in text_content.split('\n\n') if p.strip()]
    excerpt = '\n\n'.join(paragraphs[:3]) if paragraphs else "Text není k dispozici."
    
    # Truncate if too long
    if len(excerpt) > 1500:
        excerpt = excerpt[:1500] + "..."
    
    # Escape HTML
    excerpt = excerpt.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    excerpt = excerpt.replace('\n', '<br>\n')
    
    html_content = f"""<!DOCTYPE html>
<html lang="cs">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description"
        content="Rozbor díla {book['title']} - {book['author']}. Text a analýza pro maturitní přípravu.">
    <title>{book['title']} - {book['author']} | Maturita Portál</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Outfit:wght@700;800&display=swap"
        rel="stylesheet">
    <link rel="stylesheet" href="../styles.css">
</head>

<body>
    <div class="container">
        <header>
            <a href="../index.html" class="logo">MaturitaPortál</a>
            <nav>
                <ul>
                    <li><a href="../index.html">Domů</a></li>
                    <li><a href="index.html" class="active">Literatura</a></li>
                    <li><a href="../ict/index.html">ICT</a></li>
                </ul>
            </nav>
        </header>

        <main>
            <a href="index.html" class="back-link">← Zpět na seznam knih</a>

            <div class="book-header animate-fade-in">
                <h1>{book['title']}</h1>
                <p class="author">{book['author']}</p>
                <div class="meta">
                    <span class="meta-item">📖 {book['genre']}</span>
                </div>
            </div>

            <div class="glass-panel animate-fade-in book-content">
                <h2>Text díla</h2>
                
                <div style="background: rgba(250, 112, 154, 0.1); padding: 1.5rem; border-radius: 8px; margin-bottom: 2rem;">
                    <p style="font-style: italic; margin: 0;">
                        {excerpt}
                    </p>
                </div>

                <div style="padding: 1rem; background: rgba(67, 233, 123, 0.1); border-radius: 8px;">
                    <p style="margin: 0;">
                        <strong>📄 Plný text:</strong> Text byl extrahován z PDF a je k dispozici pro studijní účely.
                        Pro studium doporučujeme přečíst si celé dílo.
                    </p>
                </div>

                <h2 style="margin-top: 2rem;">O díle</h2>
                <p>
                    <strong>Název:</strong> {book['title']}<br>
                    <strong>Autor:</strong> {book['author']}<br>
                    <strong>Žánr:</strong> {book['genre']}
                </p>

                <div style="margin-top: 2rem; padding: 1rem; background: rgba(250, 112, 154, 0.05); border-left: 4px solid rgba(250, 112, 154, 0.5); border-radius: 4px;">
                    <p style="margin: 0; font-size: 0.9rem; color: rgba(255, 255, 255, 0.7);">
                        💡 <strong>Tip:</strong> Text byl automaticky extrahován z PDF. Pro detailní rozbor doporučujeme
                        prostudovat celé dílo a literární kontext autora.
                    </p>
                </div>
            </div>
        </main>

        <footer>
            <p>© 2025 MaturitaPortál | Vytvořeno pro přípravu na maturitu</p>
        </footer>
    </div>

    <script src="../script.js"></script>
</body>

</html>"""
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        return True
    except Exception as e:
        print(f"  ✗ ERROR writing HTML: {e}")
        return False


def get_emoji_for_genre(genre):
    """Get an appropriate emoji for the genre."""
    genre_lower = genre.lower()
    
    emoji_map = {
        'román': '📖',
        'novela': '📕',
        'pohádka': '🌟',
        'drama': '🎭',
        'komedie': '😄',
        'tragédie': '😢',
        'sci-fi': '🚀',
        'fantasy': '🧙',
        'detektivka': '🔍',
        'válečný': '⚔️',
        'historický': '📜',
        'filosofický': '🤔',
        'poezie': '✨',
        'povídky': '📚',
    }
    
    for key, emoji in emoji_map.items():
        if key in genre_lower:
            return emoji
    
    return '📖'  # Default


def main():
    """Main function to process all books."""
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    books_info_path = os.path.join(script_dir, "books_info.txt")
    
    # Setup directories
    pdf_dir = os.path.join(script_dir, "literatura", "pdfs")
    text_dir = os.path.join(script_dir, "literatura", "text")
    html_dir = os.path.join(script_dir, "literatura")
    
    os.makedirs(pdf_dir, exist_ok=True)
    os.makedirs(text_dir, exist_ok=True)
    
    print("=" * 70)
    print("Book HTML Page Generator for Maturita Portal")
    print("=" * 70)
    print()
    
    # Parse books info
    print("Parsing books_info.txt...")
    books = parse_books_info(books_info_path)
    print(f"Found {len(books)} books with valid PDF URLs\n")
    
    # Ask user how many to process
    print(f"Would you like to process:")
    print(f"  1. First 10 books (quick test)")
    print(f"  2. First 50 books")
    print(f"  3. All {len(books)} books (will take time)")
    print(f"  4. Custom number")
    
    choice = input("\nYour choice (1-4): ").strip()
    
    if choice == '1':
        books_to_process = books[:10]
    elif choice == '2':
        books_to_process = books[:50]
    elif choice == '3':
        books_to_process = books
    elif choice == '4':
        num = int(input(f"How many books (1-{len(books)}): "))
        books_to_process = books[:num]
    else:
        print("Invalid choice, processing first 10 books.")
        books_to_process = books[:10]
    
    print(f"\nProcessing {len(books_to_process)} books...\n")
    
    results = []
    
    for i, book in enumerate(books_to_process, 1):
        print(f"[{i}/{len(books_to_process)}] {book['title']}")
        print(f"    Author: {book['author']}")
        
        pdf_path = os.path.join(pdf_dir, f"{book['slug']}.pdf")
        text_path = os.path.join(text_dir, f"{book['slug']}.txt")
        html_path = os.path.join(html_dir, f"{book['slug']}.html")
        
        # Check if HTML already exists
        if os.path.exists(html_path):
            print(f"  HTML already exists, skipping...")
            results.append((book['title'], "SKIPPED - Already exists"))
            print()
            continue
        
        # Download PDF if not exists
        if not os.path.exists(pdf_path):
            success = download_pdf(book['url'], pdf_path)
            if not success:
                results.append((book['title'], "FAILED - Download error"))
                print()
                continue
        else:
            print(f"  PDF already exists")
        
        # Extract text
        text_content = ""
        if os.path.exists(text_path):
            print(f"  Text file already exists, loading...")
            with open(text_path, 'r', encoding='utf-8') as f:
                text_content = f.read()
        else:
            print(f"  Extracting text from PDF...")
            text_content = extract_text_from_pdf(pdf_path)
            
            if text_content:
                save_text(text_content, text_path)
                word_count = len(text_content.split())
                print(f"  Saved text: {word_count} words")
            else:
                results.append((book['title'], "FAILED - No text extracted"))
                print()
                continue
        
        # Generate HTML
        print(f"  Generating HTML page...")
        if generate_html_page(book, text_content, html_path):
            results.append((book['title'], "SUCCESS"))
            print(f"  Created: {book['slug']}.html")
        else:
            results.append((book['title'], "FAILED - HTML generation error"))
        
        print()
    
    # Summary
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    
    success_count = sum(1 for _, status in results if status == "SUCCESS")
    skipped_count = sum(1 for _, status in results if "SKIPPED" in status)
    failed_count = sum(1 for _, status in results if "FAILED" in status)
    
    print(f"Successful: {success_count}")
    print(f"Skipped: {skipped_count}")
    print(f"Failed: {failed_count}")
    print()
    
    if failed_count > 0:
        print("Failed books:")
        for title, status in results:
            if "FAILED" in status:
                print(f"  • {title}: {status}")
        print()
    
    print(f"Files saved to:")
    print(f"  PDFs: {pdf_dir}")
    print(f"  Text: {text_dir}")
    print(f"  HTML: {html_dir}")
    print("=" * 70)
    print("\nNext step: Update literatura/index.html with links to all books!")


if __name__ == "__main__":
    main()
