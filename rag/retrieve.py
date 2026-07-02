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


def retrieve_by_name(name: str):
    results = vector_db.similarity_search(name, k=1)

    if results:
        return results[0]

    return None

if __name__ == "__main__":

    query = "Java developer with leadership skills"

    results = retrieve(query)

    for i, r in enumerate(results, 1):
        print("=" * 60)
        print(f"{i}. {r['title']}")
        print(r["url"])
        print(r["content"])