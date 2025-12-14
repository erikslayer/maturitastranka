import requests
from bs4 import BeautifulSoup
import time
import re

def get_book_links(main_url):
    """Extract all book detail page links from the main page"""
    print("Fetching book links from main page...")
    response = requests.get(main_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find all links that point to book detail pages
    book_links = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        if 'mod=mod-tournaments3' in href and 'spec=detail' in href:
            # Make sure it's a full URL
            if not href.startswith('http'):
                href = 'https://www.milujemecestinu.cz/' + href.lstrip('/')
            book_links.append(href)
    
    print(f"Found {len(book_links)} book links")
    return book_links

def extract_book_info(detail_url):
    """Extract book information from a detail page"""
    try:
        print(f"Processing: {detail_url}")
        response = requests.get(detail_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Initialize variables
        title = "Unknown"
        author = "Unknown"
        genre = "Unknown"
        pdf_url = None
        
        # Try to extract the title - usually in <h1> or <h2>
        title_tag = soup.find('h1')
        if not title_tag:
            title_tag = soup.find('h2')
        if title_tag:
            title = title_tag.get_text().strip()
        
        # Look for PDF links
        for link in soup.find_all('a', href=True):
            href = link['href']
            if '.pdf' in href.lower():
                pdf_url = href
                if not pdf_url.startswith('http'):
                    pdf_url = 'https://www.milujemecestinu.cz/' + pdf_url.lstrip('/')
                break
        
        # Try to find author and genre in the page content
        # Look for common patterns like "Autor:", "Žánr:", etc.
        text_content = soup.get_text()
        
        # Extract author
        author_match = re.search(r'(?:Autor|autor|AUTOR):\s*([^\n]+)', text_content)
        if author_match:
            author = author_match.group(1).strip()
        
        # Extract genre
        genre_match = re.search(r'(?:Žánr|žánr|ŽÁNR|Druh|druh):\s*([^\n]+)', text_content)
        if genre_match:
            genre = genre_match.group(1).strip()
        
        # Look for table rows that might contain this info
        for row in soup.find_all('tr'):
            cells = row.find_all(['td', 'th'])
            if len(cells) >= 2:
                key = cells[0].get_text().strip().lower()
                value = cells[1].get_text().strip()
                
                if 'autor' in key:
                    author = value
                elif 'žánr' in key or 'druh' in key or 'literární druh' in key:
                    genre = value
        
        return {
            'title': title,
            'author': author,
            'genre': genre,
            'pdf_url': pdf_url
        }
    except Exception as e:
        print(f"Error processing {detail_url}: {e}")
        return None

def main():
    main_url = "https://www.milujemecestinu.cz/index.php?mnu=rozbory-literarnich-del&lid=cs&mod=mod-tournaments3&shw=preview"
    output_file = "books_info.txt"
    
    # Get all book links
    book_links = get_book_links(main_url)
    
    # Extract information from each book
    books_data = []
    for i, link in enumerate(book_links, 1):
        print(f"\nProcessing book {i}/{len(book_links)}")
        info = extract_book_info(link)
        if info and info['pdf_url']:
            books_data.append(info)
        
        # Be polite to the server - wait a bit between requests
        time.sleep(0.5)
    
    # Write to file
    print(f"\nWriting {len(books_data)} books to {output_file}")
    with open(output_file, 'w', encoding='utf-8') as f:
        for book in books_data:
            line = f"{book['title']}, {book['author']}, {book['genre']} - {book['pdf_url']}\n"
            f.write(line)
    
    print(f"\nDone! Extracted {len(books_data)} books with PDF URLs")
    print(f"Results saved to {output_file}")

if __name__ == "__main__":
    main()
