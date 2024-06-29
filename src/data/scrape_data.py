import json
import os
import requests
import time

from typing import Dict, List, Optional

from bs4 import BeautifulSoup


URL = "https://resources.allsetlearning.com/chinese/grammar/"

BASE_URL = "https://resources.allsetlearning.com"


def get_content(url: str) -> BeautifulSoup:
    """
    Request web page content and parse into a BeautifulSoup object.
    """
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        if response.status_code != 200:
            print("Error fetching page")
            exit()
        else:
            content = response.content
    except requests.exceptions.ConnectionError as e:
        print(e)
        print("continuing...")

    return BeautifulSoup(content, "html.parser")


def get_all_grammar_urls() -> Dict[str, str]:
    """
    Use the base URL to fetch all hrefs to child web pages, then select
    those that are grammar URLs.
    """
    soup = get_content(f"{BASE_URL}/chinese/grammar/")

    all_hrefs = [a.get("href") for a in soup.find_all("a")]
    grammar_urls = list(
        set(
            [
                BASE_URL + href
                for href in all_hrefs
                if "/chinese/grammar/" in str(href) and "grammar_points" in str(href)
            ]
        )
    )

    grammar_hrefs = {}
    for url in grammar_urls:
        soup = get_content(url)
        tables = soup.find_all("table", attrs={"class": "wikitable"})
        for table in tables:
            table_body = table.find("tbody")

            rows = table_body.find_all("tr")
            for row in rows:
                cols = row.find_all("td")
                if not len(cols):
                    continue
                href = cols[0].find("a").get("href")
                key = cols[0].text + " § " + cols[1].text
                if "/gramwiki/" not in href:
                    # exclude /gramwiki/ urls as the code struggles to fetch those
                    # TODO: figure out how to get that data too
                    grammar_hrefs[key] = href

    return grammar_hrefs


def parse_relevant_content(url: str) -> List[str]:
    """
    Parse out only the text which is relevant to Chinese grammar education.
    Ignore other blocks e.g. advertisements, copyright blocks.
    """
    soup = get_content(BASE_URL + url)

    # Find all <p> tags, that don't correspond to a copyright block
    paragraphs = [x for x in soup.find_all("p") if "©" not in x.text]

    paragraph_texts = []
    for paragraph in paragraphs:
        paragraph_text = paragraph.get_text()

        # Find the next sibling <div> tag if it exists
        next_sibling = paragraph.find_next_sibling()

        if next_sibling and next_sibling.name == "div":
            if next_sibling.get("class", []) not in (["toc"], ["jiegou"]):
                div_text = next_sibling.get_text()
                paragraph_text += div_text

        paragraph_texts.append(paragraph_text)

    return paragraph_texts, soup


def save_full_html(
    text: str, filename: str, save_dir: Optional[str] = "data/chinese_grammar_html"
) -> None:
    """
    Save full html file for debugging.
    """
    if not os.path.exists(f"{save_dir}"):
        os.makedirs(f"{save_dir}")

    print(f"Saving {filename}.html...")
    with open(f"{save_dir}/{filename}.html", "w") as f:
        f.write(text)


def save_relevant_content(
    text: str, filename: str, save_dir: Optional[str] = "data/chinese_grammar_data"
) -> None:
    """
    Save parsed text file for our RAG application's retrieval.
    """
    if not os.path.exists(f"{save_dir}"):
        os.makedirs(f"{save_dir}")

    print(f"Saving {filename}.txt...")
    with open(f"{save_dir}/{filename}.txt", "w") as f:
        f.writelines(text)


if __name__ == "__main__":
    metadata = {}

    print("Fetching all grammar URLs...")
    grammar_urls = get_all_grammar_urls()
    time.sleep(0.2)

    n = len(grammar_urls)
    for i, (title, url) in enumerate(grammar_urls.items()):
        print(f"{i+1}/{n} Fetching {title}...")
        paragraph_texts, soup = parse_relevant_content(url)
        key = url.split("/")[-1]
        metadata[key] = {
            "url": BASE_URL + url,
            "title": title,
        }
        save_full_html(str(soup), key)
        save_relevant_content(paragraph_texts, key)

    # Save metadata, this will be the 'source' when retrieving
    with open("data/metadata.json", "w") as f:
        json.dump(metadata, f)
