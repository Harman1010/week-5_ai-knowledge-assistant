import json

from services.knowledgeService import KnowledgeService
from evaluation.answer_evaluator import evaluate_answer


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

    print("Running answer evaluation...\n")

    for i, case in enumerate(test_cases, start=1):

        question = case["question"]
        expected_answer = case["expected_answer"]

        result = knowledge_service.ask(
            question,
            include_retrieval=True,
            generate_answer=True
        )

        print("=" * 70)

        print(f"Test Case {i}")
        print(f"Question: {question}")

        print("\nGenerated Answer:")
        print(result["answer"])

        print("\nEvaluating answer...")

        # RAGAS evaluation will be called here