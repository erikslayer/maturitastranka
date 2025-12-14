# Maturita Portál - Implementation Plan

## 📋 Project Overview

A professional graduation study portal for **Literatura** (Literature) and **ICT** (Information and Communication Technology) subjects, built with HTML, CSS, and JavaScript.

---

## 🏗️ Project Structure

```
maturitastranka/
├── index.html                  # ✅ Main portal homepage
├── styles.css                  # ✅ Global stylesheet (professional dark theme)
├── script.js                   # Global JavaScript
├── extract_urls.py             # ✅ Python script to extract PDF URLs
├── book_urls.txt               # Generated list of book URLs
│
├── literatura/                 # Literature section
│   ├── index.html              # ✅ List of all books
│   ├── saturnin.html           # ✅ Book page with content
│   ├── rur.html                # ✅ Book page with content
│   ├── gatsby.html             # ✅ Book page with content
│   ├── lakomec.html            # ✅ Book page with content
│   ├── na-zapadni-fronte-klid.html  # ✅ Book page with content
│   ├── o-mysich-a-lidech.html  # ✅ Book page with content
│   ├── maly-princ.html         # ✅ Book page with content
│   └── text/                   # Source text files
│
└── ict/                        # ICT section
    ├── index.html              # ✅ ICT main page with topic cards
    ├── psi.html                # ✅ Počítačové sítě (placeholder)
    ├── hw.html                 # ✅ Hardware (placeholder)
    ├── os.html                 # ✅ Operační systémy (placeholder)
    ├── prg.html                # ✅ Programování (placeholder)
    └── db.html                 # ✅ Databáze (placeholder)
```

---

## 📚 Literatura Section

### Books (with source PDFs):

| # | Title | Author | Slug | PDF Source |
|---|-------|--------|------|------------|
| 1 | Saturnin | Zdeněk Jirotka | saturnin | [PDF](https://www.milujemecestinu.cz/files/tournaments/112/Zdenek_Jirotka_Saturnin.pdf) |
| 2 | R.U.R. | Karel Čapek | rur | [PDF](https://www.milujemecestinu.cz/files/tournaments/29/Karel_Capek_-_R._U._R..pdf) |
| 3 | Velký Gatsby | F. Scott Fitzgerald | gatsby | [PDF](https://www.milujemecestinu.cz/files/tournaments/83/Francis_Scott_Fitzgerald_Velky_Gatsby.pdf) |
| 4 | Lakomec | Molière | lakomec | [PDF](https://www.milujemecestinu.cz/files/tournaments/131/Moliere_Lakomec.pdf) |
| 5 | Na západní frontě klid | E. M. Remarque | na-zapadni-fronte-klid | [PDF](https://www.milujemecestinu.cz/files/tournaments/157/Erich_Maria_Remarque_Na_zapadni_fronte_klid.pdf) |
| 6 | O myších a lidech | John Steinbeck | o-mysich-a-lidech | [PDF](https://www.milujemecestinu.cz/files/tournaments/68/John_Steinbeck_O_mysich_a_lidech.pdf) |
| 7 | Malý princ | A. de Saint-Exupéry | maly-princ | [PDF](https://www.milujemecestinu.cz/files/tournaments/81/Antoine_de_Saint_Exupery_Maly_princ.pdf) |

---

## 💻 ICT Section

### Topics (to be expanded):

| Abbreviation | Full Name (CZ) | Description |
|--------------|----------------|-------------|
| PSI | Počítačové sítě | OSI model, TCP/IP, protocols, network devices |
| HW | Hardware | CPU, memory, motherboard, peripherals |
| OS | Operační systémy | Process management, file systems, Windows/Linux |
| PRG | Programování | Algorithms, data structures, OOP |
| DB | Databáze | SQL, relational databases, normalization |

---

## 🎨 Design Features

- **Dark Theme**: Professional dark mode with glassmorphism effects
- **Modern Typography**: Inter + Outfit fonts from Google Fonts
- **Smooth Gradients**: Pink/yellow for Literatura, Green/cyan for ICT
- **Animations**: Fade-in animations, hover effects, smooth transitions
- **Responsive**: Mobile-first design with adaptive layouts
- **Accessibility**: Proper heading hierarchy, semantic HTML

---

## ✅ Completed Steps

1. [x] Create project structure
2. [x] Design and implement global stylesheet (`styles.css`)
3. [x] Create main portal homepage (`index.html`)
4. [x] Create Literatura index page with book cards
5. [x] Create ICT index page with topic cards
6. [x] Create ICT section placeholder pages (PSI, HW, OS, PRG, DB)
7. [x] Create Python URL extractor script
8. [x] Book pages already exist with content

---

## 🔜 Next Steps

1. [ ] Add more books to Literatura section (as provided)
2. [ ] Populate ICT topics with actual content:
   - [ ] PSI - Počítačové sítě topics
   - [ ] HW - Hardware topics
   - [ ] OS - Operační systémy topics
   - [ ] PRG - Programování topics
   - [ ] DB - Databáze topics
3. [ ] Add search functionality
4. [ ] Add dark/light mode toggle
5. [ ] Add print-friendly styles

---

## 🛠️ Technical Notes

- Run `python extract_urls.py` to generate `book_urls.txt`
- All pages use relative paths for linking
- Styles are shared via `../styles.css` from subfolders
- No build tools required - pure HTML/CSS/JS

---

*Last updated: December 2025*
