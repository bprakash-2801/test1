<<<<<<< HEAD
# Fraud Detection System

FastAPI backend for managing users, financial transactions, fraud logs, and alert records in a fraud detection workflow.

---

## Table of Contents

- [About the Project](#about-the-project)
- [Key Features](#key-features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)

---

## About the Project

This project provides a REST API for a fraud detection system that stores core operational data for users, transactions, fraud investigation logs, and alerts. It is built with FastAPI and SQLAlchemy, uses environment-based configuration, and organizes the application into clear API, database, model, and schema layers.

The system solves the foundational backend problem of tracking suspicious financial activity in a structured way. It gives developers a starting point for onboarding users, recording transactions, flagging fraud-related events, and managing alert resolution state, while also including automated API tests and database initialization scripts to support local development.

---

## Key Features

**User Management:** Create, list, update, and delete users with validation for unique usernames and email addresses.

**Transaction Tracking:** Record transactions with merchant, category, location, status, fraud score, and fraud flag fields.

**Fraud Logging:** Store fraud detection events with detection method, score, confidence, and investigation reason.

**Alert Management:** Create and update fraud alerts, including severity filtering and resolution tracking.

**Filtering and Pagination:** Query transactions and alerts with pagination plus filters such as user, status, fraud state, severity, and resolution state.

**Automated API Tests:** Includes endpoint tests using FastAPI's `TestClient` and a SQLite-backed test database override.

---

## Tech Stack

| Layer | Technology |
| --- | --- |
| Language | Python |
| Framework | FastAPI |
| Database | PostgreSQL |
| Libraries | SQLAlchemy, Pydantic, pydantic-settings, python-dotenv |
| API | REST API |
| DevOps | Uvicorn |
| Testing | pytest, pytest-asyncio, httpx |

---

## Installation

### Prerequisites

- Python
- PostgreSQL

### Steps

1. Clone the repository.

```bash
git clone <repository-url>
cd demo-project
```

2. Install dependencies.

```bash
pip install -r requirements.txt
```

3. Create the environment file.

```bash
copy .env.example .env
```

4. Update the database settings in `.env` if needed, then create the database tables.

```bash
python init_db.py
```

---

## Usage

### Run the API server

```bash
python main.py
```

The API starts using the host, port, debug mode, and `/api/v1` prefix defined in `.env` and `app/core/config.py`.

### Run the test suite

```bash
python -m pytest
```

The tests override the application database dependency and run against a local SQLite test database.

### Available API areas

The application exposes a root status endpoint at `/`, a health check at `/health`, and versioned REST endpoints under `/api/v1` for users, transactions, fraud logs, and alerts.

---

## Project Structure
```text
demo-project/
|-- app/                    # Main application package
|   |-- api/                # FastAPI route modules and router registration
|   |   |-- __init__.py     # Builds the shared API router
|   |   |-- fraud.py        # Fraud log and alert endpoints
|   |   |-- transactions.py # Transaction CRUD and filtering endpoints
|   |   |-- users.py        # User CRUD endpoints
|   |-- core/               # Application configuration layer
|   |   |-- __init__.py     # Re-exports application settings
|   |   |-- config.py       # Loads environment-driven settings
|   |-- database/           # Database engine and session management
|   |   |-- __init__.py     # Re-exports database utilities
|   |   |-- session.py      # SQLAlchemy engine, base model, and DB dependency
|   |-- models/             # SQLAlchemy ORM models
|   |   |-- __init__.py     # Exposes ORM model classes
|   |   |-- alert.py        # Alert persistence model
|   |   |-- fraud_log.py    # Fraud log persistence model
|   |   |-- transaction.py  # Transaction persistence model
|   |   |-- user.py         # User persistence model
|   |-- schemas/            # Pydantic request and response schemas
|   |   |-- __init__.py     # Exposes schema classes
|   |   |-- fraud.py        # Fraud log and alert schemas
|   |   |-- transaction.py  # Transaction schemas
|   |   |-- user.py         # User schemas
|   |-- services/           # Placeholder package for business logic services
|   |   |-- __init__.py     # Notes future service-layer expansion
|   |-- __init__.py         # Application package metadata
|-- tests/                  # Automated API tests
|   |-- __init__.py         # Marks the tests package
|   |-- test_api.py         # Endpoint tests using a SQLite test database
|-- .env.example            # Example environment configuration
|-- .gitignore              # Git ignore rules
|-- init_db.py              # Script to create database tables
|-- main.py                 # FastAPI application entrypoint
|-- README.md               # Project documentation
|-- requirements.txt        # Python dependency definitions
```
=======

afjdkajdfklf
>>>>>>> b3433134bbe9a671bce3848da2dfd7aa37558bd6
