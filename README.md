# Tron-Wallet-Scan

**Tron-Wallet-Scan** is a simple web service that allows users to scan TRON (TRX) wallet addresses for relevant on-chain data including TRX balance, bandwidth, and energy. The service also stores the wallet addresses in a database and provides a paginated list of saved wallets.

## Features

- Scan a wallet for:
  - TRX balance
  - Bandwidth
  - Energy
- Store scanned wallet addresses in a database
- Retrieve a paginated list of stored wallet addresses

## API Endpoints

### 1. Scan Wallet Information

**Endpoint:**

`POST /wallet/scan`

**Description:**

Scans a TRON wallet address for current on-chain data and stores the address in the database.

**Request Body:**

```json
{
  "address": "TXXXXXXXXXXXXXXXXXXXXXXXXX"
}
```

**Response:**

```json
{
  "balance": 123.456,
  "bandwidth": 5000,
  "energy": 10000
}
```


### 2. List Wallets (Paginated)


**Endpoint:**

`GET /wallets`

**Description:**

Returns a paginated list of previously scanned wallet addresses.

**Query Parameters:**

| Parameter | Type | Description                                         |
|-----------|------|-----------------------------------------------------|
| `page`    | int  | The page number (starting from 1)                   |
| `limit`   | int  | Number of wallet addresses per page (default 10)    |

**Example Request:**

`GET /wallets?page=2&limit=5`

**Response:**

```json
[
  "TXXXXXXXXXXXXXXXXXXXXXXXXX",
  "TYYYYYYYYYYYYYYYYYYYYYYYYY",
  "TZZZZZZZZZZZZZZZZZZZZZZZZZ"
]
```


## Setup & Installation

### Prerequisites

- Python 3.12+
- [Poetry](https://python-poetry.org/docs/#installation)

### Installation Steps

1. **Clone the Repository**

```bash
git clone https://github.com/your-org/tron-wallet-scan.git
cd tron-wallet-scan
```

2. ❗**Create .env file by .env.example file and write env variables there**

3. **Apply migrations to your local database**

```bash
alembic upgrade head
```

4. **Install Dependencies**

```bash
poetry install
```

5. **Activate the Virtual Environment**

```bash
poetry shell
```

6. **Run the FastAPI App**

```bash
uvicorn app:create_app --reload
```

## Tests

Run this command to start all tests
```bash
make test
```


## Technical Debt

- ❗ **Docker Support Needed**  
  Currently, the project does not include a `Dockerfile` or `docker-compose` setup. Containerizing the application would improve portability and ease of deployment across different environments. This should include:
  - A `Dockerfile` to build the FastAPI + Poetry app
  - Optional `docker-compose.yml` for local dev with a database (e.g., PostgreSQL)
  - Volume mapping for local `.env` and database data