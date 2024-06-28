import json
import os
import requests
import time

from bs4 import BeautifulSoup


URL = "https://resources.allsetlearning.com/chinese/grammar/"

BASE_URL = "https://resources.allsetlearning.com"


def get_content(url: str) -> BeautifulSoup:
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

    return BeautifulSoup(content, 'html.parser')


def get_all_urls(url) -> list[str]:
    soup = get_content(url)

    all_hrefs = [a.get('href') for a in soup.find_all('a')]
    grammar_urls = list(set([
        BASE_URL + href for href in all_hrefs if "/chinese/grammar/" in str(href) and "grammar_points" in str(href)
    ]))

    hrefs = {}
    for url in grammar_urls:
        soup = get_content(url)
        tables = soup.find_all('table', attrs={'class':'wikitable'})
        for table in tables:
            table_body = table.find('tbody')

            rows = table_body.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                if not len(cols):
                    continue
                href = cols[0].find("a").get('href')
                key = cols[0].text + " § " + cols[1].text
                hrefs[key] = href

    # filter out /gramwiki/ urls as the code struggles to fetch those
    # TODO: figure out how to get that data too
    hrefs = {
        k: v for k, v in hrefs.items()
        if "/gramwiki/" not in v
    }

    return hrefs


def get_relevant_content(url: str) -> list[str]:
    soup = get_content(BASE_URL + url)

    # Find all <p> tags, that don't correspond to a copyright block
    paragraphs = [x for x in soup.find_all("p") if "©" not in x.text]

    paragraph_texts = []
    for paragraph in paragraphs:
        paragraph_text = paragraph.get_text()
        
        # Find the next sibling <div> tag if it exists
        next_sibling = paragraph.find_next_sibling()
        
        if next_sibling and next_sibling.name == 'div':
            if next_sibling.get('class', []) not in (['toc'], ['jiegou']):
                div_text = next_sibling.get_text()
                paragraph_text += div_text

        paragraph_texts.append(paragraph_text)

    return paragraph_texts, soup


def save_full_html(text, filename, save_dir="data/chinese_grammar_html"):
    if not os.path.exists(f"{save_dir}"):
        os.makedirs(f"{save_dir}")

    print(f"Saving {filename}.html...")
    with open(f"{save_dir}/{filename}.html", 'w') as f:
        f.write(text)

def save_relevant_content(text, filename, save_dir="data/chinese_grammar_data"):
    if not os.path.exists(f"{save_dir}"):
        os.makedirs(f"{save_dir}")

    print(f"Saving {filename}.txt...")
    with open(f"{save_dir}/{filename}.txt", 'w') as f:
        f.writelines(text)

if __name__ == "__main__":
    data = []

    hrefs = get_all_urls(URL)
    time.sleep(0.2)

    n = len(hrefs)
    for i, (k, v) in enumerate(hrefs.items()):
        # # TODO: remove this line
        # if i >= 10:
        #     continue

        print(f"{i+1}/{n} Fetching {k}...")
        paragraph_texts, soup = get_relevant_content(v)
        data.append({
            "url": v,
            "name": k,
        })
        save_full_html(str(soup), v.split("/")[-1])
        save_relevant_content(paragraph_texts, v.split("/")[-1])
    
    metadata = {
        x['url'].split("/")[-1]: {
            "url": BASE_URL + x['url'],
            "title": x['name']
        }
        for x in data
    }
    with open("data/metadata.json", 'w') as f:
        json.dump(metadata, f)
