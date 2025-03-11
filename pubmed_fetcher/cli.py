import argparse
import csv
from pubmed_fetcher.fetch import search_pubmed, fetch_pubmed_details

def main():
    parser = argparse.ArgumentParser(description="Fetch research papers from PubMed.")
    parser.add_argument("query", type=str, help="PubMed search query.")
    parser.add_argument("-f", "--file", type=str, help="Output CSV filename.")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode.")
    args = parser.parse_args()

    pubmed_ids = search_pubmed(args.query)
    papers = fetch_pubmed_details(pubmed_ids)

    if not papers:
        print("No relevant papers found.")
        return

    if args.file:
            with open(args.file, "w", newline="", encoding="utf-8") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=papers[0].keys())
                writer.writeheader()
                writer.writerows(papers)
                print(f"Results saved to {args.file}")
    else:
        for paper in papers:
            print(paper)

if __name__ == "__main__":
    main()
