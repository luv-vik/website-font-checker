import asyncio
from playwright.async_api import async_playwright
from urllib.parse import urljoin, urlparse
import re
import json
from bs4 import BeautifulSoup

visited_urls = set()
font_data = []

async def extract_fonts_from_page(page, url):
    """Extract visible text elements and their font styles from a single page."""
    try:
        await page.goto(url, timeout=60000)
        await page.wait_for_load_state("networkidle")

        # Use JS to extract text + computed style
        elements = await page.evaluate('''
            () => {
                const data = [];
                const all = document.querySelectorAll('*');
                for (const el of all) {
                    const style = window.getComputedStyle(el);
                    const text = el.innerText?.trim();
                    if (text && text.length > 1) {
                        data.push({
                            tag: el.tagName.toLowerCase(),
                            selector: el.className ? `${el.tagName.toLowerCase()}.${el.className.replace(/\\s+/g, '.')}` : el.tagName.toLowerCase(),
                            text: text.substring(0, 120),
                            font_family: style.fontFamily,
                            font_size: style.fontSize,
                            font_weight: style.fontWeight
                        });
                    }
                }
                return data;
            }
        ''')
        for e in elements:
            e["page"] = url
        font_data.extend(elements)

    except Exception as e:
        print(f"[ERROR] {url} - {e}")

async def crawl_site(base_url, max_pages=10):
    """Crawl internal links and extract font data."""
    domain = urlparse(base_url).netloc

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        async def crawl(url):
            if url in visited_urls or len(visited_urls) >= max_pages:
                return
            visited_urls.add(url)
            print(f"Scanning: {url}")

            await extract_fonts_from_page(page, url)

            # Extract links for crawling
            html = await page.content()
            soup = BeautifulSoup(html, "html.parser")
            for a in soup.find_all("a", href=True):
                href = a["href"]
                if not href.startswith("http"):
                    href = urljoin(url, href)
                if urlparse(href).netloc == domain and href not in visited_urls:
                    await crawl(href)

        await crawl(base_url)
        await browser.close()

    return font_data

async def main():
    website = input("Enter website URL: ").strip()
    results = await crawl_site(website, max_pages=5)

    print(f"\nExtracted {len(results)} font entries.")
    with open("font_usage_report.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print("✅ Font usage saved in font_usage_report.json")

if __name__ == "__main__":
    asyncio.run(main())
