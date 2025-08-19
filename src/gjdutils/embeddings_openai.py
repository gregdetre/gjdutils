from __future__ import annotations

from typing import Any, Optional, Tuple

from openai import OpenAI, NOT_GIVEN

from gjdutils.env import get_env_var


# Load once to mirror pattern in other modules
OPENAI_API_KEY = get_env_var("OPENAI_API_KEY")


def get_openai_embeddings(
    txts: list[str],
    model: str,
    dimensions: Optional[int] = None,
    client: Optional[OpenAI] = None,
    verbose: int = 0,
) -> Tuple[list[list[float]], dict[str, Any]]:
    """
    Compute OpenAI embeddings for a list of strings.

    Args:
        txts: Non-empty list of non-empty strings to embed. Order is preserved.
        model: Required embedding model name (e.g., "text-embedding-3-large" or "text-embedding-3-small").
        dimensions: Optional target dimensionality supported by the model.
        client: Optional pre-initialized OpenAI client to reuse.
        verbose: Verbosity level for basic diagnostics.

    Returns:
        (embeddings, extra) where:
            embeddings: list[list[float]] with one embedding per input, order-preserving.
            extra: dict with helpful metadata (model, dimensions, response payload, etc.).

    Raises:
        ValueError: If inputs are invalid (e.g., not a list, empty list, any non-string or empty string element).

    Example:
        >>> from gjdutils.embeddings_openai import get_openai_embeddings, convert_to_numpy
        >>> texts = ["hello", "world"]
        >>> embeddings, extra = get_openai_embeddings(texts, model="text-embedding-3-small")
        >>> arr = convert_to_numpy(embeddings)
        >>> arr.shape  # (2, 1536) for text-embedding-3-small by default
    """

    # Validate inputs early and explicitly (fail-fast)
    if not isinstance(txts, list):
        raise ValueError(f"txts must be a list[str]; got {type(txts)}")
    if len(txts) == 0:
        raise ValueError("txts must be a non-empty list")
    for i, t in enumerate(txts):
        if not isinstance(t, str):
            raise ValueError(f"All elements of txts must be str; at index {i} got {type(t)}")
        if t == "":
            raise ValueError(f"txts[{i}] is an empty string; remove or provide content")

    if not isinstance(model, str) or model.strip() == "":
        raise ValueError("model must be a non-empty str")

    # Build or reuse client
    if client is None:
        client = OpenAI(api_key=OPENAI_API_KEY)

    # Prepare kwargs to avoid sending None values
    kwargs: dict[str, Any] = {
        "model": model,
        "input": txts,
        "dimensions": dimensions if dimensions is not None else NOT_GIVEN,
    }

    resp = client.embeddings.create(**kwargs)  # type: ignore[arg-type]
    # Extract embeddings in order
    embeddings: list[list[float]] = [d.embedding for d in resp.data]  # type: ignore[attr-defined]

    # Build extra diagnostics
    extra: dict[str, Any] = {
        "model": model,
        "dimensions": dimensions,
        "num_inputs": len(txts),
        "response": resp.model_dump() if hasattr(resp, "model_dump") else resp,  # fallback
    }

    if verbose >= 1:
        dim = len(embeddings[0]) if embeddings and embeddings[0] is not None else None
        print(f"OpenAI embeddings: {len(embeddings)} items, dim={dim}, model={model}")

    return embeddings, extra


def convert_to_numpy(embeddings: list[list[float]]):
    """
    Convert list-of-list embeddings to a NumPy array (dtype=float32).

    Note: NumPy is an optional dependency. Install with `pip install gjdutils[dsci]`.
    """
    try:
        import numpy as np  # type: ignore
    except Exception as e:  # pragma: no cover - error path
        raise ImportError(
            "NumPy is required for convert_to_numpy(). Install with 'pip install gjdutils[dsci]'"
        ) from e

    return np.asarray(embeddings, dtype=np.float32)


def compare_embedding_query(
    query_embedding: list[float] | Any,
    dataset_embeddings: list[list[float]] | Any,
    metric: str = "cosine",
    verbose: int = 0,
) -> Tuple[list[float], dict[str, Any]]:
    """
    Compare a single query embedding to a dataset of embeddings.

    Inputs may be Python lists or NumPy arrays. If NumPy is available, a vectorized
    implementation is used; otherwise a pure-Python fallback is used.

    Args:
        query_embedding: The embedding vector for the query (list[float] or np.ndarray).
        dataset_embeddings: The dataset embeddings (list[list[float]] or np.ndarray).
        metric: Distance/similarity metric. Options:
            - "cosine" (default): returns cosine similarity in [-1, 1], higher is more similar
            - "dot": returns dot product
            - "euclidean": returns negative Euclidean distance (so higher is more similar)
        verbose: Verbosity for diagnostics.

    Returns:
        (scores, extra) where:
            scores: list[float] of similarity scores (higher is more similar) for each dataset vector
            extra: dict with metadata such as the metric used and dimensionalities
    """

    # Try NumPy path first
    try:
        import numpy as np  # type: ignore

        q = np.asarray(query_embedding, dtype=np.float32).reshape(-1)
        X = np.asarray(dataset_embeddings, dtype=np.float32)
        if X.ndim != 2:
            raise ValueError("dataset_embeddings must be 2D (N, D)")
        if q.ndim != 1:
            raise ValueError("query_embedding must be 1D (D,)")
        if X.shape[1] != q.shape[0]:
            raise ValueError(f"Dim mismatch: query dim {q.shape[0]} vs dataset dim {X.shape[1]}")

        if metric == "cosine":
            qn = q / (np.linalg.norm(q) + 1e-12)
            Xn = X / (np.linalg.norm(X, axis=1, keepdims=True) + 1e-12)
            sims = Xn @ qn  # (N,)
            scores = sims.astype(np.float32).tolist()
        elif metric == "dot":
            scores = (X @ q).astype(np.float32).tolist()
        elif metric == "euclidean":
            diff = X - q
            dists = np.sqrt(np.sum(diff * diff, axis=1))
            scores = (-dists).astype(np.float32).tolist()  # higher is better (less distance)
        else:
            raise ValueError(f"Unknown metric: {metric}")

        extra = {
            "metric": metric,
            "query_dim": int(q.shape[0]),
            "num_dataset": int(X.shape[0]),
            "dataset_dim": int(X.shape[1]),
        }
        if verbose >= 1:
            print(f"Compared query against {extra['num_dataset']} embeddings using {metric}")
        return scores, extra

    except ImportError:
        # Pure-Python fallback
        def dot(a: list[float], b: list[float]) -> float:
            return sum(x * y for x, y in zip(a, b))

        def norm(a: list[float]) -> float:
            return sum(x * x for x in a) ** 0.5

        if not isinstance(query_embedding, list) or not all(isinstance(x, (int, float)) for x in query_embedding):
            raise ValueError("query_embedding must be a list[float] when NumPy is unavailable")
        if not isinstance(dataset_embeddings, list) or not all(isinstance(v, list) for v in dataset_embeddings):
            raise ValueError("dataset_embeddings must be a list[list[float]] when NumPy is unavailable")
        if len(dataset_embeddings) == 0:
            return [], {"metric": metric, "num_dataset": 0, "query_dim": len(query_embedding), "dataset_dim": 0}
        d = len(query_embedding)
        if any(len(v) != d for v in dataset_embeddings):
            raise ValueError("All dataset embeddings must have the same dimensionality as the query")

        if metric == "cosine":
            qn = norm(query_embedding) + 1e-12
            scores = [dot(query_embedding, v) / (qn * (norm(v) + 1e-12)) for v in dataset_embeddings]
        elif metric == "dot":
            scores = [dot(query_embedding, v) for v in dataset_embeddings]
        elif metric == "euclidean":
            def dist(a: list[float], b: list[float]) -> float:
                return sum((x - y) ** 2 for x, y in zip(a, b)) ** 0.5
            scores = [-dist(query_embedding, v) for v in dataset_embeddings]
        else:
            raise ValueError(f"Unknown metric: {metric}")

        extra = {
            "metric": metric,
            "query_dim": d,
            "num_dataset": len(dataset_embeddings),
            "dataset_dim": d,
        }
        if verbose >= 1:
            print(f"Compared query against {extra['num_dataset']} embeddings using {metric} (no NumPy)")
        return scores, extra


__all__ = [
    "get_openai_embeddings",
    "convert_to_numpy",
    "compare_embedding_query",
]


