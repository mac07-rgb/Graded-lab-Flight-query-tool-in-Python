# AI Usage Disclosure

# AI Usage Disclosure

## Tools used

- ChatGPT (OpenAI), GPT-6.

## Conversation links

- Link 1: https://chatgpt.com/c/6af487cf-3ba8-83eb-b9d1-a873ef5927b2

## What I used them for

- Understanding the assignment requirements and breaking the project into smaller tasks.
- Learning how to implement CSV validation, file processing and duplicate detection.
- Understanding argparse, JSON handling, Python logging and command-line arguments.
- Debugging errors and testing different cases.
- Reviewing the query functionality, sorting and filtering.

## Which parts of the code were AI-generated or substantially AI-assisted

| File | Function or part | How |
|---|---|---|
| validator.py | load_airports(), validate_row(), to_record() | AI-assisted implementation and debugging |
| csv_loader.py | parse_files() | AI-assisted implementation |
| query.py | run_query(), run_queries() | AI-assisted implementation |
| flight_parser.py | main() | AI-assisted implementation |
| AI_USAGE.md | Disclosure | AI-assisted drafting |

## Key prompts

1. Help me implement flight CSV validation according to the assignment requirements, including all validation checks and their order.
2. Implement CSV parsing with physical line numbers, error reporting and duplicate detection across multiple files.
3. Help me implement flight queries, sorting, filtering and the command-line interface with argparse, JSON and logging.

## What I changed or verified myself

I integrated the implementations into the teacher-provided starter project and ran the supplied public test suite. All 29 public tests passed. I also tested additional cases involving non-ASCII flight IDs, invalid query values, command-line exit codes and database generation.

I reviewed the implementation and am responsible for understanding and verifying the submitted code.
