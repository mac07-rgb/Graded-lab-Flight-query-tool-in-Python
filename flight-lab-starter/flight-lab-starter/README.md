# Flight Schedule Parser and Query Tool: starter files

This folder is the starting point for the graded lab. The full rules are in
the assignment description on Moodle; this file only explains what is here.

## What is in this folder

| Path | What it is |
| --- | --- |
| `flight_parser.py` | Entry point with `main()` and your student constants. **Edit.** |
| `validator.py` | `load_airports`, `validate_row`, `to_record`. **Edit.** |
| `csv_loader.py` | `parse_files`. **Edit.** |
| `query.py` | `run_query`, `run_queries`. **Edit.** |
| `AI_USAGE.md` | Your AI use disclosure. **Fill in before submitting.** |
| `data/db.csv` | The sample file from the worked example (7 valid rows, 12 invalid). |
| `data/airports.txt` | The airport list to pass with `-a`. |
| `data/query.json` | The sample queries from the worked example. |
| `data/flights/` | A folder for testing `-d`. One of its files uses Windows line endings, one has only a header, and the `.txt` file and the `archive/` sub-folder must be ignored. |
| `tests/run_public_tests.py` | The public test script. Do not edit. |
| `tests/expected/` | Expected outputs used by the tests. Do not edit. |
| `.devcontainer/` | Codespaces setup (Python 3.13). Do not edit. |

The function names and signatures in the four `.py` files are fixed, because
the autograder calls them directly. Replace the `raise NotImplementedError`
lines with your code. You may add more functions, classes and modules.

## Getting started

1. Create your own **private** repository from the starter template and
   open it in GitHub Codespaces. The `.devcontainer` folder sets the
   codespace up with Python 3.13; check with `python --version`.
2. Add your instructor as a collaborator (Settings > Collaborators) so the
   grader can read your repository.
3. Set `STUDENT_ID`, `FIRST_NAME` and `LAST_NAME` in `flight_parser.py`.
4. Start with `validator.py`; the tests in group B check it on its own.
5. Run your program from the project folder, for example:

   ```
   python flight_parser.py -i data/db.csv -a data/airports.txt
   python flight_parser.py -d data/flights -a data/airports.txt -o out/db.json
   python flight_parser.py -j db.json -q data/query.json
   ```

   The `out/` folder must exist before you use it with `-o`.

## Running the public tests

From this folder:

```
python tests/run_public_tests.py
```

The output lists every test and ends with a summary per grading group (A–H).
A failing test prints what it expected and what it got. Passing every public
test does not guarantee full points: the final grade uses a larger hidden test
set with different data.

## Submitting

Commit and push your work, then submit your repository URL on Moodle before
the deadline. The four `.py` files and `AI_USAGE.md` must be in the
repository root. Late submissions are not accepted, and only commits pushed
before the deadline are graded.

The `.gitignore` keeps generated files (`db.json`, `errors.log`,
`response_*.json`) out of your repository.
