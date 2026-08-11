import json

from services.knowledgeService import KnowledgeService


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

    for i, case in enumerate(test_cases, start=1):

        question = case["question"]

        result = knowledge_service.ask(
            question,
            include_retrieval=True,generate_answer=False
        )

        print("=" * 70)
        print(f"Test Case {i}")
        print(f"Question: {question}")

        print("\nAnswer:")
        print(result["answer"])

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

        print()


if __name__ == "__main__":
    main()