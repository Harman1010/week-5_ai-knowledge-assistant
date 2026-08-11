from pathlib import Path

import json

from services.knowledgeService import KnowledgeService
from evaluation.retrieval_metrics import calculate_retrieval_metrics


PDF_PATH = "What is Pollution - Final.pdf"
TEST_CASES_PATH = "evaluation/test_cases.json"


def load_test_cases():

    with open(
        TEST_CASES_PATH,
        "r",
        encoding="utf-8"
    ) as file:
        return json.load(file)


def main():

    test_cases = load_test_cases()

    knowledge_service = KnowledgeService()

    print("Ingesting document...")

    knowledge_service.ingest(PDF_PATH)

    print("Running evaluation...\n")

    total_hits = 0
    total_mrr = 0
    total_precision = 0

    expected_results = []

    total_cases = len(test_cases)

    for i, case in enumerate(test_cases, start=1):

        question = case["question"]

        result = knowledge_service.ask(
            question,
            include_retrieval=True,
            generate_answer=False
        )

        metrics = calculate_retrieval_metrics(
            result["retrieved_documents"],
            case["expected_source"],
            case["expected_pages"],
            top_k=3
        )

        total_hits += metrics["hit"]
        total_mrr += metrics["reciprocal_rank"]
        total_precision += metrics["precision"]

        expected_results.append({
            "test_case" : i,
            "question" : question,
            "hit_at_3" : metrics["hit"],
            "mrr" : metrics["reciprocal_rank"],
            "precision_at_3" : metrics["precision"]
        })

        total_cases = len(test_cases)

        print("=" * 70)

        print(f"Test Case {i}")
        print(f"Question: {question}")

        print("\nRetrieved Documents:")

        for rank, (document, score) in enumerate(
            result["retrieved_documents"],
            start=1
        ):

            print(
                f"{rank}. "
                f"Source={document.metadata.get('source')} "
                f"Page={document.metadata.get('page')} "
                f"Score={score:.4f}"
            )

        print("\nRetrieval Metrics:")

        print(
            f"Hit@3: "
            f"{metrics['hit']}"
        )

        print(
            f"MRR: "
            f"{metrics['reciprocal_rank']:.3f}"
        )

        print(
            f"Precision@3: "
            f"{metrics['precision']:.3f}"
        )

        print()

    average_metrics = {
                "hit_at_3": total_hits / total_cases,
                "mrr": total_mrr / total_cases,
                "precision_at_3": total_precision / total_cases
            }
    
    print("=" * 70)
    print("FINAL RETRIEVAL EVALUATION")
    print("=" * 70)

    print(
        f"Hit@3: "
        f"{total_hits / total_cases:.3f}"
    )

    print(
        f"MRR: "
        f"{total_mrr / total_cases:.3f}"
    )

    print(
        f"Precision@3: "
        f"{total_precision / total_cases:.3f}"
    )

    output = {
        "average" : average_metrics,
        "test_cases" : expected_results
    }

    result_dir = Path("evaluation/results")
    result_dir.mkdir(exist_ok=True)

    output_path = result_dir / "retrieval_results.json"

    with open(output_path,"w",encoding="utf-8") as file:

        json.dump(output,file,indent=2)

    print(f"Output saved to {output_path}")

if __name__ == "__main__":
    main()