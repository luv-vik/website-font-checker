# 🕵️ Font Usage Scanner

A Python-based tool that scans an entire website and extracts **font usage details** — including font family, size, and weight — for all visible text elements across multiple pages.  
It automatically crawls internal links and generates a clean mapping of text → font style.

---

## 🚀 Features

- Crawl entire website (configurable number of pages)
- Extracts **font-family**, **font-size**, and **font-weight**
- Maps extracted data to HTML element & text
- Saves results to `font_usage_report.json`
- Works even for **JavaScript-rendered websites** (using Playwright)

---

## 🧩 Example Use Case

You can use this script to:
- Audit typography usage across your or your client’s website
- Ensure consistent font styles
- Detect mismatched or legacy fonts

---

## ⚙️ Setup Guide (GitHub Codespace or Local)

### 1️⃣ Open Codespace
- Open your GitHub repository → **Code → Codespaces → New Codespace**

### 2️⃣ Create Script File
Create a file named `font_checker.py` and paste the script from [`font_checker.py`](./font_checker.py).

### 3️⃣ Install Dependencies
Run the following commands in your Codespace terminal:
```bash
pip install playwright beautifulsoup4
playwright install
