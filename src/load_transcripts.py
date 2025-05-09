import os
from langchain_community.document_loaders import JSONLoader


def load_transcripts(json_file_path: str) -> list:
    """
    Load transcripts from a JSON file using LangChain's JSONLoader.

    Args:
        json_file_path (str): Path to the JSON file containing transcripts

    Returns:
        list: List of Document objects containing transcripts
    """
    # Define the jq schema to extract transcripts
    jq_schema = """
    .[].transcripts[].sent
    """

    # Load the documents using JSONLoader
    loader = JSONLoader(
        file_path=json_file_path,
        jq_schema=jq_schema,
        content_key="page_content",
    )

    # Load the documents
    documents = loader.load()

    return documents


if __name__ == "__main__":
    # Example usage
    json_file = "../test.json"
    documents = load_transcripts(json_file)

    print(f"Loaded {len(documents)} documents")
    print("\nFirst document example:")
    print(documents[0])
