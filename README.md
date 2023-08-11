# CodeSeer: Python Code Embeddings Indexing and Retrieval

CodeSeer is a powerful tool designed to index, embed, and semantically search through Python code. It's a Code Search system for Python that can be used to feed Language Models like LLMs. The project consists of several components that work together to achieve these goals.

## Features

1. **Environment Configuration:** Set up your Python code path and OpenAI API key.
2. **Parsing Python Code:** Analyze your Python code using Abstract Syntax Trees (AST) and create a JSON file with all methods, classes, and variables.
3. **Creating Embeddings:** Create a local Chroma vector database and fetch embeddings for each code element previously indexed.
4. **Semantic Code Query:** Query your code semantically and retrieve relevant methods, classes, and variables to feed LLM context.

## Components

### Environment Configuration (`.env.example`)

This file contains example environment variables that you need to set up. You'll specify the path to your Python code and your OpenAI API key here.

### Parsing Python Code (`create_code_data.py`)

This script parses all your Python code using AST. It creates a JSON file containing all methods, classes, and variables found in the code. The script includes a class `CodeVisitor` that visits function definitions, class definitions, variable assignments, and other nodes to extract the required information.

### Creating Embeddings (`create_embeddings.py`)

This script creates a local Chroma vector database. It fetches the embedding for each code element previously indexed (methods, classes, variables) and stores them in the database.

### Semantic Code Query (`code_query.py`)

This script allows you to query your code semantically. You can search for relevant methods, classes, and variables, and it will return the results to feed the context of LLMs.

## Usage

1. **Set Up Environment Variables:** Copy `.env.example` to `.env` and fill in the required information.
2. **Create Code Data:** Run `create_code_data.py` to parse all your Python code and create a JSON file with all methods, classes, and variables.
3. **Create Embeddings:** Run `create_embeddings.py` to create a local Chroma vector database with embeddings for each code element.
4. **Query Code:** Use `code_query.py` to query your code semantically and retrieve relevant code elements.

To use that later script, you need to pass your query as an argument when running the file. For instance:

```bash
python code_query.py "How to calculate confidence with this project"
```

## Dependencies

- Python 3.x
- OpenAI API
- Other dependencies can be found in `pyproject.toml` and installed using Poetry.

## License

This project is licensed under the terms of the license found in the `LICENSE` file.
