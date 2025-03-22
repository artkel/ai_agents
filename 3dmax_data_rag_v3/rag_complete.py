"""
3D Max RAG System - A complete question answering system for 3D Max documentation
with chapter-aware document processing
"""
import os
import shutil
from dotenv import load_dotenv
from pathlib import Path

# LangChain imports
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader
from langchain.chat_models import init_chat_model
from langchain_cohere import CohereEmbeddings
from langchain_chroma import Chroma
from langchain.schema.runnable import RunnablePassthrough
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.docstore.document import Document

# Import our custom splitter
from custom_splitter import ChapterAwareMaxSplitter

# Load environment variables
load_dotenv()

# Get API keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
COHERE_API_KEY = os.getenv("COHERE_API_KEY")


class ThreeDMaxRAG:
    """
    A RAG-based question answering system for 3D Max documentation
    with chapter-aware document processing
    """

    def __init__(self, doc_path, doc_type="pdf", db_path="./chroma_db_aware_v1", rebuild_db=False):
        """
        Initialize the 3D Max RAG system

        Args:
            doc_path: Path to the 3D Max documentation
            doc_type: Type of document (pdf or docx)
            db_path: Path to store/load the Chroma vector database
            rebuild_db: Whether to rebuild the vector database even if it exists
        """
        self.doc_path = doc_path
        self.doc_type = doc_type.lower()
        self.db_path = db_path
        self.rebuild_db = rebuild_db

        # Initialize language model
        self.llm = init_chat_model("gpt-4o-mini", model_provider="openai")

        # Initialize embeddings
        self.embeddings = CohereEmbeddings(
            model="embed-multilingual-v3.0",
            cohere_api_key=COHERE_API_KEY
        )

        # Setup the vector database and retriever
        self._setup_vectorstore()

        # Create the RAG chain
        self._setup_rag_chain()

    def _load_document(self):
        """Load the document based on its type"""
        print(f"Loading document: {self.doc_path}")

        if self.doc_type == "pdf":
            loader = PyPDFLoader(self.doc_path, mode="single")
            documents = loader.load()
        elif self.doc_type == "docx":
            loader = Docx2txtLoader(self.doc_path)
            documents = loader.load()
        else:
            raise ValueError(f"Unsupported document type: {self.doc_type}")

        # Combine all pages into a single document if needed
        if len(documents) > 1:
            full_text = "\n".join([doc.page_content for doc in documents])
            documents = [Document(page_content=full_text, metadata={"source": self.doc_path})]
            print(f"Combined {len(documents)} pages into a single document")

        return documents

    def _setup_vectorstore(self):
        """Set up the vector database, loading or creating it as needed"""
        db_exists = Path(self.db_path).exists() and any(Path(self.db_path).iterdir())

        if db_exists and not self.rebuild_db:
            print(f"Loading existing vector database from {self.db_path}")
            self.vectorstore = Chroma(
                persist_directory=self.db_path,
                embedding_function=self.embeddings
            )
        else:
            print(f"Creating new vector database at {self.db_path}")

            # If rebuilding and db exists, delete it first
            if db_exists and self.rebuild_db:
                print(f"Removing existing database at {self.db_path}")
                shutil.rmtree(self.db_path)

            # Load and process the document
            documents = self._load_document()

            # Use our custom chapter-aware splitter
            splitter = ChapterAwareMaxSplitter()
            chunks = splitter.split_documents(documents)
            print(f"Created {len(chunks)} chunks with chapter-aware splitting")

            # Create the vector store
            self.vectorstore = Chroma.from_documents(
                documents=chunks,
                embedding=self.embeddings,
                persist_directory=self.db_path
            )
            print(f"Vector database created and stored at {self.db_path}")

        # Create a retriever
        self.retriever = self.vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 3}  # Retrieve top 3 most relevant chunks
        )

    def _setup_rag_chain(self):
        """Set up the RAG chain for question answering"""
        # Create prompt template
        template = """
        Ты эксперт по программе 3D Max и отвечаешь на вопросы пользователей.
        
        Используй следующие фрагменты документации 3D Max для ответа на вопрос пользователя.
        Если не знаешь ответа, просто скажи, что не знаешь. 
        Не пытайся придумать ответ, если информации нет в документации.
        Всегда указывай главу и номер вопроса/раздела из документации, если они доступны.
        
        ДОКУМЕНТАЦИЯ:
        {context}
        
        ВОПРОС ПОЛЬЗОВАТЕЛЯ:
        {question}
        
        ТВОЙ ОТВЕТ (на русском языке):
        """

        self.prompt = ChatPromptTemplate.from_template(template)

        # Define the RAG chain
        self.rag_chain = (
            {"context": self.retriever | self._format_docs, "question": RunnablePassthrough()}
            | self.prompt
            | self.llm
            | StrOutputParser()
        )

    def _format_docs(self, docs):
        """Format retrieved documents for the prompt"""
        formatted_docs = []

        for i, doc in enumerate(docs):
            # Get metadata
            chapter = doc.metadata.get("chapter", "Неизвестная глава")
            doc_type = doc.metadata.get("type", "general")

            if doc_type == "qa":
                question_num = doc.metadata.get("question_number", "?")
                question = doc.metadata.get("question", "")

                # Format as Q&A pair
                formatted_doc = f"[Глава: {chapter}] [Вопрос №{question_num}]:\n{question}\n"

                # Extract answer (everything after the question)
                content = doc.page_content
                question_index = content.find(question)

                if question_index != -1:
                    answer_text = content[question_index + len(question):].strip()
                    # Look for "Ответ:" marker
                    if "Ответ:" in answer_text:
                        answer_text = answer_text.split("Ответ:", 1)[1].strip()
                    formatted_doc += f"Ответ: {answer_text}"
                else:
                    formatted_doc += f"Содержимое: {content}"

            elif doc_type == "ui_explanation":
                section_title = doc.metadata.get("section_title", "")
                section_num = doc.metadata.get("section_number", "")

                # Format as UI explanation
                formatted_doc = f"[Глава: {chapter}] [Раздел: {section_title}]:\n{doc.page_content}"

            else:
                # Format general content
                formatted_doc = f"[Глава: {chapter}]:\n{doc.page_content}"

            formatted_docs.append(formatted_doc)

        return "\n\n" + "\n\n".join(formatted_docs)

    def ask(self, question):
        """
        Ask a question about 3D Max

        Args:
            question: The question to ask

        Returns:
            str: The answer to the question
        """
        return self.rag_chain.invoke(question)

    def test_retrieval(self, query, k=3):
        """
        Test the retrieval system with a specific query

        Args:
            query: The query to test
            k: Number of results to retrieve

        Returns:
            List of retrieved documents
        """
        print(f"\nТестовый запрос: '{query}'")
        results = self.vectorstore.similarity_search(query, k=k)

        print(f"Найдено {len(results)} релевантных фрагментов.")

        for i, doc in enumerate(results):
            print(f"\nРезультат {i+1}:")
            print(f"Глава: {doc.metadata.get('chapter', 'Неизвестная глава')}")

            doc_type = doc.metadata.get("type", "general")

            if doc_type == "qa":
                question = doc.metadata.get("question", "")
                question_num = doc.metadata.get("question_number", "?")
                print(f"Вопрос №{question_num}: {question}")

                # Extract answer
                content = doc.page_content
                question_index = content.find(question)

                if question_index != -1:
                    answer_text = content[question_index + len(question):].strip()
                    # Look for "Ответ:" marker
                    if "Ответ:" in answer_text:
                        answer_text = answer_text.split("Ответ:", 1)[1].strip()
                    print(f"Ответ: {answer_text[:200]}...")
                else:
                    print(f"Содержимое: {content[:200]}...")

            elif doc_type == "ui_explanation":
                section_title = doc.metadata.get("section_title", "")
                print(f"Раздел: {section_title}")
                print(f"Содержимое: {doc.page_content[:200]}...")

            else:
                print(f"Тип: Общее содержимое")
                print(f"Содержимое: {doc.page_content[:200]}...")

        return results

    def run_interactive(self):
        """Run an interactive session with the 3D Max Assistant"""
        print("\n" + "="*50)
        print("Добро пожаловать в ассистент по 3D Max!")
        print("Задайте вопрос о 3D Max или введите 'выход' для завершения.")
        print("="*50 + "\n")

        while True:
            user_question = input("\nВаш вопрос: ")

            if user_question.lower() in ['выход', 'exit', 'quit', 'bye']:
                print("\nСпасибо за использование ассистента по 3D Max. До свидания!")
                break

            if not user_question.strip():
                print("Пожалуйста, введите вопрос или 'выход' для завершения.")
                continue

            try:
                print("\nИщу ответ...")
                answer = self.ask(user_question)
                print(f"\nОтвет: {answer}")

            except Exception as e:
                print(f"\nИзвините, произошла ошибка: {str(e)}")
                print("Пожалуйста, попробуйте еще раз или перефразируйте вопрос.")


def main():
    """Main entry point for the 3D Max RAG system"""
    import argparse

    parser = argparse.ArgumentParser(description="3D Max RAG Question Answering System")
    parser.add_argument("--doc", type=str, default="./data/3dmax_data.pdf",
                        help="Path to the 3D Max documentation")
    parser.add_argument("--type", type=str, default="pdf", choices=["pdf", "docx"],
                        help="Document type (pdf or docx)")
    parser.add_argument("--db", type=str, default="./chroma_db_aware_v1",
                        help="Path to the Chroma vector database")
    parser.add_argument("--rebuild", action="store_true",
                        help="Rebuild the vector database even if it exists")
    parser.add_argument("--query", type=str,
                        help="Single query to test (non-interactive mode)")

    args = parser.parse_args()

    # Create the RAG system
    rag = ThreeDMaxRAG(
        doc_path=args.doc,
        doc_type=args.type,
        db_path=args.db,
        rebuild_db=args.rebuild
    )

    # Either run a test query or interactive session
    if args.query:
        print(f"\nTesting query: {args.query}")
        rag.test_retrieval(args.query)
        print("\nGenerating answer...")
        answer = rag.ask(args.query)
        print(f"\nAnswer: {answer}")
    else:
        rag.run_interactive()


if __name__ == "__main__":
    main()