def calculate_retrieval_metrics(
    retrieved_documents,
    expected_source,
    expected_pages,
    top_k=3
):
    retrieved_documents = retrieved_documents[:top_k]

    relevant_count = 0
    first_relevant_rank = None

    for rank, (document, _) in enumerate(
        retrieved_documents,
        start=1
    ):
        source = document.metadata.get("source")
        page = document.metadata.get("page")

        if (
            source == expected_source
            and page in expected_pages
        ):
            relevant_count += 1

            if first_relevant_rank is None:
                first_relevant_rank = rank

    hit = 1 if relevant_count > 0 else 0

    if first_relevant_rank is not None:
        reciprocal_rank = 1 / first_relevant_rank
    else:
        reciprocal_rank = 0

    precision = relevant_count / top_k

    return {
        "hit": hit,
        "reciprocal_rank": reciprocal_rank,
        "precision": precision
    }