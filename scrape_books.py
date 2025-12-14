import requests
from bs4 import BeautifulSoup
import re
import time

def scrape_book_list():
    """Scrape the main list page to get all book URLs"""
    url = "https://www.milujemecestinu.cz/index.php?mnu=rozbory-literarnich-del&lid=cs&mod=mod-tournaments3&shw=preview"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all links to book detail pages
        book_links = []
        for link in soup.find_all('a', href=True):
            href = link.get('href')
            if 'mod=mod-tournaments3' in href and 'op=archive' in href and 'itemid=' in href:
                full_url = href if href.startswith('http') else f"https://www.milujemecestinu.cz/{href}"
                book_title = link.get_text(strip=True)
                book_links.append({
                    'title': book_title,
                    'url': full_url
                })
        
        return book_links
    except Exception as e:
        print(f"Error scraping book list: {e}")
        return []

def scrape_book_details(book_url):
    """Scrape individual book page for author, genre, and PDF URL"""
    try:
        response = requests.get(book_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find PDF link
        pdf_url = None
        for link in soup.find_all('a', href=True):
            href = link.get('href')
            if href.endswith('.pdf'):
                pdf_url = href if href.startswith('http') else f"https://www.milujemecestinu.cz{href}"
                break
        
        # Try to extract author and genre from the page content
        author = "Nezjištěno"
        genre = "Nezjištěno"
        
        # Look for author information in various possible locations
        page_text = soup.get_text()
        
        # Common patterns for author
        author_patterns = [
            r'Autor:\s*([^\n]+)',
            r'Spisovate[lí]:\s*([^\n]+)',
        ]
        
        for pattern in author_patterns:
            match = re.search(pattern, page_text, re.IGNORECASE)
            if match:
                author = match.group(1).strip()
                break
        
        # Common patterns for genre
        genre_patterns = [
            r'Žánr:\s*([^\n]+)',
            r'Literární druh:\s*([^\n]+)',
        ]
        
        for pattern in genre_patterns:
            match = re.search(pattern, page_text, re.IGNORECASE)
            if match:
                genre = match.group(1).strip()
                break
        
        return {
            'author': author,
            'genre': genre,
            'pdf_url': pdf_url
        }
    except Exception as e:
        print(f"Error scraping book details from {book_url}: {e}")
        return {
            'author': 'Nezjištěno',
            'genre': 'Nezjištěno',
            'pdf_url': None
        }

def main():
    print("Zacinam sber informaci o knihach...")
    
    # Get all book links
    books = scrape_book_list()
    print(f"Nalezeno {len(books)} knih\n")
    
    # Prepare output file
    output_file = "books_info.txt"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("Rozbory literarnich del - Seznam knih\n")
        f.write("=" * 80 + "\n")
        f.write("Format: Nazev knihy, Autor, Zanr - PDF URL\n")
        f.write("=" * 80 + "\n\n")
        
        for i, book in enumerate(books, 1):
            print(f"[{i}/{len(books)}] Zpracovavam: {book['title']}")
            
            # Get details for each book
            details = scrape_book_details(book['url'])
            
            # Format output
            author = details['author']
            genre = details['genre']
            pdf_url = details['pdf_url'] if details['pdf_url'] else "PDF nenalezeno"
            
            line = f"{book['title']}, {author}, {genre} - {pdf_url}\n"
            f.write(line)
            
            # Be polite to the server
            time.sleep(0.5)
        
        print(f"\nHotovo! Vysledky ulozeny do: {output_file}")
        print(f"Celkem zpracovano: {len(books)} knih")

if __name__ == "__main__":
    main()
