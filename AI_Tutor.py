import ollama
import os
import numpy as np
from numpy.linalg import norm
import PyPDF2



'''
 Retrieves the filename and verifies the existance of a PDF.
 @return The file name
'''
def getPDFLocation():
    while True:
        # Get the file name from the user
        fileName = input("Enter PDF file name: ").strip()

        # Check that the file ends with the .pdf extension
        if not fileName.lower().endswith(".pdf"):
            print("Error: The file must have the .pdf extension")
            continue

        # Check that the file exists
        if not os.path.exists(fileName):
            print("Error: The file was not found")
            continue

        # Return the file name
        return fileName



'''
 Reads the PDF from the given fileName and splits it into paragrpahs.
 @param filename The name of the PDF file to read from
 @return The paragraphs from the PDF file
'''
def getParagraphsFromPDF(fileName):
    # Read the PDF
    with open(fileName, "rb") as pdf:
        reader = PyPDF2.PdfReader(pdf)
        text = ""
        for page in reader.pages:
            pageText = page.extract_text()
            if pageText:
                text += pageText + "\n"

    # Split the text into paragraphs
    paragraphs = []
    buffer = []
    for line in text.splitlines():
        line = line.strip()
        if line:
            buffer.append(line)
        elif buffer:
            paragraphs.append(" ".join(buffer))
            buffer = []
    if buffer:
        paragraphs.append(" ".join(buffer))

    # Return the paragraphs
    return paragraphs



'''
 Gets the embeddings for a list of paragraphs.
 @param paragraphs The paragraphs to get the embeddings for
 @return The embeddings
'''
def getEmbeddings(paragraphs):
    embeddings = [
        ollama.embeddings(model="nomic-embed-text", prompt=paragraph)["embedding"]
        for paragraph in paragraphs
    ]
    return embeddings



'''
 Calculates the cosine similarity between a given embedding and a list of other embeddings.
 @param embedding Embedding to compare
 @param embeddingList List of embeddings to compare against
 @return A list of tuples of similarity scores and indexes
'''
def findMostSimilar(embedding, embeddingList):
    embeddingNorm = norm(embedding)
    similarityScores = [
        np.dot(embedding, item) / (embeddingNorm * norm(item)) for item in embeddingList
    ]
    return sorted(zip(similarityScores, range(len(embeddingList))), reverse=True)



'''
 Sets up and runs the LLM.
'''
def main():
    SYSTEM_PROMPT = """You are a strict tutor. You must only answer questions related to the context provided below. You must only answer with information provided in the context below.
                    If the context does not contain the answer, reply with: "I'm sorry, I can't answer that."
                    Context:
                    """

    # Get the PDF filename from the user
    print("Retrieving PDF file location")
    pdf_filename = getPDFLocation()

    # Parse the pdf to get a list of paragraphs
    print("Parsing PDF")
    paragraphs = getParagraphsFromPDF(pdf_filename)

    # Generate the embeddings for the list of paragraphs
    print("Generating embeddings")
    embeddings = getEmbeddings(paragraphs)

    while True:
        # Get the user's query
        query = input("\n What can I help you with? (type 'quit' to exit chat): ")

        # Exit the loop if the user want's to quit
        if query.lower() == "quit":
            break

        # Generate an embedding for the user's query and find the most relevant paragraphs from the document to create the context for the model
        queryEmbedding = ollama.embeddings(model="nomic-embed-text", prompt=query)["embedding"]
        mostSimilarChunks = findMostSimilar(queryEmbedding, embeddings)[:5]
        relevantContext = "\n\n".join(paragraphs[i] for _, i in mostSimilarChunks)

        # Get the response from the model
        response = ollama.chat(
            model="tutor",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT + "\n\n" + relevantContext},
                {"role": "user", "content": query},
            ],
        )

        # Print the model's response
        print("\n" + response["message"]["content"])


if __name__ == "__main__":
    main()