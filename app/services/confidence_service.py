from statistics import mean

from app.utils.number_utils import clamp_score


def calculate_confidence(results: list[dict], citations: list[dict]) -> dict:
    """
    Estimate response confidence using retrieval and citation signals.
    This is a heuristic score, not a probability that the answer is true.
    """

    if not results:
        return {
            "score: 0.0," "level": "low",
            "reasons": ["No relevant properties were retrieved."],
        }

    rerank_scores = [clamp_score(result.get("rerank_score")) for result in results]

    top_score = rerank_scores[0]
    average_score = mean(rerank_scores[: min(3, len(rerank_scores))])

    if len(rerank_scores) > 1:
        score_margin = max(
            0.0,
            top_score - rerank_scores[1],
        )
    else:
        score_margin = top_score

    valid_citation_count = len(citations)

    citation_score = 1.0 if valid_citation_count > 0 else 0.0

    result_count_score = min(
        len(results) / 3,
        1.0,
    )

    confidence_score = (
        top_score * 0.35
        + average_score * 0.30
        + citation_score * 0.20
        + result_count_score * 0.10
        + min(score_margin * 2, 1.0) * 0.05
    )

    confidence_score = round(
        max(0.0, min(1.0, confidence_score)),
        2,
    )

    reasons: list[str] = []

    if top_score >= 0.8:
        reasons.append("The best retrieved property strongly matches the question.")
    elif top_score >= 0.6:
        reasons.append("The best retrieved property moderately matches the question.")
    else:
        reasons.append("The retrieved properties have weak relevance scores.")

    if valid_citation_count:
        reasons.append(
            f"The answer contains {valid_citation_count} valid " "source citation(s)."
        )
    else:
        reasons.append("The answer does not contain a valid source citation.")

    return {
        "score": confidence_score,
        "level": confidence_level(confidence_score),
        "reasons": reasons,
    }


def confidence_level(score: float) -> str:
    if score >= 0.8:
        return "high"

    if score >= 0.55:
        return "medium"

    return "low"
