// Maturita Portal - Global JavaScript
// Adds interactive elements and animations

// ========================================
// THEME TOGGLE SYSTEM
// ========================================

// Initialize theme before DOM loads to prevent flash
(function () {
    const savedTheme = localStorage.getItem('theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;

    // Apply saved theme or system preference
    if (savedTheme) {
        document.documentElement.setAttribute('data-theme', savedTheme);
    } else if (!prefersDark) {
        document.documentElement.setAttribute('data-theme', 'light');
    }
    // Dark theme is default (no data-theme attribute needed)
})();

document.addEventListener('DOMContentLoaded', () => {
    // ========================================
    // THEME TOGGLE FUNCTIONALITY
    // ========================================

    const createThemeToggle = () => {
        // Create the toggle button
        const toggle = document.createElement('button');
        toggle.className = 'theme-toggle';
        toggle.setAttribute('aria-label', 'Přepnout světlý/tmavý režim');
        toggle.setAttribute('title', 'Přepnout téma');
        toggle.id = 'theme-toggle';

        // Create inner elements
        toggle.innerHTML = `
            <span class="theme-toggle-stars">✦ ✧</span>
            <span class="theme-toggle-clouds">☁️</span>
            <span class="theme-toggle-slider"></span>
        `;

        // Find the header and insert the toggle
        const header = document.querySelector('header');
        if (header) {
            const nav = header.querySelector('nav');
            if (nav) {
                // Insert after nav
                nav.after(toggle);
            } else {
                header.appendChild(toggle);
            }
        }

        // Add click handler
        toggle.addEventListener('click', toggleTheme);
    };

    const toggleTheme = () => {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'light' ? 'dark' : 'light';

        // Apply new theme
        if (newTheme === 'dark') {
            document.documentElement.removeAttribute('data-theme');
        } else {
            document.documentElement.setAttribute('data-theme', newTheme);
        }

        // Save preference
        localStorage.setItem('theme', newTheme);

        // Announce change for screen readers
        const announcement = newTheme === 'light' ? 'Světlý režim aktivován' : 'Tmavý režim aktivován';
        announceForScreenReader(announcement);
    };

    const announceForScreenReader = (message) => {
        const announcement = document.createElement('div');
        announcement.setAttribute('role', 'status');
        announcement.setAttribute('aria-live', 'polite');
        announcement.setAttribute('aria-atomic', 'true');
        announcement.style.cssText = 'position: absolute; left: -10000px; width: 1px; height: 1px; overflow: hidden;';
        announcement.textContent = message;
        document.body.appendChild(announcement);

        setTimeout(() => announcement.remove(), 1000);
    };

    // Listen for system theme changes
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
        // Only apply if user hasn't set a preference
        if (!localStorage.getItem('theme')) {
            if (e.matches) {
                document.documentElement.removeAttribute('data-theme');
            } else {
                document.documentElement.setAttribute('data-theme', 'light');
            }
        }
    });

    // Initialize theme toggle
    createThemeToggle();

    // ========================================
    // DYNAMIC COUNTERS FOR HOME PAGE
    // ========================================

    const loadDynamicCounts = async () => {
        const literaturaCountEl = document.getElementById('literatura-count');
        const ictCountEl = document.getElementById('ict-count');

        // Only run on the home page where these elements exist
        if (!literaturaCountEl && !ictCountEl) return;

        // Load literatura count
        if (literaturaCountEl) {
            try {
                const response = await fetch('literatura/index.html');
                if (response.ok) {
                    const html = await response.text();
                    // Parse the books array - count objects in the array
                    const booksMatch = html.match(/const\s+books\s*=\s*\[[\s\S]*?\];/);
                    if (booksMatch) {
                        // Count the number of book objects (filename entries)
                        const filenameCount = (booksMatch[0].match(/"filename":/g) || []).length;
                        const bookWord = filenameCount === 1 ? 'kniha' :
                            (filenameCount >= 2 && filenameCount <= 4) ? 'knihy' : 'knih';
                        literaturaCountEl.textContent = `${filenameCount} ${bookWord}`;
                    } else {
                        literaturaCountEl.textContent = '33 knih'; // Fallback
                    }
                } else {
                    literaturaCountEl.textContent = '33 knih'; // Fallback
                }
            } catch (error) {
                // Fallback for file:// protocol or other errors
                literaturaCountEl.textContent = '33 knih';
                console.log('literatura count fallback:', error.message);
            }
        }

        // Load ICT count
        if (ictCountEl) {
            try {
                const response = await fetch('ict/index.html');
                if (response.ok) {
                    const html = await response.text();
                    // Count topic-card links (excluding the index.html itself)
                    const topicMatches = html.match(/class="topic-card/g) || [];
                    const topicCount = topicMatches.length;
                    const topicWord = topicCount === 1 ? 'okruh' :
                        (topicCount >= 2 && topicCount <= 4) ? 'okruhy' : 'okruhů';
                    ictCountEl.textContent = `${topicCount} ${topicWord}`;
                } else {
                    ictCountEl.textContent = '5 okruhů'; // Fallback
                }
            } catch (error) {
                // Fallback for file:// protocol or other errors
                ictCountEl.textContent = '5 okruhů';
                console.log('ICT count fallback:', error.message);
            }
        }
    };

    loadDynamicCounts();

    // ========================================
    // FOOTER DISCLAIMER
    // ========================================

    // Universal Footer Disclaimer
    // Automatically adds AI disclaimer to all footer elements
    const addFooterDisclaimer = () => {
        const footers = document.querySelectorAll('footer');
        footers.forEach(footer => {
            // Check if disclaimer already exists
            if (!footer.querySelector('.ai-disclaimer')) {
                const disclaimer = document.createElement('p');
                disclaimer.className = 'ai-disclaimer';
                disclaimer.style.cssText = 'margin-top: 0.5rem; font-size: 0.85rem; color: var(--text-muted); max-width: 800px; margin-left: auto; margin-right: auto;';
                disclaimer.innerHTML = '⚠️ Upozornění: Obsah tohoto portálu byl částečně generován umělou inteligencí. Vždy si ověřujte správnost informací z oficiálních zdrojů a učebnic.';
                footer.appendChild(disclaimer);
            }
        });
    };

    addFooterDisclaimer();

    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Add animation classes on scroll
    const animateOnScroll = () => {
        const elements = document.querySelectorAll('.glass-panel, .card, .topic-card');

        elements.forEach(el => {
            const rect = el.getBoundingClientRect();
            const isVisible = rect.top < window.innerHeight - 100;

            if (isVisible && !el.classList.contains('animate-fade-in')) {
                el.classList.add('animate-fade-in');
            }
        });
    };

    window.addEventListener('scroll', animateOnScroll);
    animateOnScroll(); // Initial check

    // ========================================
    // COOKIE CONSENT BANNER
    // ========================================

    const initCookieConsent = () => {
        // Check if user already accepted cookies
        if (localStorage.getItem('cookieConsent') === 'accepted') {
            return; // Don't show banner
        }

        // Create banner element
        const banner = document.createElement('div');
        banner.id = 'cookie-consent';
        banner.className = 'cookie-consent';
        banner.innerHTML = `
            <div class="cookie-content">
                <span class="cookie-icon">🍪</span>
                <p class="cookie-text">
                    Tento web používá cookies pro zobrazování personalizovaných reklam prostřednictvím Google AdSense.
                </p>
                <div class="cookie-buttons">
                    <a href="privacy.html" class="cookie-btn cookie-btn-secondary">Více informací</a>
                    <button id="cookie-accept" class="cookie-btn cookie-btn-primary">Rozumím</button>
                </div>
            </div>
        `;

        // Fix privacy.html path based on current directory
        const currentPath = window.location.pathname;
        const privacyLink = banner.querySelector('a[href="privacy.html"]');

        if (currentPath.includes('/ict/') || currentPath.includes('/literatura/')) {
            if (currentPath.split('/').filter(p => p).length >= 3) {
                // We're in a subdirectory like /ict/hw/
                privacyLink.href = '../../privacy.html';
            } else {
                // We're in /ict/ or /literatura/
                privacyLink.href = '../privacy.html';
            }
        }

        // Add styles
        const styles = document.createElement('style');
        styles.textContent = `
            .cookie-consent {
                position: fixed;
                bottom: 0;
                left: 0;
                right: 0;
                background: rgba(20, 20, 30, 0.95);
                backdrop-filter: blur(20px);
                -webkit-backdrop-filter: blur(20px);
                border-top: 1px solid rgba(255, 255, 255, 0.1);
                padding: 1rem 1.5rem;
                z-index: 9999;
                animation: slideUp 0.4s ease;
                box-shadow: 0 -4px 30px rgba(0, 0, 0, 0.3);
            }

            [data-theme="light"] .cookie-consent {
                background: rgba(248, 249, 252, 0.95);
                border-top-color: rgba(0, 0, 0, 0.08);
                box-shadow: 0 -4px 30px rgba(0, 0, 0, 0.1);
            }

            @keyframes slideUp {
                from {
                    transform: translateY(100%);
                    opacity: 0;
                }
                to {
                    transform: translateY(0);
                    opacity: 1;
                }
            }

            .cookie-content {
                max-width: 1200px;
                margin: 0 auto;
                display: flex;
                align-items: center;
                gap: 1rem;
                flex-wrap: wrap;
            }

            .cookie-icon {
                font-size: 1.5rem;
                flex-shrink: 0;
            }

            .cookie-text {
                flex: 1;
                margin: 0;
                font-size: 0.9rem;
                color: var(--text-secondary, #a0a0b0);
                min-width: 200px;
            }

            .cookie-buttons {
                display: flex;
                gap: 0.75rem;
                flex-shrink: 0;
            }

            .cookie-btn {
                padding: 0.5rem 1.25rem;
                border-radius: 8px;
                font-size: 0.85rem;
                font-weight: 500;
                cursor: pointer;
                transition: all 0.2s ease;
                text-decoration: none;
                border: none;
                font-family: inherit;
            }

            .cookie-btn-secondary {
                background: transparent;
                color: var(--text-secondary, #a0a0b0);
                border: 1px solid rgba(255, 255, 255, 0.2);
            }

            [data-theme="light"] .cookie-btn-secondary {
                border-color: rgba(0, 0, 0, 0.15);
            }

            .cookie-btn-secondary:hover {
                background: rgba(255, 255, 255, 0.1);
                color: var(--text-primary, #ffffff);
            }

            [data-theme="light"] .cookie-btn-secondary:hover {
                background: rgba(0, 0, 0, 0.05);
            }

            .cookie-btn-primary {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
            }

            .cookie-btn-primary:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
            }

            @media (max-width: 600px) {
                .cookie-content {
                    flex-direction: column;
                    text-align: center;
                }
                
                .cookie-buttons {
                    width: 100%;
                    justify-content: center;
                }
            }
        `;

        document.head.appendChild(styles);
        document.body.appendChild(banner);

        // Handle accept button
        document.getElementById('cookie-accept').addEventListener('click', () => {
            localStorage.setItem('cookieConsent', 'accepted');
            banner.style.animation = 'slideUp 0.3s ease reverse';
            setTimeout(() => banner.remove(), 300);
        });
    };

    initCookieConsent();

    // Console message
    console.log('%c✨ Maturita Portál', 'font-size: 20px; font-weight: bold; color: #667eea;');
    console.log('%cPřiprav se na maturitu s profesionálně zpracovanými materiály!', 'font-size: 12px; color: #a0a0b0;');
});
