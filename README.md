# Nanami

A FastAPI application to synchronize transactions from Pluggy.ai to YNAB (You Need A Budget).

## Project Structure

(Details about the project structure will go here)

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd nanami_sync
    ```

2.  **Install Poetry:**
    If you don't have Poetry installed, follow the instructions on the [official Poetry website](https://python-poetry.org/docs/#installation).

3.  **Create and populate `.env` file:**
    Copy `.env.example` to `.env` and fill in your actual credentials and database URL.
    ```bash
    cp .env.example .env
    ```
    Edit `.env` with your details.

4.  **Install dependencies:**
    ```bash
    poetry install
    ```

5.  **Initialize the database (if applicable, after setting up Alembic):
    ```bash
    # poetry run alembic upgrade head
    ```

## Running the Application

To run the development server:

```bash
poetry run uvicorn app.main:app --reload
```

Or, if you have the `if __name__ == "__main__":` block in `app/main.py`:

```bash
poetry run python app/main.py
```

The application will typically be available at `http://127.0.0.1:8000`.

## Running with Docker (Optional - Future Step)

(Instructions for Docker will go here once a Dockerfile is created) 