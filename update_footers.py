"""
Script to update footer on all HTML pages to include privacy policy and contact links
"""
import os
import re

# Old footer pattern
old_footer_pattern = r'<footer>\s*<p>© 2025 MaturitaPortál \| Vytvořeno pro přípravu na maturitu</p>\s*</footer>'

# New footer
new_footer = '''<footer>
            <p>© 2025 MaturitaPortál | Vytvořeno pro přípravu na maturitu</p>
            <p style="margin-top: 0.5rem; font-size: 0.85rem;">
                <a href="../privacy.html" style="color: var(--text-muted);">Zásady ochrany osobních údajů</a> | 
                <a href="mailto:prasecibota@gmail.com" style="color: var(--text-muted);">Kontakt</a>
            </p>
        </footer>'''

# For root level pages (index.html, privacy.html)
new_footer_root = '''<footer>
            <p>© 2025 MaturitaPortál | Vytvořeno pro přípravu na maturitu</p>
            <p style="margin-top: 0.5rem; font-size: 0.85rem;">
                <a href="privacy.html" style="color: var(--text-muted);">Zásady ochrany osobních údajů</a> | 
                <a href="mailto:prasecibota@gmail.com" style="color: var(--text-muted);">Kontakt</a>
            </p>
        </footer>'''

# For second level pages (ict/index.html, literatura/index.html)
new_footer_one_level = '''<footer>
            <p>© 2025 MaturitaPortál | Vytvořeno pro přípravu na maturitu</p>
            <p style="margin-top: 0.5rem; font-size: 0.85rem;">
                <a href="../privacy.html" style="color: var(--text-muted);">Zásady ochrany osobních údajů</a> | 
                <a href="mailto:prasecibota@gmail.com" style="color: var(--text-muted);">Kontakt</a>
            </p>
        </footer>'''

# For third level pages (ict/hw/*.html, ict/prg/*.html, etc.)
new_footer_two_levels = '''<footer>
            <p>© 2025 MaturitaPortál | Vytvořeno pro přípravu na maturitu</p>
            <p style="margin-top: 0.5rem; font-size: 0.85rem;">
                <a href="../../privacy.html" style="color: var(--text-muted);">Zásady ochrany osobních údajů</a> | 
                <a href="mailto:prasecibota@gmail.com" style="color: var(--text-muted);">Kontakt</a>
            </p>
        </footer>'''

def update_file(filepath):
    """Update footer in a single HTML file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Skip if already updated
        if 'privacy.html' in content and 'prasecibota@gmail.com' in content:
            print(f"[OK] Already updated: {filepath}")
            return False
        
        # Determine depth level
        depth = filepath.count(os.sep) - os.getcwd().count(os.sep)
        
        if depth == 0:
            # Root level
            replacement = new_footer_root
        elif depth == 1:
            # One level deep (ict/, literatura/)
            replacement = new_footer_one_level
        else:
            # Two+ levels deep
            replacement = new_footer_two_levels
        
        # Replace footer
        new_content = re.sub(old_footer_pattern, replacement, content, flags=re.DOTALL)
        
        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"[UPDATED] {filepath}")
            return True
        else:
            print(f"[SKIP] No match found in: {filepath}")
            return False
            
    except Exception as e:
        print(f"[ERROR] updating {filepath}: {e}")
        return False

def main():
    """Update all HTML files"""
    updated_count = 0
    total_count = 0
    
    # Walk through all directories
    for root, dirs, files in os.walk('.'):
        # Skip hidden directories and python cache
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
        
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                total_count += 1
                if update_file(filepath):
                    updated_count += 1
    
    print(f"\n{'='*50}")
    print(f"Summary: Updated {updated_count} out of {total_count} HTML files")
    print(f"{'='*50}")

if __name__ == '__main__':
    main()
