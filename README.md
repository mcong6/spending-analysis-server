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
*   **Environment Management:** Conda

## Getting Started

Follow these instructions to set up and run the project on your local machine for development and testing.

### Prerequisites

*   [Conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html)
*   [Python 3.10](https://www.python.org/downloads/release/python-3100/)
*   [PostgreSQL](https://www.postgresql.org/download/)

### Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/your_username/bank-statement-py.git
    cd bank-statement-py/app
    ```

2.  **Create and activate the Conda environment:**

    The `build.sh` script will create a new Conda environment named `cenv` within the project directory and install all required dependencies from `scripts/environments.yml`.

    ```bash
    bash scripts/build.sh
    conda activate ./cenv
    ```

3.  **Set up the PostgreSQL database:**

    *   Ensure your PostgreSQL server is running.
    *   Create a new database and a user with credentials that match those configured in `config.py`.
    *   By default, the application expects a user `services_user` with the password `Newpassword2023` and a database named `postgres`. You can modify `config.py` to use different credentials.

## Usage

To start the Flask development server, navigate to the `app` directory and execute:

```bash
python app.py
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

## Built With

*   [Flask](https://flask.palletsprojects.com/) - Web framework
*   [Flask-RESTX](https://flask-restx.readthedocs.io/) - Extension for building REST APIs
*   [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/) - SQLAlchemy integration for Flask
*   [Psycopg2](https://www.psycopg.org/) - PostgreSQL adapter for Python
*   [Pipenv](https://pipenv.pypa.io/en/latest/) - Python dependency management and virtual environment tool

## Contributing

Please read `CONTRIBUTING.md` for details on our code of conduct, and the process for submitting pull requests to us.

## License

This project is licensed under the MIT License - see the `LICENSE.md` file for details.

## Acknowledgments

*   Hat tip to anyone whose code was used
*   Inspiration
*   etc