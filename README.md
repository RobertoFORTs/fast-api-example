# Simple API

A basic API project designed for demonstration and learning purposes.

## Table of Contents

- [Description](#description)
- [Architecture](#architecture)
- [How to Run](#how-to-run)
- [Testing](#testing)
- [Limitations](#limitations)
- [Possible Improvements](#possible-improvements)

---

## Description

This project implements a simple RESTful API using **FastAPI** in Python. It serves as a template for building maintainable backend services, focusing on simplicity, scalability, and ease of use for learning purposes.

---

## Architecture

- **Framework**: FastAPI
- **Endpoints**: Accessible through `http://localhost:3000/docs` (available when the application is running)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Structure**: 3-layer architecture (API, Domain, Infrastructure)

### Architectural Decision Records (ADRs)

**ADR.01: 3-Layer Architecture**  
The 3-layer architecture (API, Domain, Infrastructure) was chosen for its simplicity, ensuring the delivery of core functionalities in a scalable and maintainable way.

**ADR.02: Async Database Engine**  
An asynchronous database engine was selected over a synchronous one to optimize performance for I/O-bound operations. Async operations enable concurrent database queries without blocking, improving throughput and reducing latency, especially under high load.

**ADR.03: Generic Base Repository Pattern**  
A generic base repository pattern was implemented to provide a consistent interface for data access operations. This reduces code duplication, standardizes database interactions, and simplifies maintenance by centralizing common CRUD operations in a reusable component.

**ADR.04: Pydantic BaseModel**  
Pydantic's `BaseModel` is used for data validation, transfer, and documentation. It integrates seamlessly with Swagger for API documentation and provides robust validation for input/output data.

---

## How to Run

Follow these steps to set up and run the API locally:

1. **Clone the Repository**  
   ```bash
   git clone <repository-url>
   cd simple_api
   ```

2. **Install Poetry**  
   Ensure Poetry is installed. If not, install it using:
   ```bash
   pip install poetry
   ```

3. **Activate Poetry Virtual Environment**  
   ```bash
   poetry shell
   ```

4. **Install Dependencies**  
   Install project dependencies using Poetry:
   ```bash
   poetry install
   ```

5. **Set Up the Database**  
   Create a PostgreSQL database and user with the following commands:
   ```sql
   psql -U postgres
   CREATE DATABASE simple_api_db;
   \c simple_api_db
   CREATE USER admin WITH PASSWORD '123';
   DROP SCHEMA public CASCADE;
   CREATE SCHEMA public;
   ALTER SCHEMA public OWNER TO admin;
   GRANT ALL PRIVILEGES ON SCHEMA public TO admin;
   ```

6. **Configure Environment Variables**  
   Create a `.env` file based on the template below:
   ```env
   ENV="dev" # or "prod"
   APP_NAME="Simple API"
   DATABASE_URL=postgresql+asyncpg://admin:123@localhost/simple_api_db
   ```

7. **Run Database Migrations**  
   Export the `DATABASE_URL` and apply migrations:
   ```bash
   export DATABASE_URL=postgresql+asyncpg://admin:123@localhost/simple_api_db
   alembic upgrade head
   ```

8. **Run the Application**  
   Start the FastAPI server:
   ```bash
   poetry shell
   cd simple_api
   poetry run uvicorn main:app --reload
   ```

9. **Access the API**  
   Open a browser and navigate to:
   ```
   http://localhost:3000/docs
   ```

---

## Testing

To test the API, use the interactive Swagger UI at `http://localhost:3000/docs` to explore and test endpoints. Ensure the application and database are running before testing.

---

## Limitations

- **Manual Migration Setup**: The `.env` file must be exported in the terminal before running Alembic migrations.
- **Local Environment Only**: The application currently runs only on `localhost` with no deployment setup.
- **Separate Initialization**: The database and application must be initialized separately.

---

## Possible Improvements

- **Containerization**: Use Docker to containerize the application and database for easier environment setup.
- **Architecture Upgrade**: Transition to a Hexagonal (Ports and Adapters) architecture with Domain-Driven Design (DDD) and a Modular Monolith approach for scalability:
  - Implement interfaces between layers.
  - Enrich the domain with entities and value objects.
  - Apply the Facade design pattern for model interactions.
- **Testing**: Add unit tests and integration tests.
- **Fitness Functions**: Implement fitness functions to ensure architectural quality.
- **Validation**: Add checks for duplicate properties in data models.