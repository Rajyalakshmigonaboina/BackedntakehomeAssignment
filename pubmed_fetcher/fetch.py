import requests
import xml.etree.ElementTree as ET
import re
from typing import List, Dict, Optional

PUBMED_SEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
PUBMED_FETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

NON_ACADEMIC_KEYWORDS = ["pharma", "biotech", "inc", "ltd", "corporation", "therapeutics"]

def search_pubmed(query: str, max_results: int = 20) -> List[str]:
    params = {"db": "pubmed", "term": query, "retmode": "json", "retmax": max_results}
    response = requests.get(PUBMED_SEARCH_URL, params=params)
    response.raise_for_status()
    data = response.json()
    return data.get("esearchresult", {}).get("idlist", [])

def fetch_pubmed_details(pubmed_ids: List[str]) -> List[Dict[str, str]]:
    if not pubmed_ids:
        return []

    params = {"db": "pubmed", "id": ",".join(pubmed_ids), "retmode": "xml"}
    response = requests.get(PUBMED_FETCH_URL, params=params)
    response.raise_for_status()

    root = ET.fromstring(response.content)
    papers = []

    for article in root.findall(".//PubmedArticle"):
        paper_data = parse_pubmed_article(article)
        if paper_data:
            papers.append(paper_data)

    return papers

def parse_pubmed_article(article) -> Optional[Dict[str, str]]:
    pmid = article.findtext(".//PMID")
    title = article.findtext(".//ArticleTitle", default="Unknown Title")
    pub_date = article.findtext(".//PubDate/Year") or "Unknown Date"

    non_academic_authors = []
    company_affiliations = []
    corresponding_email = None

    for author in article.findall(".//Author"):
        full_name = f"{author.findtext('ForeName', '')} {author.findtext('LastName', '')}".strip()
        affiliation = author.findtext("AffiliationInfo/Affiliation", default="")

        if any(keyword in affiliation.lower() for keyword in NON_ACADEMIC_KEYWORDS):
            non_academic_authors.append(full_name)
            company_affiliations.append(affiliation)

        email_match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", affiliation)
        if email_match and not corresponding_email:
            corresponding_email = email_match.group(0)

    if not company_affiliations:
        return None  # Skip if no pharma/biotech authors found

    return {
        "PubmedID": pmid,
        "Title": title,
        "Publication Date": pub_date,
        "Non-academic Author(s)": "; ".join(non_academic_authors),
        "Company Affiliation(s)": "; ".join(company_affiliations),
        "Corresponding Author Email": corresponding_email or "N/A"
    }
