# Basic-LLM-Tutor

## A Python tool powered by Ollama which can read a PDF document and answer questions based on its content.

This tool uses a customised Llama 3 (8B parameters) model to answer questions solely on the content of any given PDF file. The custom model has adjusted parameters and a unique system prompt in order to make it adhere to the provided context and avoid hallucinations.

## Screenshots

![Prompt Within Context](Screenshots/prompt-within-context.png)

This screenshot shows an example of a prompt within the context provided by the PDF document. Here, the context is a PDF on the Model-View-Controller software design pattern.

![Prompt Outside Context](Screenshots/prompt-outside-context.png)

This screenshot shows an example of a prompt outside of the context provided by the PDF document. This is using the same context as the screenshot above.

## Setup

Download [Ollama](https://ollama.com/).

Run "ollama pull llama3:8b" to download the Llama 3 8B parameter modle.

Run "ollama create tutor -f Tutor_Model.txt" in the repository directory to create the custom model.

Add PDF documents into the repository directory.

Run the python script.