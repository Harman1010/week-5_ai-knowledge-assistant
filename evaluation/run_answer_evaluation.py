import asyncio
import json
from pathlib import Path

from services.knowledgeService import KnowledgeService

from evaluation.answer_evaluator import evaluate_answer

from evaluation.evaluator_config import (
    get_evaluator_llm,
    get_evaluator_embeddings
)


PDF_PATH = "What is Pollution - Final.pdf"
TEST_CASES_PATH = "evaluation/test_cases.json"


def load_test_cases():

    with open(
        TEST_CASES_PATH,
        "r",
        encoding="utf-8"
    ) as file:
        return json.load(file)


async def main():

    test_cases = load_test_cases()

    knowledge_service = KnowledgeService()

    print("Ingesting document...")

    knowledge_service.ingest(PDF_PATH)

    print("Creating evaluation models...")

    evaluator_llm = get_evaluator_llm()
    evaluator_embeddings = get_evaluator_embeddings()

    print("Running answer evaluation...\n")

    total_faithfulness = 0
    total_relevance = 0
    total_correctness = 0

    evaluation_results = []

    total_cases = len(test_cases)

    for i, case in enumerate(test_cases, start=1):

        question = case["question"]
        expected_answer = case["expected_answer"]

        result = knowledge_service.ask(
            question,
            include_retrieval=True,
            generate_answer=True
        )

        metrics = await evaluate_answer(
            question=question,
            answer=result["answer"],
            retrieved_documents=result["retrieved_documents"],
            expected_answer=expected_answer,
            evaluator_llm=evaluator_llm,
            evaluator_embeddings=evaluator_embeddings
        )

        total_faithfulness += metrics["faithfulness"]
        total_relevance += metrics["relevance"]
        total_correctness += metrics["correctness"]

        evaluation_results.append({
            "test_case": i,
            "question": question,
            "faithfulness": metrics["faithfulness"],
            "relevance": metrics["relevance"],
            "correctness": metrics["correctness"]
        })

        print("=" * 70)

        print(f"Test Case {i}")
        print(f"Question: {question}")

        print("\nGenerated Answer:")
        print(result["answer"])

        print("\nAnswer Metrics:")

        print(
            f"Faithfulness: "
            f"{metrics['faithfulness']:.3f}"
        )

        print(
            f"Relevance: "
            f"{metrics['relevance']:.3f}"
        )

        print(
            f"Correctness: "
            f"{metrics['correctness']:.3f}"
        )

        print()

    # Calculate overall averages
    average_metrics = {
        "faithfulness": total_faithfulness / total_cases,
        "relevance": total_relevance / total_cases,
        "correctness": total_correctness / total_cases
    }

    print("=" * 70)
    print("FINAL ANSWER EVALUATION")
    print("=" * 70)

    print(
        f"Faithfulness: "
        f"{average_metrics['faithfulness']:.3f}"
    )

    print(
        f"Relevance: "
        f"{average_metrics['relevance']:.3f}"
    )

    print(
        f"Correctness: "
        f"{average_metrics['correctness']:.3f}"
    )

    # Prepare output
    output = {
        "average": average_metrics,
        "test_cases": evaluation_results
    }

    # Create results directory
    results_dir = Path("evaluation/results")
    results_dir.mkdir(exist_ok=True)

    output_path = (
        results_dir / "answer_results.json"
    )

    # Save results
    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            output,
            file,
            indent=2
        )

    print(
        f"\nOutput saved to {output_path}"
    )


if __name__ == "__main__":
    asyncio.run(main())