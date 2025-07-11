# Bank Statement Analysis API

This project provides a robust Python-based RESTful API designed for the analysis and management of bank statement transactions. It offers functionalities to import, categorize, and gain insights from financial data through a well-defined set of API endpoints.

## Features

*   **Transaction Management:** Comprehensive CRUD operations for bank transactions.
*   **Categorization:** Tools to categorize transactions for better financial organization.
*   **Source and Type Management:** Define and manage transaction sources and types.
*   **Financial Statistics:** Generate statistical reports grouped by category, date, and source to provide actionable insights into spending patterns.

## Technologies Used

*   **Backend:** Python 3.10, Flask, Flask-RESTX, Flask-SQLAlchemy, Psycopg2
*   **Database:** PostgreSQL
*   **Environment Management:** Pipenv

## Getting Started

Follow these instructions to set up and run the project on your local machine for development and testing.

### Prerequisites

*   [Python 3.10](https://www.python.org/downloads/release/python-3100/)
*   [PostgreSQL](https://www.postgresql.org/download/)
*   [Pipenv](https://pipenv.pypa.io/en/latest/)

### Installation

1.  **Clone the repository:**

2.  **Install dependencies and activate the virtual environment:**

    ```bash
    pipenv install
    pipenv shell
    ```

3.  **Set up the PostgreSQL database:**

    *   Ensure your PostgreSQL server is running.
    *   Create a new database and a user with credentials that match those configured in `config.py`.

## Usage

To start the Flask development server, navigate to the project root directory and execute:

```bash
python app/app.py
```

The API will be accessible at `http://127.0.0.1:8080`.

## API Endpoints

The API provides the following primary endpoints:

*   **`/`**: Index endpoint.
*   **`/transaction`**: Manage individual transactions (GET, POST).
*   **`/transaction_category`**: Manage transaction categories (GET, POST).
*   **`/transaction_type`**: Manage transaction types (GET, POST).
*   **`/transaction_source`**: Manage transaction sources (GET, POST).
*   **`/statistics_by_category`**: Retrieve transaction statistics grouped by category (GET).
*   **`/statistics_by_date`**: Retrieve transaction statistics grouped by date (GET).
*   **`/statistics_by_source`**: Retrieve transaction statistics grouped by source (GET).

For detailed information on request/response formats and specific endpoint functionalities, please refer to the source code within the `namespace` directory.

## Database

The application utilizes a PostgreSQL database for persistent storage of all transaction-related data. The database schema is managed through SQLAlchemy models, which can be found in the `db/models` directory.

## License

This project is licensed under the MIT License - see the `LICENSE.md` file for details.
