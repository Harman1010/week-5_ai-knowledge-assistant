from ragas.metrics.collections import Faithfulness,AnswerRelevancy,AnswerCorrectness

async def evaluate_answer(
    question: str,
    answer: str,
    retrieved_documents,
    expected_answer: str,
    evaluator_llm,
    evaluator_embeddings
):

    contexts = [
        document.page_content
        for document, _ in retrieved_documents
    ]

    faithfulness_metric = Faithfulness(
        llm=evaluator_llm
    )

    relevance_metric = AnswerRelevancy(
        llm=evaluator_llm,
        embeddings=evaluator_embeddings
    )

    correctness_metric = AnswerCorrectness(
        llm=evaluator_llm,
        embeddings=evaluator_embeddings
    )

    faithfulness = await faithfulness_metric.ascore(
        user_input=question,
        response=answer,
        retrieved_contexts=contexts
    )

    relevance = await relevance_metric.ascore(
        user_input=question,
        response=answer
    )

    correctness = await correctness_metric.ascore(
        user_input=question,
        response=answer,
        reference=expected_answer
    )

    return {
        "faithfulness": faithfulness.value,
        "relevance": relevance.value,
        "correctness": correctness.value
    }