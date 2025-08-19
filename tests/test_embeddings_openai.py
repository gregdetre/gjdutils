import os
import pytest

from gjdutils.embeddings_openai import get_openai_embeddings, compare_embedding_query


@pytest.mark.skipif(
    not os.environ.get("OPENAI_API_KEY"),
    reason="Requires OPENAI_API_KEY to call OpenAI embeddings API",
)
def test_cosine_similarity_three_sentences():
    texts = [
        "The quick brown fox jumps over the lazy dog.",
        "A quick brown fox leaps over a lazy dog.",  # semantically similar
        "The stock market closed higher today after strong earnings.",
    ]

    embs, extra = get_openai_embeddings(texts, model="text-embedding-3-small")

    # Compare sentence 0 vs others (list inputs)
    scores, _ = compare_embedding_query(embs[0], embs, metric="cosine")
    # scores[0] is self-similarity (~1.0). Interested in indices 1 and 2.
    assert scores[1] > scores[2], (
        f"Expected similar sentence to have higher cosine similarity: {scores[1]=} vs {scores[2]=}"
    )


