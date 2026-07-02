from rag.index import vector_db


from rag.index import vector_db


def retrieve(query: str, k: int = 5):
    results = vector_db.similarity_search(query, k=k)

    seen = set()
    recommendations = []

    for d in results:

        if d["url"] in seen:
            continue

        seen.add(d["url"])

        recommendations.append({
            "title": d["title"],
            "url": d["url"],
            "content": d["content"],
            "test_type": d.get("test_type", "Assessment")
        })

        if len(recommendations) >= k:
            break

    return recommendations
