import requests
from bs4 import BeautifulSoup, Tag
import json
import sys

BASE_URL = "https://crowdworks.jp"
JOBS_URL = sys.argv[1] if len(sys.argv) > 1 else "https://crowdworks.jp/public/jobs/search?category_id=226&order=new"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def scrape_jobs():
    resp = requests.get(JOBS_URL, headers=headers)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    job_list = []
    # Find all <ul> and pick the one with job <li>s
    for ul in soup.find_all("ul"):
        if not isinstance(ul, Tag):
            continue
        lis = [li for li in ul.find_all("li", recursive=False) if isinstance(li, Tag)]
        if not lis:
            continue
        # Heuristic: check if first <li> has <h3> with <a>
        first_li = lis[0]
        h3 = first_li.find("h3") if isinstance(first_li, Tag) else None
        a = h3.find("a") if h3 and isinstance(h3, Tag) else None
        if not (h3 and a and isinstance(a, Tag)):
            continue
        # This is likely the job list
        for li in lis:
            # Title and link: first <a> inside <h3>
            title, link = None, None
            h3 = li.find("h3") if isinstance(li, Tag) else None
            if h3 and isinstance(h3, Tag):
                a = h3.find("a")
                if a and isinstance(a, Tag) and a.has_attr("href"):
                    title = a.get_text(strip=True)
                    href = a["href"]
                    if isinstance(href, str):
                        link = BASE_URL + href
            # Category: first <a> with '/public/jobs/category/' in href
            category = None
            for cat_a in li.find_all("a") if isinstance(li, Tag) else []:
                if not isinstance(cat_a, Tag):
                    continue
                href = cat_a.get("href", "")
                if isinstance(href, str) and "/public/jobs/category/" in href:
                    category = cat_a.get_text(strip=True)
                    break
            # Description: first <p> in <li>
            description = None
            desc_p = li.find("p") if isinstance(li, Tag) else None
            if desc_p and isinstance(desc_p, Tag):
                description = desc_p.get_text(strip=True)
            # Reward: first <b> containing '円' or a digit
            reward = None
            for b in li.find_all("b") if isinstance(li, Tag) else []:
                if not isinstance(b, Tag):
                    continue
                b_text = b.get_text()
                if "円" in b_text or any(c.isdigit() for c in b_text):
                    reward = b_text.strip().replace("\n", " ").replace("  ", " ")
                    break
            # Contract count: <b> after '契約数'
            contract = None
            for span in li.find_all("span") if isinstance(li, Tag) else []:
                if not isinstance(span, Tag):
                    continue
                if "契約数" in span.get_text():
                    b = span.find("b")
                    if b and isinstance(b, Tag):
                        contract = b.get_text(strip=True)
                    break
            # Deadline: <b> after 'あと'
            deadline = None
            for span in li.find_all("span") if isinstance(li, Tag) else []:
                if not isinstance(span, Tag):
                    continue
                if "あと" in span.get_text():
                    b = span.find("b")
                    if b and isinstance(b, Tag):
                        deadline = b.get_text(strip=True)
                    break
            job_list.append({
                "title": title,
                "link": link,
                "category": category,
                "description": description,
                "reward": reward,
                "contract_count": contract,
                "deadline": deadline
            })
        break  # Only process the first matching <ul>
    return job_list

if __name__ == "__main__":
    jobs = scrape_jobs()
    print(json.dumps(jobs, ensure_ascii=False, indent=2))

