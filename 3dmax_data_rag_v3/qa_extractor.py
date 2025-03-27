from langchain_community.document_loaders import PyPDFLoader
from langchain.docstore.document import Document
import re
import random


def process_max_document(file_path, file_type="pdf", num_samples=5, test_question=None):
    """
    Process a 3D Max document to extract Q&A pairs

    Args:
        file_path: Path to the document
        file_type: Type of document (pdf or docx)
        num_samples: Number of sample chunks to display
        test_question: Specific question to search for
    """
    # Load the document as a single text
    if file_type.lower() == "pdf":
        loader = PyPDFLoader(file_path, mode="single",
                             pages_delimiter="\n--PAGE--\n")
        documents = loader.load()
    elif file_type.lower() == "docx":
        from langchain_community.document_loaders import Docx2txtLoader
        loader = Docx2txtLoader(file_path)
        documents = loader.load()
    else:
        raise ValueError(f"Unsupported file type: {file_type}")

    print(f"Loaded document: {file_path}")

    # We should have a single document with all the text
    if len(documents) == 1:
        full_text = documents[0].page_content
    else:
        # If we have multiple documents, combine them
        full_text = "\n".join([doc.page_content for doc in documents])

    print(f"Document length: {len(full_text)} characters")

    # Extract Q&A pairs
    qa_chunks = extract_qa_pairs(full_text)
    print(f"Extracted {len(qa_chunks)} Q&A pairs")

    # Display sample chunks
    display_samples(qa_chunks, num_samples)

    # Test specific question if provided
    if test_question:
        eval_specific_question(qa_chunks, test_question)

    return qa_chunks


def extract_qa_pairs(text):
    """Extract Q&A pairs from text"""
    qa_chunks = []

    # Pattern for questions like "37. Как выбрать систему координат?"
    # Includes all common Russian question words
    qa_pattern = r'(\d+)\.\s+((?:Как|Что|Почему|Где|Когда|Каким образом|В чем|Зачем|Сколько|Какие|Какой|Какая|Какое)[^?]+\?)'

    # Find all matching questions
    matches = list(re.finditer(qa_pattern, text))

    if not matches:
        print("Warning: No Q&A pairs found with the standard pattern")
        # Try a simpler pattern as fallback
        qa_pattern = r'(\d+)\.\s+([^\.]+\?)'
        matches = list(re.finditer(qa_pattern, text))
        if matches:
            print(f"Found {len(matches)} Q&A pairs with simplified pattern")

    # Process each matched question
    for i, match in enumerate(matches):
        q_num = match.group(1)
        question = match.group(2).strip()
        start_pos = match.start()

        # Find where this answer ends (start of next question or end of text)
        if i < len(matches) - 1:
            end_pos = matches[i + 1].start()
        else:
            end_pos = len(text)

        # Extract the full Q&A text
        qa_text = text[start_pos:end_pos].strip()

        # Create metadata
        metadata = {
            "type": "qa",
            "question_number": q_num,
            "question": question
        }

        # Add to results
        qa_chunks.append(Document(page_content=qa_text, metadata=metadata))

    return qa_chunks


def display_samples(chunks, num_samples):
    """Display sample chunks"""
    if not chunks:
        print("No chunks to display")
        return

    # Sample chunks
    if len(chunks) <= num_samples:
        samples = chunks
    else:
        samples = random.sample(chunks, num_samples)

    print(f"\n{'=' * 60}")
    print(f"SHOWING {len(samples)} SAMPLE Q&A PAIRS:")
    print(f"{'=' * 60}")

    for i, chunk in enumerate(samples):
        print(f"\nSAMPLE {i + 1}:")
        print(f"Question #{chunk.metadata['question_number']}: {chunk.metadata['question']}")

        # Extract just the answer part
        full_text = chunk.page_content
        question_text = chunk.metadata['question']

        # Find the answer part (everything after the question)
        q_index = full_text.find(question_text)
        if q_index != -1:
            answer_start = q_index + len(question_text)
            answer_text = full_text[answer_start:].strip()
            # Remove the question number prefix if present
            answer_text = re.sub(r'^\s*\d+\.\s*', '', answer_text)
            # Look for "Ответ:" marker and extract from there if found
            answer_marker = re.search(r'Ответ:', answer_text)
            if answer_marker:
                answer_text = answer_text[answer_marker.end():].strip()
        else:
            answer_text = "Unable to extract answer"

        # Display a preview of the answer
        answer_preview = answer_text[:200] + "..." if len(answer_text) > 200 else answer_text
        print(f"Answer: {answer_preview}")
        print(f"{'=' * 60}")


def eval_specific_question(chunks, question_text):
    """Test retrieval for a specific question"""
    print(f"\nSEARCHING FOR: '{question_text}'")

    # First, try exact matching
    exact_matches = []
    for chunk in chunks:
        if question_text.lower() in chunk.metadata['question'].lower():
            exact_matches.append(chunk)

    if exact_matches:
        print(f"Found {len(exact_matches)} matches containing this question")
        for i, chunk in enumerate(exact_matches):
            print(f"\nMATCH {i + 1}:")
            print(f"Complete question: {chunk.metadata['question']}")

            # Extract the answer
            full_text = chunk.page_content
            question_text = chunk.metadata['question']

            # Find where the answer starts
            q_index = full_text.find(question_text)
            if q_index != -1:
                answer_start = q_index + len(question_text)
                answer_text = full_text[answer_start:].strip()

                # Check if the answer has a marker like "Ответ:"
                answer_marker = re.search(r'Ответ:', answer_text)
                if answer_marker:
                    answer_text = answer_text[answer_marker.end():].strip()
            else:
                answer_text = "Unable to extract answer"

            print(f"Answer: {answer_text}")
    else:
        # Try word matching
        print("No exact matches found. Trying partial matching...")

        query_words = set(question_text.lower().split())
        best_matches = []

        for chunk in chunks:
            chunk_words = set(chunk.metadata['question'].lower().split())
            common_words = query_words.intersection(chunk_words)

            if len(common_words) >= 2:  # At least two words in common
                best_matches.append((chunk, len(common_words)))

        # Sort by number of matching words, descending
        best_matches.sort(key=lambda x: x[1], reverse=True)

        if best_matches:
            print(f"Found {len(best_matches)} partial matches")
            # Show top 3 matches
            for i, (chunk, match_count) in enumerate(best_matches[:3]):
                print(f"\nPARTIAL MATCH {i + 1} ({match_count} matching words):")
                print(f"Question: {chunk.metadata['question']}")

                # Extract answer as above
                full_text = chunk.page_content
                q_text = chunk.metadata['question']
                q_index = full_text.find(q_text)

                if q_index != -1:
                    answer_start = q_index + len(q_text)
                    answer_text = full_text[answer_start:].strip()
                    answer_marker = re.search(r'Ответ:', answer_text)
                    if answer_marker:
                        answer_text = answer_text[answer_marker.end():].strip()
                else:
                    answer_text = "Unable to extract answer"

                print(f"Answer preview: {answer_text[:150]}...")
        else:
            print("No partial matches found with at least 2 matching words")


# Example usage
if __name__ == "__main__":
    # Process PDF document
    qa_chunks = process_max_document(
        "./data/3dmax_data.pdf",
        file_type="pdf",
        num_samples=5,
        test_question="Как выбрать систему координат?"
    )

    # Uncomment to try DOCX if PDF doesn't work
    # qa_chunks = process_max_document(
    #     "./data/3dmax_data.docx",
    #     file_type="docx",
    #     num_samples=5,
    #     test_question="Как выбрать систему координат?"
    # )