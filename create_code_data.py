import ast
import os
import json
import tiktoken
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class CodeVisitor(ast.NodeVisitor):
    def __init__(self, source_lines, file_path):
        self.source_lines = source_lines
        self.file_path = file_path
        self.code_data = []

    # Visit function definitions
    def visit_FunctionDef(self, node):
        start_line = node.lineno - 1
        end_line = (
            node.body[-1].end_lineno
            if hasattr(node.body[-1], "end_lineno")
            else start_line
        )
        code_lines = self.source_lines[start_line : end_line + 1]
        code = "".join(code_lines).strip()

        decorators = [d.id for d in node.decorator_list if isinstance(d, ast.Name)]
        args = [arg.arg for arg in node.args.args]
        code_info = {
            "type": "function",
            "name": node.name,
            "decorators": decorators,
            "args": args,
            "code": code,
            "file_path": self.file_path,
            "start_line": start_line + 1,
            "end_line": end_line + 1,
            "start_col": node.col_offset,
            "end_col": node.end_col_offset if hasattr(node, "end_col_offset") else None,
        }
        self.code_data.append(code_info)
        for child_node in ast.iter_child_nodes(node):
            self.visit(child_node)

    # Visit class definitions
    def visit_ClassDef(self, node):
        start_line = node.lineno - 1
        end_line = (
            node.body[-1].end_lineno
            if hasattr(node.body[-1], "end_lineno")
            else start_line
        )
        code_lines = self.source_lines[start_line : end_line + 1]
        code = "".join(code_lines).strip()

        decorators = [d.id for d in node.decorator_list if isinstance(d, ast.Name)]
        bases = [base.id for base in node.bases if isinstance(base, ast.Name)]
        code_info = {
            "type": "class",
            "name": node.name,
            "decorators": decorators,
            "bases": bases,
            "code": code,
            "file_path": self.file_path,
            "start_line": start_line + 1,
            "end_line": end_line + 1,
            "start_col": node.col_offset,
            "end_col": node.end_col_offset if hasattr(node, "end_col_offset") else None,
        }
        self.code_data.append(code_info)
        for child_node in ast.iter_child_nodes(node):
            self.visit(child_node)

    # Visit variable assignments
    def visit_Assign(self, node):
        for target in node.targets:
            if isinstance(target, ast.Name):
                start_line = node.lineno - 1
                end_line = (
                    node.end_lineno if hasattr(node, "end_lineno") else start_line
                )
                code_lines = self.source_lines[start_line : end_line + 1]
                code = "".join(code_lines).strip()
                code_info = {
                    "type": "variable",
                    "name": target.id,
                    "code": code,
                    "file_path": self.file_path,
                    "start_line": start_line + 1,
                    "end_line": end_line + 1,
                    "start_col": target.col_offset,
                    "end_col": target.end_col_offset
                    if hasattr(target, "end_col_offset")
                    else None,
                }
                self.code_data.append(code_info)
        for child_node in ast.iter_child_nodes(node):
            self.visit(child_node)

    # Visit other nodes
    def generic_visit(self, node):
        for child_node in ast.iter_child_nodes(node):
            self.visit(child_node)


# Print the AST of a given file
def print_ast(filename):
    with open(filename, "r") as source:
        source_lines = source.readlines()
        source.seek(0)
        tree = ast.parse(source.read())
        visitor = CodeVisitor(source_lines, filename)
        visitor.visit(tree)
        return visitor.code_data


# Get all Python files in a given directory
def get_python_files(directory):
    python_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                python_files.append(os.path.join(root, file))
    return python_files


# Function to estimate the number of tokens for a given code snippet
def estimate_tokens(code_snippet):
    # Get the tokenizer for GPT-4
    tokenizer = tiktoken.encoding_for_model("gpt-4")
    tokens = tokenizer.encode(
        code_snippet,
        allowed_special={"<|endoftext|>"},
    )
    return len(tokens)


# Main function to process the files and generate code data
def main():
    directory = os.environ.get("CODESEER_CODE_PATH", None)
    if directory is None:
        directory = input("Please enter the directory path: ")

    if not os.path.isdir(directory):
        print("Invalid directory path. Please try again.")
        return

    python_files = get_python_files(directory)
    all_code_data = []
    for file in python_files:
        print(f"\nProcessing file: {file}")
        code_data = print_ast(file)
        all_code_data.extend(code_data)

    # Iterate through the code data and estimate tokens for each code snippet
    for item in all_code_data:
        code_snippet = item["code"]
        num_tokens = estimate_tokens(code_snippet)
        item["num_tokens"] = num_tokens

        # Log the results
        print(
            f"Type: {item['type']}, Name: {item['name']}, File: {item['file_path']}, "
            f"Lines: {item['start_line']} - {item['end_line']}, Tokens: {num_tokens}"
        )

    with open("code_data.json", "w") as output_file:
        json.dump(all_code_data, output_file, indent=2)


# Function to be called from another Python file
def run(directory=None):
    if directory is None:
        main()
    else:
        os.environ["CODESEER_CODE_PATH"] = directory
        main()


if __name__ == "__main__":
    main()
