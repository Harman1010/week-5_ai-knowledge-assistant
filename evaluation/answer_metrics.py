def generate_answer_metrics(faithfulness:int,relevance:int,correctness:int):

    """Generates evaluation metrics related to answer generation

        Args:
            faithfulness = how much the answer is related to context retrieved
            relevance = how correct the answer is related to query
            correctness = how close the answer is to the ground truth

    """

    return {
        "faithfulness" : faithfulness,
        "relevance" : relevance,
        "correctness" : correctness
    }



