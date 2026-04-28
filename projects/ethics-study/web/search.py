"""
Search logic for Ethics Study Guide.
Provides unified full-text search across claims, keywords, and works indices.
"""

from elasticsearch import Elasticsearch


def get_thinker_name_map(es: Elasticsearch) -> dict[str, str]:
    """Return a mapping of thinker_id -> name from ethics-thinkers index."""
    try:
        resp = es.search(
            index="ethics-thinkers",
            body={
                "size": 200,
                "_source": ["id", "name"],
            },
        )
        name_map: dict[str, str] = {}
        for hit in resp["hits"]["hits"]:
            src = hit["_source"]
            tid = src.get("id") or hit["_id"]
            name_map[tid] = src.get("name", tid)
        return name_map
    except Exception:
        return {}


def search_claims(es: Elasticsearch, query: str, size: int = 30) -> list[dict]:
    """Full-text search across ethics-claims index."""
    try:
        resp = es.search(
            index="ethics-claims",
            body={
                "size": size,
                "query": {
                    "multi_match": {
                        "query": query,
                        "fields": ["claim^3", "explanation^2", "argument", "counterpoint", "keywords"],
                        "type": "best_fields",
                        "fuzziness": "AUTO",
                    }
                },
                "_source": [
                    "id", "thinker_id", "work_id", "source_detail",
                    "claim", "explanation", "keywords",
                ],
                "highlight": {
                    "fields": {
                        "claim": {"number_of_fragments": 1, "fragment_size": 200},
                        "explanation": {"number_of_fragments": 1, "fragment_size": 150},
                    },
                    "pre_tags": ["<mark>"],
                    "post_tags": ["</mark>"],
                },
            },
        )
        results = []
        for hit in resp["hits"]["hits"]:
            src = hit["_source"]
            src.setdefault("id", hit["_id"])
            src["_type"] = "claim"
            src["_score"] = hit.get("_score", 0)
            # Use highlight if available
            highlights = hit.get("highlight", {})
            if "claim" in highlights:
                src["_highlight_claim"] = highlights["claim"][0]
            if "explanation" in highlights:
                src["_highlight_explanation"] = highlights["explanation"][0]
            results.append(src)
        return results
    except Exception:
        return []


def search_keywords(es: Elasticsearch, query: str, size: int = 20) -> list[dict]:
    """Full-text search across ethics-keywords index."""
    try:
        resp = es.search(
            index="ethics-keywords",
            body={
                "size": size,
                "query": {
                    "multi_match": {
                        "query": query,
                        "fields": ["term^3", "term_en^2", "definition"],
                        "type": "best_fields",
                        "fuzziness": "AUTO",
                    }
                },
                "_source": ["id", "thinker_id", "term", "term_en", "definition", "related_terms"],
                "highlight": {
                    "fields": {
                        "term": {"number_of_fragments": 1},
                        "definition": {"number_of_fragments": 1, "fragment_size": 150},
                    },
                    "pre_tags": ["<mark>"],
                    "post_tags": ["</mark>"],
                },
            },
        )
        results = []
        for hit in resp["hits"]["hits"]:
            src = hit["_source"]
            src.setdefault("id", hit["_id"])
            src["_type"] = "keyword"
            src["_score"] = hit.get("_score", 0)
            highlights = hit.get("highlight", {})
            if "definition" in highlights:
                src["_highlight_definition"] = highlights["definition"][0]
            results.append(src)
        return results
    except Exception:
        return []


def search_works(es: Elasticsearch, query: str, size: int = 20) -> list[dict]:
    """Full-text search across ethics-works index."""
    try:
        resp = es.search(
            index="ethics-works",
            body={
                "size": size,
                "query": {
                    "multi_match": {
                        "query": query,
                        "fields": ["title^3", "significance^2", "key_concepts"],
                        "type": "best_fields",
                        "fuzziness": "AUTO",
                    }
                },
                "_source": ["id", "thinker_id", "title", "title_original", "year", "significance", "key_concepts"],
                "highlight": {
                    "fields": {
                        "title": {"number_of_fragments": 1},
                        "significance": {"number_of_fragments": 1, "fragment_size": 150},
                    },
                    "pre_tags": ["<mark>"],
                    "post_tags": ["</mark>"],
                },
            },
        )
        results = []
        for hit in resp["hits"]["hits"]:
            src = hit["_source"]
            src.setdefault("id", hit["_id"])
            src["_type"] = "work"
            src["_score"] = hit.get("_score", 0)
            highlights = hit.get("highlight", {})
            if "significance" in highlights:
                src["_highlight_significance"] = highlights["significance"][0]
            results.append(src)
        return results
    except Exception:
        return []


def search_all(es: Elasticsearch, query: str, size: int = 50) -> dict:
    """
    Search claims, keywords, and works simultaneously.
    Returns unified result dict with thinker names resolved.
    """
    if not query or not query.strip():
        return {
            "query": query,
            "total": 0,
            "claims": [],
            "keywords": [],
            "works": [],
            "thinker_names": {},
        }

    # Fetch thinker name map for resolving IDs
    thinker_names = get_thinker_name_map(es)

    claims = search_claims(es, query, size=min(size, 30))
    keywords = search_keywords(es, query, size=min(size, 20))
    works = search_works(es, query, size=min(size, 20))

    # Attach thinker names to each result
    for item in claims + keywords + works:
        tid = item.get("thinker_id", "")
        item["thinker_name"] = thinker_names.get(tid, tid)

    total = len(claims) + len(keywords) + len(works)

    return {
        "query": query,
        "total": total,
        "claims": claims,
        "keywords": keywords,
        "works": works,
        "thinker_names": thinker_names,
    }
