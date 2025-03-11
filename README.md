# BackedntakehomeAssignment
## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/pubmed-fetcher.git
    cd pubmed-fetcher
    ```

2. **Install Poetry** (if not already installed):
    ```bash
    curl -sSL https://install.python-poetry.org | python3 -
    ```

3. **Install dependencies**:
    ```bash
    poetry install
    ```
## Usage

### Command-Line Interface

To fetch papers based on a query and print the results to the console:
```bash
get-papers-list "your-query"

### Command-Line Arguments
```markdown
## Command-Line Arguments

The program accepts the following command-line arguments:

- `query` (required): The search query to fetch papers.
- `-f`, `--file` (optional): The filename to save the results. If not provided, the output will be printed to the console.
- `-h`, `--help`: Display usage instructions.

