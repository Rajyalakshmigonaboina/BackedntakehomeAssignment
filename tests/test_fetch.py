import pytest
from pubmed_fetcher.fetch import search_pubmed

def test_search_pubmed():
    results = search_pubmed("cancer", max_results=5)
    assert isinstance(results, list)
    assert len(results) > 0
