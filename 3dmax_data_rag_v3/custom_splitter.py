from langchain.text_splitter import TextSplitter
from langchain.docstore.document import Document
from langchain_community.document_loaders import PyPDFLoader
import re
import random


class ChapterAwareMaxSplitter(TextSplitter):
    """
    A document splitter that respects chapter structure in 3D Max documentation.
    Identifies chapters marked with --ChapterName-- format and properly handles
    both Q&A sections and UI explanation sections.
    """

    def __init__(self):
        # Initialize with reasonable values for the parent class
        super().__init__(chunk_size=1000, chunk_overlap=0)

    def split_text(self, text):
        """Required by the interface but not used directly"""
        docs = self.split_documents([Document(page_content=text, metadata={})])
        return [doc.page_content for doc in docs]

    def split_documents(self, documents):
        """Split documents by chapters then by content type within each chapter"""
        result = []

        # Process each input document
        for doc in documents:
            text = doc.page_content
            base_metadata = doc.metadata.copy()

            # Chapter identification with --ChapterName-- format
            chapters = self._identify_chapters(text)

            if not chapters:
                print("Warning: No chapters found with --ChapterName-- pattern")
                # Keep the document as is if no chapters found
                result.append(doc)
                continue

            print(f"Found {len(chapters)} chapters")

            # Process each chapter
            for chapter_name, chapter_content in chapters:
                print(f"\nProcessing chapter: {chapter_name}")

                # Determine content type and process accordingly
                if self._is_qa_chapter(chapter_content):
                    chunks = self._process_qa_content(chapter_name, chapter_content, base_metadata)
                    result.extend(chunks)
                    print(f"  Processed as Q&A chapter with {len(chunks)} Q&A pairs")
                elif self._is_ui_chapter(chapter_content):
                    chunks = self._process_ui_content(chapter_name, chapter_content, base_metadata)
                    result.extend(chunks)
                    print(f"  Processed as UI chapter with {len(chunks)} sections")
                else:
                    # Keep as a single chunk if content type is unknown
                    metadata = base_metadata.copy()
                    metadata["chapter"] = chapter_name
                    metadata["type"] = "general"
                    result.append(Document(page_content=chapter_content, metadata=metadata))
                    print(f"  Processed as general content (single chunk)")

        return result

    def _identify_chapters(self, text):
        """Identify chapters marked with --ChapterName-- format"""
        chapters = []

        # Find all chapter markers
        chapter_pattern = r'--([^-]+)--'
        chapter_matches = list(re.finditer(chapter_pattern, text))

        # Extract chapter content
        for i, match in enumerate(chapter_matches):
            chapter_name = match.group(1).strip()
            start_pos = match.end()

            # Find the end of this chapter (start of next chapter or end of text)
            if i < len(chapter_matches) - 1:
                end_pos = chapter_matches[i + 1].start()
            else:
                end_pos = len(text)

            # Extract chapter content
            chapter_content = text[start_pos:end_pos].strip()
            chapters.append((chapter_name, chapter_content))

        return chapters

    def _is_qa_chapter(self, content):
        """Determine if a chapter contains Q&A pairs"""
        # Look for numbered questions that end with question marks
        qa_pattern = r'\d+\.\s+(?:Как|Что|Почему|Где|Когда|Каким|В чем|Зачем|Сколько)[^?]+\?'
        return bool(re.search(qa_pattern, content))

    def _is_ui_chapter(self, content):
        """Determine if a chapter contains UI explanations with numbered sections"""
        # Look for section numbering like 1.1, 1.2, etc.
        ui_pattern = r'\d+\.\d+\.'
        return bool(re.search(ui_pattern, content))

    def _process_qa_content(self, chapter_name, content, base_metadata):
        """Process a chapter containing Q&A pairs"""
        chunks = []

        # Pattern for numbered questions
        qa_pattern = r'(\d+)\.\s+((?:Как|Что|Почему|Где|Когда|Каким|В чем|Зачем|Сколько)[^?]+\?)'

        # Find all Q&A pairs
        qa_matches = list(re.finditer(qa_pattern, content))

        # Process each Q&A pair
        for i, match in enumerate(qa_matches):
            q_num = match.group(1)
            question = match.group(2).strip()
            start_pos = match.start()

            # Find where this Q&A pair ends
            if i < len(qa_matches) - 1:
                end_pos = qa_matches[i + 1].start()
            else:
                end_pos = len(content)

            # Extract the full Q&A text
            qa_text = content[start_pos:end_pos].strip()

            # Create metadata
            metadata = base_metadata.copy()
            metadata.update({
                "chapter": chapter_name,
                "type": "qa",
                "question_number": q_num,
                "question": question
            })

            # Create document with the complete Q&A pair
            chunks.append(Document(page_content=qa_text, metadata=metadata))

        return chunks

    def _process_ui_content(self, chapter_name, content, base_metadata):
        """Process a chapter containing UI explanations with numbered sections"""
        chunks = []

        # Pattern for numbered sections
        section_pattern = r'(\d+\.\d+\.)\s+([^\n]+)'

        # Find all sections
        section_matches = list(re.finditer(section_pattern, content))

        # Process each section
        for i, match in enumerate(section_matches):
            section_num = match.group(1)
            section_title = match.group(2).strip()
            start_pos = match.start()

            # Find where this section ends
            if i < len(section_matches) - 1:
                end_pos = section_matches[i + 1].start()
            else:
                end_pos = len(content)

            # Extract the full section text
            section_text = content[start_pos:end_pos].strip()

            # Create metadata
            metadata = base_metadata.copy()
            metadata.update({
                "chapter": chapter_name,
                "type": "ui_explanation",
                "section_number": section_num.rstrip('.'),
                "section_title": f"{section_num} {section_title}"
            })

            # Create document with the complete section
            chunks.append(Document(page_content=section_text, metadata=metadata))

        return chunks


def eval_chapter_aware_splitter(pdf_path, num_samples=5):
    """Test the chapter-aware splitter and display sample chunks"""
    print(f"Loading document: {pdf_path}")

    # Load the PDF as a single document to preserve structure
    loader = PyPDFLoader(pdf_path, mode="single")
    documents = loader.load()

    if len(documents) > 1:
        print(f"Warning: PDF loaded as {len(documents)} separate pages. Combining into one document.")
        full_text = "\n".join([doc.page_content for doc in documents])
        documents = [Document(page_content=full_text, metadata={"source": pdf_path})]

    print(f"Document loaded ({len(documents[0].page_content)} characters)")

    # Apply our custom splitter
    splitter = ChapterAwareMaxSplitter()
    chunks = splitter.split_documents(documents)
    print(f"\nCreated {len(chunks)} total chunks")

    # Group chunks by chapter
    chapters = {}
    for chunk in chunks:
        chapter = chunk.metadata.get("chapter", "Unknown")
        if chapter not in chapters:
            chapters[chapter] = []
        chapters[chapter].append(chunk)

    # Print chapter statistics
    print("\nCHAPTER STATISTICS:")
    for chapter, chapter_chunks in chapters.items():
        print(f"  {chapter}: {len(chapter_chunks)} chunks")

    # Display sample chunks
    if len(chunks) <= num_samples:
        samples = chunks
    else:
        samples = random.sample(chunks, num_samples)

    print(f"\n{'=' * 60}")
    print(f"SHOWING {len(samples)} SAMPLE CHUNKS:")
    print(f"{'=' * 60}")

    for i, chunk in enumerate(samples):
        print(f"\nSAMPLE CHUNK {i + 1}:")

        # Show metadata
        print(f"Chapter: {chunk.metadata.get('chapter', 'Unknown')}")
        print(f"Type: {chunk.metadata.get('type', 'Unknown')}")

        if chunk.metadata.get("type") == "qa":
            print(f"Question #{chunk.metadata.get('question_number')}: {chunk.metadata.get('question')}")
        elif chunk.metadata.get("type") == "ui_explanation":
            print(f"Section: {chunk.metadata.get('section_title')}")

        # Show content preview
        content_preview = chunk.page_content[:200] + "..." if len(chunk.page_content) > 200 else chunk.page_content
        print(f"Content preview: {content_preview}")
        print(f"Content length: {len(chunk.page_content)} characters")
        print(f"{'=' * 60}")

    return chunks, chapters


def eval_retrieval(chunks, query, num_results=3):
    """Test retrieval for a specific question"""
    print(f"\nTesting retrieval for: '{query}'")

    # Simple search function - in practice, you'd use a vector database
    matching_chunks = []

    # Try exact matching first
    for chunk in chunks:
        if chunk.metadata.get("type") == "qa" and query.lower() in chunk.metadata.get("question", "").lower():
            matching_chunks.append((chunk, 1.0))  # Perfect match score

    # If no exact matches, try word matching
    if not matching_chunks:
        query_words = set(query.lower().split())

        for chunk in chunks:
            if chunk.metadata.get("type") == "qa":
                question = chunk.metadata.get("question", "")
                chunk_words = set(question.lower().split())
                common_words = query_words.intersection(chunk_words)

                if common_words:
                    # Calculate similarity score
                    similarity = len(common_words) / max(len(query_words), len(chunk_words))
                    matching_chunks.append((chunk, similarity))

    # Sort by similarity score
    matching_chunks.sort(key=lambda x: x[1], reverse=True)

    # Display top results
    if matching_chunks:
        print(f"Found {len(matching_chunks)} potential matches")

        for i, (chunk, score) in enumerate(matching_chunks[:num_results]):
            print(f"\nMATCH {i + 1} (score: {score:.2f}):")
            print(f"Chapter: {chunk.metadata.get('chapter')}")
            print(f"Question #{chunk.metadata.get('question_number')}: {chunk.metadata.get('question')}")

            # Extract answer (everything after the question)
            content = chunk.page_content
            question = chunk.metadata.get("question", "")

            question_index = content.find(question)
            if question_index != -1:
                answer_text = content[question_index + len(question):].strip()

                # Look for "Ответ:" marker
                answer_marker = re.search(r'Ответ:', answer_text)
                if answer_marker:
                    answer_text = answer_text[answer_marker.end():].strip()

                print(f"Answer: {answer_text[:300]}...")
            else:
                print(f"Content: {content[:300]}...")

            print(f"{'=' * 60}")
    else:
        print("No matches found")


# Test the splitter
if __name__ == "__main__":
    chunks, chapters = eval_chapter_aware_splitter("./data/3dmax_data.pdf")

    # Test retrieval
    eval_retrieval(chunks, "Как выбрать систему координат?")